from collections import OrderedDict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Optional

import lxml.etree as et

from .codelists import CodelistStore
from .geometry import parse_multipolygon
from .models import processors
from .models.base import FeatureProcessingDefinition
from .namespaces import Namespace
from .types import CityObject

_BOOLEAN_TRUE_STRINGS = frozenset({"true", "True", "1"})


@dataclass
class ParseSettings:
    load_semantic_parts: bool = False
    """部分要素 (e.g. Road の細分化の TrafficArea) に分けて読み込むかどうか"""

    only_highest_lod: bool = False
    """各地物の最高の LOD だけ出力するかどうか"""


class Parser:
    def __init__(
        self, settings: ParseSettings, ns: Namespace, codelist_store: CodelistStore
    ) -> None:
        self._settings = settings
        self._ns: Namespace = ns
        self._nsmap: dict[str, str] = ns.nsmap
        self._codelist_store = codelist_store

    def _get_id_and_name(self, elem: et._Element):
        """@gml:id と gml:name (あれば) を読む"""
        nsmap = self._nsmap
        gml_id = elem.get("{http://www.opengis.net/gml}id", None)
        if (name_elem := elem.find("./gml:name", nsmap)) is not None:
            gml_name = name_elem.text
            if path := name_elem.get("codeSpace"):
                gml_name = self._codelist_store.lookup(None, path, gml_name)
        else:
            gml_name = None

        return (gml_id, gml_name)

    def _get_basic_dates(
        self, elem: et._Element
    ) -> tuple[Optional[date], Optional[date]]:
        """core:creationDate (あれば) と core:terminationDate (あれば) を読む"""
        nsmap = self._nsmap
        creation_date = (
            date.fromisoformat(name_elem.text)
            if (name_elem := elem.find("./core:creationDate", nsmap)) is not None
            else None
        )
        termination_date = (
            date.fromisoformat(name_elem.text)
            if (name_elem := elem.find("./core:terminationDate", nsmap)) is not None
            else None
        )
        return (creation_date, termination_date)

    def _load_props(  # noqa: C901
        self, processor: FeatureProcessingDefinition, feature_elem: et._Element
    ) -> OrderedDict[str, Any]:
        nsmap = self._nsmap
        props = OrderedDict()
        codelist_lookup = self._codelist_store.lookup

        if processor.load_generic_attributes:
            props["generic"] = self._parse_generic_attributes(feature_elem)

        for group in processor.attribute_groups:
            if group.base_element is None:
                base_elem = feature_elem
            else:
                base_elem = feature_elem.find(group.base_element, nsmap)
                if base_elem is None:
                    continue

            for prop in group.attributes:
                assert prop.name in prop.path, f"{prop.name} not in {prop.path}"
                if prop.datatype == "[]string":
                    values = []
                    for child_elem in base_elem.iterfind(prop.path, nsmap):
                        v = child_elem.text
                        path = child_elem.get("codeSpace")
                        if prop.predefined_codelist or path:
                            v = codelist_lookup(prop.predefined_codelist, path, v)
                        values.append(v)
                    props[prop.name] = values
                else:
                    if (child_elem := base_elem.find(prop.path, nsmap)) is not None:
                        value = child_elem.text
                    else:
                        continue

                    if prop.datatype == "string":
                        v = str(value)
                        path = child_elem.get("codeSpace")
                        if prop.predefined_codelist or path:
                            v = codelist_lookup(prop.predefined_codelist, path, v)
                        props[prop.name] = v
                    elif prop.datatype == "double":
                        props[prop.name] = float(value)
                    elif prop.datatype == "integer":
                        props[prop.name] = int(value)
                    elif prop.datatype == "boolean":
                        props[prop.name] = bool(value in _BOOLEAN_TRUE_STRINGS)
                    elif prop.datatype == "date":
                        props[prop.name] = date.fromisoformat(value)
                    else:
                        raise NotImplementedError(f"Unknown datatype: {prop.datatype}")
        return props

    def _parse_generic_attributes(  # noqa: C901
        self, elem: et._Element
    ) -> dict[str, Any]:
        nsmap = self._nsmap
        generic_attrs = {}

        for gen in elem.iterfind("gen:genericAttributeSet", nsmap):
            if name := gen.get("name"):
                generic_attrs[name] = self._parse_generic_attributes(gen)

        for gen in elem.iterfind("gen:stringAttribute", nsmap):
            if (name := gen.get("name")) and (
                value := gen.find("./gen:value", nsmap)
            ) is not None:
                generic_attrs[name] = value.text

        for gen in elem.iterfind("gen:intAttribute", nsmap):
            if (name := gen.get("name")) and (
                value := gen.find("./gen:value", nsmap)
            ) is not None:
                generic_attrs[name] = int(value.text)

        for gen in elem.iterfind("gen:doubleAttribute", nsmap):
            if (name := gen.get("name")) and (
                value := gen.find("./gen:value", nsmap)
            ) is not None:
                generic_attrs[name] = float(value.text)

        for gen in elem.iterfind("gen:measureAttribute", nsmap):
            if (name := gen.get("name")) and (
                value := gen.find("./gen:value", nsmap)
            ) is not None:
                generic_attrs[name] = float(value.text)

        for gen in elem.iterfind("gen:dateAttribute", nsmap):
            if (name := gen.get("name")) and (
                value := gen.find("./gen:value", nsmap)
            ) is not None:
                generic_attrs[name] = value.text

        return generic_attrs

    def process_cityobj_element(  # noqa: C901
        self,
        elem: et._Element,
        parent: Optional[CityObject],  # 祖先地物の Processor
    ) -> Iterable[CityObject]:
        ns = self._ns
        nsmap = self._nsmap

        (gml_id, gml_name) = self._get_id_and_name(elem)
        (creation_date, termination_date) = self._get_basic_dates(elem)

        # この要素のための Processor を得る
        processor = processors.get_processor_by_tag(elem.tag)
        if processor is None:
            return

        # 属性を収集する
        props = self._load_props(processor, elem)

        # 子地物 (部分要素) を個別に読み込む設定の場合は、子地物を探索する
        if self._settings.load_semantic_parts and processor.emissions.semantic_parts:
            # 親地物 (ジオメトリなし) を用意する
            nogeom_obj = CityObject(
                type=ns.to_prefixed_name(elem.tag),
                id=gml_id,
                name=gml_name,
                creation_date=creation_date,
                termination_date=termination_date,
                lod=None,
                geometry=None,
                attributes=props,
                processor=processor,
                parent=parent,
            )

            found_child = False
            for path in processor.emissions.semantic_parts:
                for child_cityobj in elem.iterfind(path, nsmap):
                    # 子地物の Processor に処理を委ねる
                    for child in self.process_cityobj_element(
                        child_cityobj, nogeom_obj
                    ):
                        found_child = True
                        yield child

            if found_child:
                # 親地物 (ジオメトリなし) を出力する
                yield nogeom_obj

        # ジオメトリを読んで出力する
        emission_for_lods = processor.emission_list
        has_lods = processor.detect_lods(elem, nsmap)
        for lod in (4, 3, 2, 1, 0):
            if not has_lods[lod]:
                continue

            emission = emission_for_lods[lod]
            if emission is None:
                continue

            # 子地物を読む設定かどうかによって探索方法を変える
            geom_paths = (
                emission.only_direct or emission.collect_all
                if self._settings.load_semantic_parts
                else emission.collect_all
            )
            if emission.geometry_loader == "polygons":
                geom = parse_multipolygon(elem, geom_paths, nsmap)
            else:
                raise NotImplementedError(
                    f"Unknown geometry loader: {emission.geometry_loader}"
                )

            if geom:
                yield CityObject(
                    lod=lod,
                    type=ns.to_prefixed_name(elem.tag),
                    id=gml_id,
                    name=gml_name,
                    creation_date=creation_date,
                    termination_date=termination_date,
                    attributes=props,
                    geometry=geom,
                    processor=processor,
                    parent=parent,
                )

            if self._settings.only_highest_lod:
                # 各地物の最高 LOD だけ出力する設定の場合はここで離脱
                break


class FileParser:
    def __init__(self, filename: str, settings: ParseSettings):
        self._base_dir = Path(filename).parent
        self._doc = et.parse(filename, None)
        self._settings = settings

        # ドキュメントで使われている i-UR のバージョンを検出して
        # uro: と urf: 接頭辞が指すXML名前空間を自動で決定する
        self._ns = Namespace.from_document_nsmap(self._doc.getroot().nsmap)

    def count_toplevel_cityobjs(self) -> int:
        """ファイルに含まれるトップレベルの地物の数を返す"""
        return sum(
            1 for _ in self._doc.iterfind("./core:cityObjectMember", self._ns.nsmap)
        )

    def iter_cityobjs(self) -> Iterable[tuple[int, CityObject]]:
        """ファイルに含まれる地物の数を返す"""

        codelists = CodelistStore(self._base_dir)
        parser = Parser(self._settings, ns=self._ns, codelist_store=codelists)
        toplevel_count = 0
        for city_object in self._doc.iterfind(
            "./core:cityObjectMember/*", self._ns.nsmap
        ):
            for cityobj in parser.process_cityobj_element(city_object, parent=None):
                yield (toplevel_count, cityobj)
            toplevel_count += 1
