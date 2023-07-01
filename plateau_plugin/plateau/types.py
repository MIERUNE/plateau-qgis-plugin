from collections import OrderedDict
from dataclasses import dataclass
from datetime import date
from typing import Any, Literal, Optional, Union

import numpy as np

from .models.base import FeatureProcessingDefinition, PropertyDatatype


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


def get_geometry_type_name(geometry: Geometry):
    if isinstance(geometry, MultiPolygon):
        return "MultiPolygon"
    elif isinstance(geometry, MultiLineString):
        return "MultiLineString"
    elif isinstance(geometry, MultiPoint):
        return "MultiPoint"
    else:
        raise NotImplementedError(f"Geometry type {type(geometry)} is not implemented.")


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

    processor: FeatureProcessingDefinition

    parent: Optional["CityObject"]
    """親のCityObject"""


@dataclass
class FieldDefinition:
    """QGIS 等にテーブルを作る際のフィールド定義"""

    name: str
    datatype: PropertyDatatype


@dataclass
class TableDefinition:
    """QGIS 等にテーブルを作る際のテーブル定義"""

    fields: list[FieldDefinition]


def get_table_definition(cityobj: CityObject):
    processor = cityobj.processor
    fields = [
        FieldDefinition("id", "string"),
        FieldDefinition("type", "string"),
        FieldDefinition("name", "string"),
        FieldDefinition("creationDate", "date"),
        FieldDefinition("terminationDate", "date"),
    ]
    if processor.load_generic_attributes:
        fields.append(FieldDefinition("generic", "object"))
    closed: dict[str, str] = {}
    for group in processor.attribute_groups:
        for prop in group.attributes:
            if prop.name not in closed:
                fields.append(FieldDefinition(prop.name, prop.datatype))
                closed[prop.name] = prop.datatype
            else:
                # 同名のフィールドが既にある場合は、型が一致しているか確認する
                assert (
                    closed[prop.name] == prop.datatype
                ), f"{prop.name}, {closed[prop.name]} != {prop.datatype}"

    return TableDefinition(fields=fields)
