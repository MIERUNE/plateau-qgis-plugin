"""Processing algorithm for converting plateau files"""

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

import datetime
import json
from typing import Any, Optional

from PyQt5.QtCore import QCoreApplication, QDate, QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    # QgsLayerTreeGroup,
    QgsProcessingAlgorithm,
    QgsProcessingException,  # pyright: ignore
    QgsProcessingParameterBoolean,
    QgsProcessingParameterFile,
    QgsProject,
    QgsVectorLayer,
    QgsVectorLayerJoinInfo,
)

from ..geometry import to_qgis_geometry
from ..plateau.parser import FileParser, ParseSettings
from ..plateau.types import (
    CityObject,
    LineStringCollection,
    PointCollection,
    PolygonCollection,
    get_geometry_type_name,
    get_table_definition,
)

_TYPE_TO_QT_TYPE = {
    "string": QVariant.String,
    "double": QVariant.Double,
    "integer": QVariant.Int,
    "boolean": QVariant.Bool,
    "date": QVariant.Date,
    "[]string": QVariant.StringList,
    "object": QVariant.String,  # JSON string
    "[]object": QVariant.String,  # JSON string
}


def _convert_to_qt_value(v: Any):
    if isinstance(v, list):
        if not v:
            return []

        if isinstance(v[0], str):
            return v
        else:
            return json.dumps(v, ensure_ascii=False)
    else:
        # not a list
        if isinstance(v, dict):
            return json.dumps(v, ensure_ascii=False)
        elif isinstance(v, datetime.date):
            return QDate(v.year, v.month, v.day)
        else:
            return v


class LayerManager:
    """Featureの種類とLoDをもとにふさわしい出力先レイヤを返すためのユーティリティ"""

    def __init__(self, is3d: bool):
        self._layers: dict[str, QgsVectorLayer] = {}
        self._parent_map: dict[str, str] = {}
        self._is3d = is3d

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
            name += (
                f":LoD={cityobj.lod}):type={get_geometry_type_name(cityobj.geometry)}"
            )
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
                QgsField("name", QVariant.String),
                QgsField("creationDate", QVariant.Date),
                QgsField("terminationDate", QVariant.Date),
            ]
        )
        table_def = get_table_definition(cityobj)
        for field in table_def.fields:
            attributes.append(QgsField(field.name, _TYPE_TO_QT_TYPE[field.datatype]))

        # make a new layer
        _z_suffix = "Z" if self._is3d else ""
        if isinstance(cityobj.geometry, PolygonCollection):
            layer_path = f"MultiPolygon{_z_suffix}?crs=epsg:6697"
        elif isinstance(cityobj.geometry, LineStringCollection):
            layer_path = f"MultiLineString{_z_suffix}?crs=epsg:6697"
        elif isinstance(cityobj.geometry, PointCollection):
            layer_path = f"MultiPoint{_z_suffix}?crs=epsg:6697"
        elif cityobj.geometry is None:
            layer_path = "NoGeometry"
        else:
            raise RuntimeError(f"Unsupported geometry type: {type(cityobj.geometry)}")

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


class PlateauVectorLoaderAlrogithm(QgsProcessingAlgorithm):
    """Processing algorithm to load PLATEAU 3D City models as vector layers"""

    INPUT = "INPUT"
    ONLY_HIGHEST_LOD = "ONLY_HIGHEST_LOD"
    LOAD_SEMANTIC_PARTS = "LOAD_SEMANTIC_PARTS"
    FORCE_2D = "FORCE_2D"

    def tr(self, string: str):
        return QCoreApplication.translate("Processing", string)

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("PLATEAU CityGML ファイル"),
                fileFilter=self.tr("PLATEAU CityGML ファイル (*.gml)"),
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ONLY_HIGHEST_LOD,
                self.tr("各地物の最高 LoD のみを読み込む"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_SEMANTIC_PARTS,
                self.tr("意味的子要素に分けて読み込む"),
                defaultValue=False,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FORCE_2D,
                self.tr("2次元データとして読み込む"),
                defaultValue=False,
            )
        )

    def createInstance(self):
        return PlateauVectorLoaderAlrogithm()

    def name(self):
        return "load_as_vector"

    def group(self):
        return None

    def groupId(self):
        return None

    def displayName(self):
        return self.tr("PLATEAU 3D都市モデルを読み込む")

    def shortHelpString(self) -> str:
        return self.tr("PLATEAU PLATEAU PLATEAU")

    def _make_parser(self, parameters, context) -> FileParser:
        """プロセシングの設定をもとにパーサを作る"""
        load_semantic_parts = self.parameterAsBoolean(
            parameters, self.LOAD_SEMANTIC_PARTS, context
        )
        only_highest_lod = self.parameterAsBoolean(
            parameters, self.ONLY_HIGHEST_LOD, context
        )
        settings = ParseSettings(
            load_semantic_parts=load_semantic_parts,
            only_highest_lod=only_highest_lod,
        )

        filename = self.parameterAsFile(parameters, self.INPUT, context)
        if filename is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )  # pragma: no cover

        return FileParser(filename, settings)

    def processAlgorithm(self, parameters, context, feedback):
        is3d = not self.parameterAsBoolean(parameters, self.FORCE_2D, context)
        layers = LayerManager(is3d=is3d)

        parser = self._make_parser(parameters, context)
        total_count = parser.count_toplevel_cityobjs()
        feedback.pushInfo(f"{total_count}個のトップレベル都市オブジェクトが含まれています。")
        feedback.pushInfo("都市オブジェクトを読み込んでいます...")
        top_level_count = 0
        count = 0

        # NOTE: 例外のハンドリングはプロセッシングフレームワークに任せている
        for top_level_count, cityobj in parser.iter_cityobjs():
            if feedback.isCanceled():
                return {}

            layer = layers.get_layer(cityobj)
            provider = layer.dataProvider()
            feature = QgsFeature(provider.fields())

            # Set attributes
            feature.setAttribute("id", cityobj.id)
            feature.setAttribute("type", cityobj.type)
            feature.setAttribute("name", cityobj.name)
            feature.setAttribute(
                "creationDate",
                QDate(cityobj.creation_date) if cityobj.creation_date else None,  # type: ignore
            )
            feature.setAttribute(
                "terminationDate",
                QDate(cityobj.creation_date) if cityobj.termination_date else None,  # type: ignore
            )
            if cityobj.parent:
                # 親Featureと結合 (join) できるように親Featureの ID を持たせる
                feature.setAttribute("parent", cityobj.parent.id)

            for name, value in cityobj.attributes.items():
                feature.setAttribute(name, _convert_to_qt_value(value))

            # Set geometry
            if cityobj.geometry:
                feature.setGeometry(to_qgis_geometry(cityobj.geometry, is3d=is3d))

            provider.addFeature(feature)
            count += 1
            if count % 100 == 0:
                feedback.setProgress(top_level_count / total_count * 100)
                feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        feedback.pushInfo(f"{count} 個の地物を読み込みました。")
        layers.add_to_project()

        return {}
