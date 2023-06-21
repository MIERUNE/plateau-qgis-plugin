from collections import OrderedDict
from datetime import date
from typing import Any, Iterable, Optional, Sequence

import lxml.etree as et

from .codelists import get_codelist
from .geometry import parse_multipolygon
from .models import processors
from .models.base import ProcessorDefinition
from .namespaces import Namespace
from .types import CityObject, ParseSettings

_BOOLEAN_VALUES = frozenset({"true", "True", "1"})


class Parser:
    def __init__(self, settings: ParseSettings, ns: Namespace) -> None:
        self._settings = settings
        self._ns: Namespace = ns
        self._nsmap: dict[str, str] = ns.nsmap

    def _get_id_and_name(self, elem: et._Element):
        nsmap = self._nsmap
        gml_id = elem.get("{http://www.opengis.net/gml}id", None)
        gml_name = (
            name_elem.text
            if (name_elem := elem.find("./gml:name", nsmap)) is not None
            else None
        )
        return (gml_id, gml_name)

    def _get_creation_date(self, elem: et._Element):
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

    def _load_props(
        self, processor: ProcessorDefinition, feature_elem: et._Element
    ) -> OrderedDict[str, Any]:
        nsmap = self._nsmap
        props = OrderedDict()
        for group in processor.property_groups:
            if group.base_element is None:
                base_elem = feature_elem
            else:
                base_elem = feature_elem.find(group.base_element, nsmap)
                if base_elem is None:
                    continue

            for prop in group.properties:
                if prop.datatype == "[]string":
                    values = [str(e.text) for e in base_elem.iterfind(prop.path, nsmap)]
                    if prop.codelist:
                        cl = get_codelist(prop.codelist)
                        values = [cl.get(v, v) for v in values]
                    props[prop.name] = values
                else:
                    if (child_elem := base_elem.find(prop.path, nsmap)) is not None:
                        value = child_elem.text
                    else:
                        continue
                    if prop.datatype == "string":
                        v = str(value)
                        if prop.codelist:
                            cl = get_codelist(prop.codelist)
                            v = cl.get(v, v)
                        props[prop.name] = v
                    elif prop.datatype == "double":
                        props[prop.name] = float(value)
                    elif prop.datatype == "integer":
                        props[prop.name] = int(value)
                    elif prop.datatype == "boolean":
                        props[prop.name] = bool(value in _BOOLEAN_VALUES)
                    else:
                        raise NotImplementedError(f"Unknown datatype: {prop.datatype}")
        return props

    def process_cityobj_element(
        self,
        elem: et._Element,
        ancestors: Sequence[tuple[str, str]],  # 親地物の (target_element, gml_id)
    ) -> Iterable[CityObject]:
        ns = self._ns
        nsmap = ns.nsmap

        (gml_id, gml_name) = self._get_id_and_name(elem)
        (creation_date, _termination_date) = self._get_creation_date(elem)

        # この要素のための Processor を得る
        processor = processors.get_processor_by_tag(elem.tag)
        if processor is None:
            return

        # 部分要素を個別に読む設定の場合は、部分要素を探索する
        new_ancestors = (*ancestors, (processor.id, gml_id))
        if self._settings.load_semantic_parts and processor.emissions.semantic_parts:
            for path in processor.emissions.semantic_parts:
                for child in elem.iterfind(path, nsmap):
                    yield from self.process_cityobj_element(child, new_ancestors)
                    has_semantic_parts = True

        # 属性 (プロパティ) の値を収集する
        props = self._load_props(processor, elem)

        emissions_for_lod = processor.emissions_list
        has_lods = processor.get_lods(elem, nsmap)
        has_semantic_parts = False
        for lod in (4, 3, 2, 1):
            if not has_lods[lod]:
                continue

            if (emission := emissions_for_lod[lod]) is None:
                continue

            geom_paths = (
                (emission.direct or emission.catch_all)
                if self._settings.load_semantic_parts
                else emission.catch_all
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
                    termination_date=_termination_date,
                    properties=props,
                    geometry=geom,
                    processor_path=new_ancestors,
                )
                if self._settings.only_highest_lod:  # 各地物の最高のLODだけ出力する場合
                    break

        if has_semantic_parts:
            # 子地物を出力したときは、親の情報を含んだジオメトリなしの地物を出力する
            yield CityObject(
                type=ns.to_prefixed_name(elem.tag),
                id=gml_id,
                name=gml_name,
                creation_date=creation_date,
                termination_date=_termination_date,
                lod=None,
                geometry=None,
                properties=props,
                processor_path=new_ancestors,
            )


class FileParser:
    def __init__(self, filename: str, settings: ParseSettings):
        self._doc = et.parse(filename, None)
        self._settings = settings

        # ドキュメントで使われている i-UR のバージョンを検出して
        # uro: と urf: 接頭辞のXML名前空間に自動で対応する
        self._ns = Namespace.from_document_nsmap(self._doc.getroot().nsmap)

    def count_toplevel_objects(self):
        return sum(
            1 for _ in self._doc.iterfind("./core:cityObjectMember", self._ns.nsmap)
        )

    def iter_city_objects(self) -> Iterable[tuple[int, CityObject]]:
        parser = Parser(self._settings, ns=self._ns)
        toplevel_count = 0
        for city_object in self._doc.iterfind(
            "./core:cityObjectMember/*", self._ns.nsmap
        ):
            for cityobj in parser.process_cityobj_element(city_object, ancestors=[]):
                yield (toplevel_count, cityobj)
            toplevel_count += 1
