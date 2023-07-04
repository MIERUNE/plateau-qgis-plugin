import re
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Iterator, Literal, Optional, Sequence, Union

import lxml.etree as et

from ..namespaces import BASE_NS

PropertyDatatype = Literal[
    "string",
    "[]string",
    "integer",
    "double",
    "datetime",
    "boolean",
    "date",
    "object",
    "[]object",
]


@dataclass
class FeatureEmission:
    lod_detection: Sequence[str]

    collect_all: Sequence[str]
    """このFeatureの階層下にある全ジオメトリを収集するための element path (部分要素に分けずに読み込む場合に使う) """

    only_direct: Optional[list[str]] = None
    """このFeatureの直下にあるジオメトリを収集するための element path"""


@dataclass
class FeatureEmissions:
    """Featureの出力について記述する"""

    lod0: Optional[FeatureEmission] = None
    lod1: Optional[FeatureEmission] = None
    lod2: Optional[FeatureEmission] = None
    lod3: Optional[FeatureEmission] = None
    lod4: Optional[FeatureEmission] = None

    lod_n: Optional[str] = None
    lod_n_paths: Optional[FeatureEmission] = None

    semantic_parts: Optional[list[str]] = None
    """子Featureへの element paths"""


@dataclass
class Attribute:
    name: str
    path: str
    datatype: PropertyDatatype
    predefined_codelist: Optional[Union[str, dict[str, str]]] = None


@dataclass
class AttributeGroup:
    """属性抽出をグルーピングする"""

    base_element: Optional[str]
    """属性抽出の起点とするXML要素への element path。None の場合はこのFeature自体を起点とする。"""

    attributes: Sequence[Attribute]
    # mode: Literal["flatten", "map"] = "flatten"


@dataclass
class FacilityAttributePaths:
    facility_types: str
    facility_id: str
    facility_attrs: str
    large_customer_facility_attrs: Optional[str] = None


@dataclass
class FeatureProcessingDefinition:
    """各 Feature の処理方法を定める"""

    id: str
    """このProcessorのID"""

    target_elements: list[str]
    """処理対象とするFeature要素 (e.g. "tran:Road", "tran:TrafficArea", "bldg:WallSurface")"""

    attribute_groups: list[AttributeGroup]
    """取得したい属性の定義"""

    emissions: FeatureEmissions
    """ジオメトリの抽出についての定義"""

    load_generic_attributes: bool = False
    """汎用属性 (gen:stringAttribute など) を読み込むかどうか"""

    dm_attr_container: Optional[str] = None
    """公共測量標準図式 uro:DmAttribute を包含する要素 (e.g. bldg:bldgDmAttribute) への element path"""

    facility_attr_paths: Optional[FacilityAttributePaths] = None
    """施設管理の応用スキーマ関連の属性へのpath"""

    disaster_risk_attr_conatiner_path: Optional[str] = None
    """災害リスク属性 uro:(Building)DisasterRiskAttribute を包含する要素への element path"""

    non_geometric: bool = False
    """ジオメトリを持たない Feature であるかどうか"""

    def detect_lods(self, elem: et._Element, nsmap: dict[str, str]) -> tuple[bool, ...]:
        """
        どの LoD が存在するかを返す。例: LoD1と2のとき → (False, True, True, False, False)
        """
        det = self.emissions
        if det.lod_n:
            lod = int(elem.find(det.lod_n, BASE_NS).text)
            return tuple(lod == i for i in range(5))
        else:
            return tuple(
                bool(
                    em
                    and any(elem.find(p, nsmap) is not None for p in em.lod_detection)
                )
                for em in self.emission_list
            )

    @cached_property
    def emission_list(self) -> tuple[Optional[FeatureEmission], ...]:
        return (
            self.emissions.lod0,
            self.emissions.lod1,
            self.emissions.lod2,
            self.emissions.lod3,
            self.emissions.lod4,
        )


class ProcessorRegistory:
    """Featureを処理する Processors を登録しておくレジストリ"""

    def __init__(
        self, processors: Optional[Iterable[FeatureProcessingDefinition]] = None
    ):
        self._tag_map: dict[str, FeatureProcessingDefinition] = {}
        self._id_map: dict[str, FeatureProcessingDefinition] = {}
        if processors:
            for processor in processors:
                self.register_processor(processor)

    def _make_prefix_variants(self, prefixed_names: Iterable[str]) -> Iterator[str]:
        for name in prefixed_names:
            prefix, n = name.split(":", 1)
            if prefix == "uro":
                yield "uro14:" + n
                yield "uro15:" + n
                yield "uro2:" + n
                yield "uro3:" + n
            elif prefix == "urf":
                yield "urf14:" + n
                yield "urf15:" + n
                yield "urf2:" + n
                yield "urf3:" + n
            else:
                yield name

    def register_processor(self, processor: FeatureProcessingDefinition):
        """Processor を登録する"""
        assert (
            processor.id not in self._id_map
        ), f"Processor id {processor.id} is already registered"

        self._id_map[processor.id] = processor
        for prefixed_name in self._make_prefix_variants(processor.target_elements):
            qualified_name = re.sub(
                r"^(.+?):()", lambda m: "{" + BASE_NS[m.group(1)] + "}", prefixed_name
            )
            assert prefixed_name not in self._tag_map
            self._tag_map[prefixed_name] = processor
            assert qualified_name not in self._tag_map
            self._tag_map[qualified_name] = processor

    def get_processor_by_tag(
        self, target_tag: str
    ) -> Optional[FeatureProcessingDefinition]:
        """XMLの要素名をもとに Processor を取得する"""
        return self._tag_map.get(target_tag)

    def validate_processors(self):
        from pathlib import Path

        from ..codelists import CodelistStore

        codelists = CodelistStore(Path("./"))

        for processor in self._id_map.values():
            for group in processor.attribute_groups:
                for prop in group.attributes:
                    if prop.predefined_codelist:
                        if isinstance(prop.predefined_codelist, str):
                            codelists.get_predefined(prop.predefined_codelist)
                        else:
                            for a in prop.predefined_codelist.values():
                                codelists.get_predefined(a)
