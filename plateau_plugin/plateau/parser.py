from collections import OrderedDict
from typing import Iterable

import lxml.etree as et

from .codelists import get_codelist
from .geometry import parse_multipolygon
from .models import processors
from .namespaces import _NS, to_prefixed_name
from .types import CityObject


def process_cityobj_element(
    elem: et._Element,
    ancestors: list[tuple[str, str]],  # 親地物の (target_element, gml_id)
) -> Iterable[CityObject]:
    gml_id = elem.get("{http://www.opengis.net/gml}id", None)
    gml_name = (
        name_elem.text
        if (name_elem := elem.find("./gml:name", _NS)) is not None
        else None
    )
    props = OrderedDict()
    props["id"] = gml_id
    props["name"] = gml_name

    processor = processors.get_processor_by_tag(elem.tag)
    if processor is None:
        return

    for attr in processor.attributes:
        values = elem.xpath(attr.xpath, namespaces=_NS)
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

    has_lods = processor.get_lods(elem)
    emissions_for_lod = processor.emissions_list
    children_for_lod = processor.children_paths_list
    has_children = False
    new_ancestors = [*ancestors, (processor.id, gml_id)]
    for lod in (4, 3, 2, 1):
        if not has_lods[lod]:
            continue

        if paths := children_for_lod[lod]:
            for path in paths:
                for child in elem.iterfind(path, _NS):
                    yield from process_cityobj_element(child, new_ancestors)
                    has_children = True

        else:
            emission = emissions_for_lod[lod]
            if not emission:
                continue

            if emission.geometry_loader == "polygons":
                geom = parse_multipolygon(elem, emission.elem_paths)
            else:
                raise NotImplementedError(
                    f"Unknown geometry loader: {emission.geometry_loader}"
                )

            if geom:
                yield CityObject(
                    lod=lod,
                    type=to_prefixed_name(elem.tag),
                    properties=props,
                    geometry=geom,
                    processor_path=new_ancestors,
                )

    if has_children:
        # 子地物を出力したときは、親の情報を含んだジオメトリなしの地物を出力する
        yield CityObject(
            type=to_prefixed_name(elem.tag),
            lod=None,
            geometry=None,
            properties=props,
            processor_path=new_ancestors,
        )


class FileParser:
    def __init__(self, filename: str):
        self._doc = et.parse(filename, None)

    def count_toplevel_objects(self):
        return sum(1 for _ in self._doc.iterfind("./core:cityObjectMember", _NS))

    def iter_city_objects(self) -> Iterable[tuple[int, CityObject]]:
        toplevel_count = 0
        for city_object in self._doc.iterfind("./core:cityObjectMember/*", _NS):
            for cityobj in process_cityobj_element(city_object, ancestors=[]):
                yield (toplevel_count, cityobj)
            toplevel_count += 1
