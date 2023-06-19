from collections import OrderedDict
from typing import Iterable

import lxml.etree as et

from .codelists import get_codelist
from .geometry import parse_multipolygon
from .models import processors
from .namespaces import Namespace
from .types import CityObject, ParseSettings


def process_cityobj_element(
    elem: et._Element,
    settings: ParseSettings,
    ancestors: list[tuple[str, str]],  # 親地物の (target_element, gml_id)
) -> Iterable[CityObject]:
    ns = settings.namespace
    nsmap = ns.nsmap

    gml_id = elem.get("{http://www.opengis.net/gml}id", None)
    gml_name = (
        name_elem.text
        if (name_elem := elem.find("./gml:name", nsmap)) is not None
        else None
    )
    props = OrderedDict()
    props["id"] = gml_id
    props["name"] = gml_name

    processor = processors.get_processor_by_tag(elem.tag)
    if processor is None:
        return

    for attr in processor.attributes:
        values = [e.text for e in elem.iterfind(attr.path, nsmap)]
        if attr.datatype == "[]string":
            values = [str(v) for v in values]
            if attr.codelist:
                cl = get_codelist(attr.codelist)
                values = [cl.get(v, v) for v in values]
            props[attr.name] = values
        elif attr.datatype == "string":
            if not values:
                continue
            v = str(values[0])
            if attr.codelist:
                cl = get_codelist(attr.codelist)
                v = cl.get(v, v)
            props[attr.name] = v
        else:
            raise NotImplementedError(f"Unknown datatype: {attr.datatype}")

    emissions_for_lod = processor.emissions_list
    new_ancestors = [*ancestors, (processor.id, gml_id)]
    is_semantic_parts_mode = True
    has_semantic_parts = False

    if is_semantic_parts_mode and processor.emissions.semantic_parts:
        for path in processor.emissions.semantic_parts:
            for child in elem.iterfind(path, nsmap):
                yield from process_cityobj_element(child, settings, new_ancestors)
                has_semantic_parts = True

    has_lods = processor.get_lods(elem, nsmap)
    for lod in (4, 3, 2, 1):
        if not has_lods[lod]:
            continue

        if (emission := emissions_for_lod[lod]) is None:
            continue

        geom_paths = (
            (emission.direct or emission.catch_all)
            if is_semantic_parts_mode
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
                properties=props,
                geometry=geom,
                processor_path=new_ancestors,
            )

    if has_semantic_parts:
        # 子地物を出力したときは、親の情報を含んだジオメトリなしの地物を出力する
        yield CityObject(
            type=ns.to_prefixed_name(elem.tag),
            lod=None,
            geometry=None,
            properties=props,
            processor_path=new_ancestors,
        )


class FileParser:
    def __init__(self, filename: str):
        self._doc = et.parse(filename, None)

        # Detect i-UR versions
        self._ns = Namespace.from_document_nsmap(self._doc.getroot().nsmap)

    def count_toplevel_objects(self):
        return sum(
            1 for _ in self._doc.iterfind("./core:cityObjectMember", self._ns.nsmap)
        )

    def iter_city_objects(self) -> Iterable[tuple[int, CityObject]]:
        settings = ParseSettings(namespace=self._ns)
        toplevel_count = 0
        for city_object in self._doc.iterfind(
            "./core:cityObjectMember/*", self._ns.nsmap
        ):
            for cityobj in process_cityobj_element(city_object, settings, ancestors=[]):
                yield (toplevel_count, cityobj)
            toplevel_count += 1
