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


Geometry = Union[MultiPolygon, MultiLineString, MultiPoint]


@dataclass
class CityObject:
    """都市オブジェクト (地物) を表す"""

    lod: Literal[0, 1, 2, 3, 4, None]
    """LOD (0, 1, 2, 3, 4) または None (ジオメトリなし)"""

    type: str
    """この地物の型名 (e.g. tran:Road, tran:TrafficArea, etc.)"""

    id: str
    """@gml:id"""

    name: Optional[str]
    """gml:name"""

    creation_date: Optional[date]
    """core:creationDate"""

    termination_date: Optional[date]
    """core:terminationDate"""

    attributes: OrderedDict[str, Any]
    """地物のプロパティ値"""

    geometry: Optional[Geometry]
    """地物のジオメトリ"""

    processor_path: Sequence[tuple[str, str]]
    """この要素に至るまでに使われた (processor.id, gml:id) のリスト"""
