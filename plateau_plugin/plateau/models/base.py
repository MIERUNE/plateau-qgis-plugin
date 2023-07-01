import re
from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Literal, Optional, Sequence

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
class LODDetection:
    """各LODの存在を判定するための XML Paths を列挙する"""

    lod0: Optional[list[str]] = None
    lod1: Optional[list[str]] = None
    lod2: Optional[list[str]] = None
    lod3: Optional[list[str]] = None
    lod4: Optional[list[str]] = None
    lod_n: Optional[str] = None


@dataclass
class FeatureEmission:
    collect_all: list[str]
    """この地物の階層下にある全ジオメトリを収集するための element path (部分要素に分けずに読み込む場合に使う) """

    only_direct: Optional[list[str]] = None
    """この地物の直下にあるジオメトリを収集するための element path"""

    geometry_loader: Literal["polygons"] = "polygons"


@dataclass
class FeatureEmissions:
    """地物の出力について記述する"""

    lod0: Optional[FeatureEmission] = None
    lod1: Optional[FeatureEmission] = None
    lod2: Optional[FeatureEmission] = None
    lod3: Optional[FeatureEmission] = None
    lod4: Optional[FeatureEmission] = None

    semantic_parts: Optional[list[str]] = None
    """子地物への element paths"""


@dataclass
class Attribute:
    name: str
    path: str
    datatype: PropertyDatatype
    predefined_codelist: Optional[str] = None


@dataclass
class AttributeGroup:
    """属性抽出をグルーピングする"""

    base_element: Optional[str]
    """属性抽出の起点とするXML要素への element path。None の場合はこの地物自体を起点とする。"""

    attributes: Sequence[Attribute]
    # mode: Literal["flatten", "map"] = "flatten"


@dataclass
class FeatureProcessingDefinition:
    """各地物の処理方法を定める"""

    id: str
    """このProcessorのID"""

    target_elements: list[str]
    """処理対象とする地物要素 (e.g. "tran:Road", "tran:TrafficArea", "bldg:WallSurface")"""

    lod_detection: LODDetection
    """各 LOD の有無を判定するための element paths"""

    attribute_groups: list[AttributeGroup]
    """取得したい属性の定義"""

    emissions: FeatureEmissions
    """ジオメトリの抽出についての定義"""

    load_generic_attributes: bool = False
    """gen:stringAttribute などの汎用属性を読み込むかどうか"""

    def detect_lods(self, elem: et._Element, nsmap: dict[str, str]) -> tuple[bool, ...]:
        """
        どの LOD が存在するかを返す。例: LOD1と2のとき → (False, True, True, False, False)
        """
        det = self.lod_detection
        if det.lod_n:
            lod = int(elem.find(det.lod_n, BASE_NS).text)
            return tuple(lod == i for i in range(5))
        return (
            bool(det.lod0 and any(elem.find(p, nsmap) is not None for p in det.lod0)),
            bool(det.lod1 and any(elem.find(p, nsmap) is not None for p in det.lod1)),
            bool(det.lod2 and any(elem.find(p, nsmap) is not None for p in det.lod2)),
            bool(det.lod3 and any(elem.find(p, nsmap) is not None for p in det.lod3)),
            bool(det.lod4 and any(elem.find(p, nsmap) is not None for p in det.lod4)),
        )

    @cached_property
    def emission_list(self) -> tuple[Optional[FeatureEmission], ...]:
        emissions = self.emissions
        return (
            emissions.lod0,
            emissions.lod1,
            emissions.lod2,
            emissions.lod3,
            emissions.lod4,
        )


class ProcessorRegistory:
    """地物を処理する Processors を登録しておくレジストリ"""

    def __init__(
        self, processors: Optional[Iterable[FeatureProcessingDefinition]] = None
    ):
        self._tag_map: dict[str, FeatureProcessingDefinition] = {}
        self._id_map: dict[str, FeatureProcessingDefinition] = {}
        if processors:
            for processor in processors:
                self.register_processor(processor)

    def _make_prefix_variants(self, prefixed_names: Iterable[str]) -> list[str]:
        names = []
        for name in prefixed_names:
            prefix, n = name.split(":", 1)
            if prefix == "uro":
                names.append("uro14:" + n)
                names.append("uro15:" + n)
                names.append("uro2:" + n)
                names.append("uro3:" + n)
            if prefix == "urf":
                names.append("urf14:" + n)
                names.append("urf15:" + n)
                names.append("urf2:" + n)
                names.append("urf3:" + n)
        return names

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

    def get_processor_by_id(self, _id: str) -> FeatureProcessingDefinition:
        """Processor の id をもとに Processor を取得する"""
        return self._id_map[_id]

    def validate_processors(self):
        from pathlib import Path

        from ..codelists import CodelistStore

        codelists = CodelistStore(Path("./"))

        for processor in self._id_map.values():
            for group in processor.attribute_groups:
                for prop in group.attributes:
                    if prop.predefined_codelist:
                        codelists.get_predefined(prop.predefined_codelist)
