"""Vector layer manager for 'load_vector' algorithm"""

# Copyright (C) 2023 MIERUNE Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from typing import Optional

from PyQt5.QtCore import QVariant
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsField,
    # QgsLayerTreeGroup,
    QgsProject,
    QgsVectorLayer,
    QgsVectorLayerJoinInfo,
)

from ...plateau.types import (
    CityObject,
    LineStringCollection,
    PointCollection,
    PolygonCollection,
    get_table_definition,
)

_TYPE_TO_QT_TYPE = {
    "string": QVariant.String,
    "double": QVariant.Double,
    "integer": QVariant.Int,
    "boolean": QVariant.Bool,
    "date": QVariant.Date,
    "[]string": QVariant.String,  # Comma-separated string
    "object": QVariant.String,  # JSON string
    "[]object": QVariant.String,  # JSON string
    "xAL": QVariant.String,  # JSON string
}


class LayerManager:
    """Featureの種類とLoDをもとにふさわしい出力先レイヤを返すためのユーティリティ"""

    def __init__(self, force2d: bool, crs: QgsCoordinateReferenceSystem):
        self._layers: dict[str, QgsVectorLayer] = {}
        self._parent_map: dict[str, str] = {}
        self._force2d = force2d
        self._crs = crs

    def get_layer(self, cityobj: CityObject) -> QgsVectorLayer:
        """Featureの種類とLoDをもとにふさわしい出力レイヤを取得する"""

        layer_id = self._get_layer_id(cityobj)
        if (layer := self._layers.get(layer_id)) is not None:
            # if already exists
            return layer

        return self._add_new_layer(layer_id, cityobj)

    def _get_layer_id(self, cityobj: CityObject) -> str:
        co: Optional[CityObject] = cityobj
        s = []
        while co:
            s.append(co.processor.id)
            co = co.parent
        name = " / ".join(reversed(s))
        if cityobj.lod is not None:
            assert cityobj.geometry is not None
            name += f":LoD={cityobj.lod}):type={self._get_geometry_type_name(cityobj)}"
        return name

    def _get_layer_name(self, cityobj: CityObject) -> str:
        co: Optional[CityObject] = cityobj
        s = []
        while co:
            s.append(co.processor.name)
            co = co.parent
        name = " / ".join(reversed(s))
        if cityobj.lod is not None:
            name += f" (LoD{cityobj.lod})"
        return name

    def _get_geometry_type_name(self, cityobj: CityObject):
        as2d = False
        if cityobj.lod is not None:
            lod_def = cityobj.processor.lod_list[cityobj.lod]
            if lod_def:
                as2d = self._force2d or lod_def.is2d

        _z_suffix = "" if as2d else "Z"
        geometry = cityobj.geometry
        if geometry is None:
            return "NoGeometry"
        if isinstance(geometry, PolygonCollection):
            return "MultiPolygon" + _z_suffix
        elif isinstance(geometry, LineStringCollection):
            return "MultiLineString" + _z_suffix
        elif isinstance(geometry, PointCollection):
            return "MultiPoint" + _z_suffix
        else:
            raise NotImplementedError(
                f"Geometry type {type(geometry)} is not implemented."
            )

    def _add_new_layer(self, layer_id: str, cityobj: CityObject) -> QgsVectorLayer:
        """新たなレイヤを作る"""

        # setup attributes
        attributes = [
            QgsField("id", QVariant.String),
        ]

        if cityobj.parent:
            parent_layer_id = self._get_layer_id(cityobj.parent)
            self._parent_map[layer_id] = parent_layer_id
            attributes.append(QgsField("parent", QVariant.String))

        attributes.extend(
            [
                QgsField("type", QVariant.String),
                QgsField("lod", QVariant.Int),
                QgsField("name", QVariant.String),
                QgsField("creationDate", QVariant.Date),
                QgsField("terminationDate", QVariant.Date),
            ]
        )
        table_def = get_table_definition(cityobj)
        for field in table_def.fields:
            attributes.append(QgsField(field.name, _TYPE_TO_QT_TYPE[field.datatype]))

        # make a new layer
        crs = self._crs.authid()
        geometry_type_name = self._get_geometry_type_name(cityobj)
        layer_path = f"{geometry_type_name}?crs={crs}"

        layer = QgsVectorLayer(
            layer_path,
            self._get_layer_name(cityobj),
            "memory",
        )
        dp = layer.dataProvider()
        dp.addAttributes(attributes)
        self._layers[layer_id] = layer
        return layer

    def add_to_project(self):
        """レイヤをプロジェクトに追加する"""
        for layer in self._layers.values():
            layer.updateFields()
        QgsProject.instance().addMapLayers(self._layers.values(), True)
        # グループを作る?
        # QgsProject.instance().addMapLayers(layers.layers(), False)
        # group = QgsProject.instance().layerTreeRoot().addGroup(Path(filename).stem)
        self._make_joins()

    def _make_joins(self):
        """子Feature->親Featureのテーブル結合を生成する"""
        for layer_id, parent_id in self._parent_map.items():
            layer = self._layers.get(layer_id)
            parent_layer = self._layers.get(parent_id)
            if layer is None or parent_layer is None:
                continue
            join = QgsVectorLayerJoinInfo()
            join.setJoinLayerId(parent_layer.id())
            join.setJoinLayer(parent_layer)
            join.setJoinFieldName("id")
            join.setTargetFieldName("parent")
            join.setUsingMemoryCache(True)
            layer.addJoin(join)
