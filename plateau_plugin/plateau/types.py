from collections import OrderedDict
from dataclasses import dataclass
from datetime import date
from typing import Any, Literal, Optional, Sequence, Union

import numpy as np


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
    id: str
    name: Optional[str]
    creation_date: Optional[date]
    termination_date: Optional[date]
    properties: OrderedDict[str, Any]
    geometry: Geometry
    processor_path: Sequence[
        tuple[str, str]
    ]  # この要素に至るまでに使われた (processor.id, gml:id) のリスト


@dataclass
class ParseSettings:
    load_semantic_parts: bool = False  # 部分要素 (e.g. Road > TrafficArea) を読み込むかどうか
    only_highest_lod: bool = False  # 各地物の最高の LOD だけ出力するかどうか
