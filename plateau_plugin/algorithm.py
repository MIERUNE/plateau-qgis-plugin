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
from typing import Any, Iterable

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

from .geometry import to_qgis_geometry
from .plateau.models import processors
from .plateau.parser import FileParser, ParseSettings
from .plateau.types import CityObject, MultiPolygon

_TYPE_TO_QT_TYPE = {
    "string": QVariant.String,
    "double": QVariant.Double,
    "integer": QVariant.Int,
    "boolean": QVariant.Bool,
    "date": QVariant.Date,
    "[]string": QVariant.StringList,
}


def _convert_to_qt_value(v: Any):
    if isinstance(v, datetime.date):
        return QDate(v.year, v.month, v.day)
    else:
        return v


class LayerManager:
    """地物の種類とLODをもとにふさわしい出力先レイヤを返すためのユーティリティ"""

    def __init__(self):
        self._layers: dict[str, QgsVectorLayer] = {}
        self._parent_map: dict[str, str] = {}

    def get_layer(self, cityobj: CityObject) -> QgsVectorLayer:
        """地物の種類とLODをもとにふさわしい出力レイヤを取得する"""

        # レイヤ名を決定
        # TODO: レイヤの名前を識別子として使わないほうがよいだろう
        layer_name = " / ".join(p[0] for p in cityobj.processor_path)
        if cityobj.lod is not None:
            layer_name += f" (LOD{cityobj.lod})"

        if (layer := self._layers.get(layer_name)) is not None:
            # if already exists
            return layer

        return self._add_new_layer(layer_name, cityobj)

    def _add_new_layer(self, layer_name: str, cityobj: CityObject) -> QgsVectorLayer:
        """新たなレイヤを作る"""

        if len(cityobj.processor_path) > 1:
            parent_layer_name = " / ".join(p[0] for p in cityobj.processor_path[:-1])
            self._parent_map[layer_name] = parent_layer_name

        # setup attributes
        attributes = [
            QgsField("id", QVariant.String),
        ]
        if len(cityobj.processor_path) > 1:
            attributes.append(QgsField("parent", QVariant.String))
        attributes.extend(
            [
                QgsField("type", QVariant.String),
                QgsField("name", QVariant.String),
                QgsField("creationDate", QVariant.Date),
                QgsField("terminationDate", QVariant.Date),
            ]
        )
        table_def = processors.get_table_definition(cityobj.processor_path)
        for field in table_def.fields:
            attributes.append(QgsField(field.name, _TYPE_TO_QT_TYPE[field.datatype]))

        # make a new layer
        if isinstance(cityobj.geometry, MultiPolygon):
            layer_path = "MultiPolygonZ?crs=epsg:6697"
        elif cityobj.geometry is None:
            layer_path = "NoGeometry"
        else:
            raise RuntimeError(f"Unsupported geometry type: {type(cityobj.geometry)}")
        layer = QgsVectorLayer(
            layer_path,
            layer_name,
            "memory",
        )
        dp = layer.dataProvider()
        dp.addAttributes(attributes)
        self._layers[layer_name] = layer
        return layer

    def add_to_project(self, feedback):
        """レイヤをプロジェクトに追加する"""
        for layer in self._layers.values():
            layer.updateFields()
        QgsProject.instance().addMapLayers(self._layers.values(), True)
        # グループを作る?
        # QgsProject.instance().addMapLayers(layers.layers(), False)
        # group = QgsProject.instance().layerTreeRoot().addGroup(Path(filename).stem)
        self._make_joins(feedback)

    def _make_joins(self, feedback):
        """子地物->親地物のテーブル結合を生成する"""
        for layer_id, parent_id in self._parent_map.items():
            layer = self._layers.get(layer_id)
            parent_layer = self._layers.get(parent_id)
            feedback.pushInfo(f"Joining {layer} to {parent_layer}")
            if layer is None or parent_layer is None:
                continue
            join = QgsVectorLayerJoinInfo()
            join.setJoinLayerId(parent_layer.id())
            join.setJoinLayer(parent_layer)
            join.setJoinFieldName("id")
            join.setTargetFieldName("parent")
            join.setUsingMemoryCache(True)
            layer.addJoin(join)


class PlateauProcessingAlrogithm(QgsProcessingAlgorithm):
    """Processing algorithm for loading PLATEAU 3D City models into QGIS"""

    INPUT = "INPUT"
    ONLY_HIGHEST_LOD = "ONLY_HIGHEST_LOD"
    LOAD_SEMANTIC_PARTS = "LOAD_SEMANTIC_PARTS"

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
                self.tr("各地物の最高 LOD のみを読み込む"),
                defaultValue=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.LOAD_SEMANTIC_PARTS,
                self.tr("部分要素に分けて読み込む"),
                defaultValue=False,
            )
        )

    def createInstance(self):
        return PlateauProcessingAlrogithm()

    def name(self):
        return "plateau_plugin"

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
        # Prepare field definition
        layers = LayerManager()

        parser = self._make_parser(parameters, context)
        total_count = parser.count_toplevel_cityobjs()
        feedback.pushInfo(f"{total_count}個のトップレベル地物が含まれています。")
        feedback.pushInfo("地物を読み込んでいます...")
        top_level_count = 0
        count = 0
        try:
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
                if len(cityobj.processor_path) > 1:
                    # 親地物と結合 (join) できるように親地物の ID を持たせる
                    feature.setAttribute("parent", cityobj.processor_path[-2][1])

                for name, value in cityobj.properties.items():
                    feature.setAttribute(name, _convert_to_qt_value(value))

                # Set geometry
                if cityobj.geometry:
                    feature.setGeometry(to_qgis_geometry(cityobj.geometry))

                provider.addFeature(feature)
                count += 1
                if count % 100 == 0:
                    feedback.setProgress(top_level_count / total_count * 100)
                    feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        except ValueError:
            feedback.reportError(
                "ファイルの読み込みに失敗しました。正常なファイルかどうか確認してください。", fatalError=True
            )

        feedback.pushInfo(f"{count} 個の地物を読み込みました。")
        layers.add_to_project(feedback)

        return {}
