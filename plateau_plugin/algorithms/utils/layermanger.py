"""Vector layer manager for 'load_vector' algorithm"""

# Copyright (C) 2023 MLIT Japan
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

from __future__ import annotations

from typing import Iterable

from PyQt5.QtCore import QVariant
from qgis._3d import QgsPolygon3DSymbol, QgsVectorLayer3DRenderer
from qgis.core import (
    Qgis,
    QgsCoordinateReferenceSystem,
    QgsField,
    # QgsLayerTreeGroup,
    QgsProject,
    QgsVectorLayer,
    QgsWkbTypes,
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
    "[]double": QVariant.String,  # Comma-separated string
    "object": QVariant.String,  # JSON string
    "[]object": QVariant.String,  # JSON string
    "xAL": QVariant.String,  # JSON string
}


class LayerManager:
    """Featureの種類とLoDをもとにふさわしい出力先レイヤを返すためのユーティリティ"""

    def __init__(
        self,
        force2d: bool,
        crs: QgsCoordinateReferenceSystem,
        append_mode: bool,
        lod_in_name: bool,
        project: QgsProject,
    ):
        self._layers: dict[str, QgsVectorLayer] = {}
        self._parent_map: dict[str, str] = {}
        self._force2d = force2d
        self._crs = crs
        self._lod_in_name = lod_in_name
        self._append_mode = append_mode
        self._project = project

    def get_layer(self, cityobj: CityObject) -> QgsVectorLayer:
        """Featureの種類とLoDをもとにふさわしい出力レイヤを取得する"""

        layer_id = self._get_layer_id(cityobj)
        # if already exists
        if (layer := self._layers.get(layer_id)) is not None:
            return layer

        if self._append_mode:
            # プロジェクト中に存在する同名の既存レイヤに追記する
            layer_name = self._get_layer_name(cityobj)
            for layer in self._project.mapLayersByName(layer_name):
                # 既存レイヤに追記できる条件:
                # 見つかったレイヤがベクタレイヤ かつ
                # ジオメトリ型が一致する かつ
                # CRSが一致する (または NoGeometry 型である)
                geom_type_name = self._get_geometry_type_name(cityobj)
                if isinstance(layer, QgsVectorLayer) and (
                    QgsWkbTypes.displayString(layer.wkbType()) == geom_type_name
                    and (geom_type_name == "NoGeometry" or layer.crs() == self._crs)
                ):
                    self._layers[layer_id] = layer
                    return layer

        return self._add_new_layer(layer_id, cityobj)

    def _subclass_name(self, cityobj: CityObject) -> str:
        """特定の種類において、属性値に応じて恣意的にレイヤを分けるための副分類名を返す"""
        _type = cityobj.type
        if (  # 建物の災害リスク情報を 'description' と 'scale' 属性にもとづいてレイヤ分けする
            _type == "uro:BuildingRiverFloodingRiskAttribute"
            or _type == "uro:BuildingTsunamiRiskAttribute"
            or _type == "uro:BuildingLandSlideRiskAttribute"
        ):
            s = ""
            if desc := cityobj.attributes.get("description"):
                s += desc
            if scale := cityobj.attributes.get("scale"):
                s += " " + scale
            return s.strip()

        return ""

    def _get_layer_id(self, cityobj: CityObject) -> str:
        """Featureの挿入先を決めるレイヤ識別子を CityObject をもとに組み立てる"""
        co: CityObject | None = cityobj
        s = []
        while co:
            s.append(co.processor.id)
            co = co.parent
        name = " / ".join(reversed(s))
        if cityobj.lod is not None:
            assert cityobj.geometry is not None
            if self._lod_in_name:
                name += f":LoD={cityobj.lod})"
            name += f":type={self._get_geometry_type_name(cityobj)}"
        if subclass := self._subclass_name(cityobj):
            name += ":subclass=" + subclass
        return name

    def _get_layer_name(self, cityobj: CityObject) -> str:
        """レイヤ名を組み立てる"""
        co: CityObject | None = cityobj
        s = []
        while co:
            s.append(co.processor.name)
            co = co.parent
        name = " / ".join(reversed(s))
        if (cityobj.lod is not None) and self._lod_in_name:
            name += f" (LoD{cityobj.lod})"
        if subclass := self._subclass_name(cityobj):
            name += " " + subclass
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

        # Prepare basic fields
        attributes.extend(
            [
                QgsField("source", QVariant.String),  # source file name
                QgsField("type", QVariant.String),  # feature type
                QgsField("lod", QVariant.Int),  # LoD
                QgsField("name", QVariant.String),  # gml:name
                QgsField("description", QVariant.String),  # gml:description
                QgsField("creationDate", QVariant.Date),  # gml:creationDate
                QgsField("terminationDate", QVariant.Date),  # gml:terminationDate
            ]
        )
        table_def = get_table_definition(cityobj)
        for field in table_def.fields:
            attributes.append(QgsField(field.name, _TYPE_TO_QT_TYPE[field.datatype]))

        # make a new layer
        crs = self._crs.authid()
        geometry_type_name = self._get_geometry_type_name(cityobj)
        layer_path = f"{geometry_type_name}?crs={crs}&index=yes"

        layer = QgsVectorLayer(
            layer_path,
            self._get_layer_name(cityobj),
            "memory",
        )
        dp = layer.dataProvider()
        dp.addAttributes(attributes)
        self._layers[layer_id] = layer

        # set a default 3d renderer
        try:
            symbol = QgsPolygon3DSymbol()
            symbol.setAltitudeClamping(Qgis.AltitudeClamping.Absolute)  # type: ignore
            symbol.setAltitudeBinding(Qgis.AltitudeBinding.Vertex)  # type: ignore
            renderer = QgsVectorLayer3DRenderer()
            renderer.setSymbol(symbol)
            layer.setRenderer3D(renderer)
        except Exception:
            pass

        return layer

    @property
    def layers(self) -> Iterable[QgsVectorLayer]:
        return self._layers.values()

    # def _make_joins(self):
    #     """子Feature->親Featureのテーブル結合を生成する"""
    #     for layer_id, parent_id in self._parent_map.items():
    #         layer = self._layers.get(layer_id)
    #         parent_layer = self._layers.get(parent_id)
    #         if layer is None or parent_layer is None:
    #             continue
    #         join = QgsVectorLayerJoinInfo()
    #         join.setJoinLayerId(parent_layer.id())
    #         join.setJoinLayer(parent_layer)
    #         join.setJoinFieldName("id")
    #         join.setTargetFieldName("parent")
    #         join.setUsingMemoryCache(True)
    #         layer.addJoin(join)
