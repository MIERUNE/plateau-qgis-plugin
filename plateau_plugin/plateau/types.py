from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Union

import numpy as np

from .namespaces import Namespace


@dataclass
class MultiPoint:
    __slots__ = ["points"]  # noqa
    points: np.ndarray


@dataclass
class MultiLineString:
    __slots__ = ["lines"]  # noqa
    lines: list[np.ndarray]


@dataclass
class MultiPolygon:
    __slots__ = ["polygons"]  # noqa
    polygons: list[list[np.ndarray]]


Geometry = Union[MultiPolygon, MultiLineString, MultiPoint, None]


@dataclass
class CityObject:
    lod: Literal[0, 1, 2, 3, 4, None]  # 0, 1, 2, 3, 4 or None (ジオメトリなし)
    type: str  # この地物の型名 (e.g. Road, TrafficArea, etc.)
    properties: OrderedDict[str, Any]  # この地物のプロパティ
    geometry: Geometry
    processor_path: list[tuple[str, str]]  # この要素に至るまでに使われた (processor.id, gml:id) のリスト


@dataclass
class ParseSettings:
    namespace: Namespace
