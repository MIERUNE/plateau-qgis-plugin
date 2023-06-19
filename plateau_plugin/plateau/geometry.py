from typing import Iterable, Optional

import lxml.etree as et
import numpy as np

from .namespaces import _NS
from .types import MultiPolygon


def parse_multipolygon(
    element: et._Element, polygon_paths: Iterable[str]
) -> Optional[MultiPolygon]:
    polygons = []
    for polygon_path in polygon_paths:
        for polygon in element.iterfind(polygon_path, _NS):
            pos_list = polygon.find("./gml:exterior//gml:posList", _NS)
            vertices = np.fromstring(pos_list.text, dtype=np.float64, sep=" ")
            exterior = vertices.reshape(-1, 3)
            rings = []
            rings.append(exterior)
            for pos_list in polygon.iterfind("./gml:interior//gml:posList", _NS):
                vertices = np.fromstring(pos_list.text, dtype=np.float64, sep=" ")
                vertices = vertices.reshape(-1, 3)
                rings.append(vertices)

            polygons.append(rings)

    if polygons:
        return MultiPolygon(polygons=polygons)
    else:
        return None
