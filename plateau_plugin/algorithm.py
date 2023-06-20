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
)

from .geometry import to_qgis_geometry
from .plateau.models import processors
from .plateau.parser import FileParser
from .plateau.types import CityObject, MultiPolygon, ParseSettings

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
    """地物の種類とLODをもとにふさわしい出力レイヤを取得する"""

    def __init__(self):
        self._layers: dict[str, QgsVectorLayer] = {}

    def get_layer(self, cityobj: CityObject) -> QgsVectorLayer:
        # layer name
        layer_name = " / ".join(p[0] for p in cityobj.processor_path)
        if cityobj.lod is not None:
            layer_name += f" (LOD{cityobj.lod})"

        if (layer := self._layers.get(layer_name)) is not None:
            # already exists
            return layer

        # prepare new layer
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
        provider = layer.dataProvider()
        attributes = [
            QgsField("id", QVariant.String),
            QgsField("type", QVariant.String),
            QgsField("name", QVariant.String),
            QgsField("creationDate", QVariant.Date),
            QgsField("terminationDate", QVariant.Date),
        ]
        table_def = processors.get_table_definition(cityobj.processor_path)
        for field in table_def.fields:
            attributes.append(QgsField(field.name, _TYPE_TO_QT_TYPE[field.datatype]))
        provider.addAttributes(attributes)
        self._layers[layer_name] = layer
        return layer

    def layers(self) -> Iterable[QgsVectorLayer]:
        return self._layers.values()


class PlateauProcessingAlrogithm(QgsProcessingAlgorithm):
    """Processing algorithm for converting PLATEAU 3D City models"""

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
        return self.tr("3D都市モデルを読み込む")

    def shortHelpString(self) -> str:
        return self.tr("PLATEAU PLATEAU PLATEAU")

    def _make_parser(self, parameters, context) -> FileParser:
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
        total_count = parser.count_toplevel_objects()
        feedback.pushInfo(f"{total_count}個のトップレベル地物が含まれています。")
        feedback.pushInfo("地物を読み込んでいます...")
        top_level_count = 0
        count = 0
        try:
            for top_level_count, cityobj in parser.iter_city_objects():
                if feedback.isCanceled():
                    return {}

                layer = layers.get_layer(cityobj)
                dp = layer.dataProvider()
                dest_feat = QgsFeature(dp.fields())
                dest_feat.setAttribute("id", cityobj.id)
                dest_feat.setAttribute("name", cityobj.name)
                dest_feat.setAttribute("type", cityobj.type)
                dest_feat.setAttribute(
                    "creationDate",
                    QDate(cityobj.creation_date) if cityobj.creation_date else None,  # type: ignore
                )
                dest_feat.setAttribute(
                    "terminationDate",
                    QDate(cityobj.creation_date) if cityobj.creation_date else None,  # type: ignore
                )
                for name, value in cityobj.properties.items():
                    dest_feat.setAttribute(name, _convert_to_qt_value(value))

                if cityobj.geometry:
                    dest_feat.setGeometry(to_qgis_geometry(cityobj.geometry))

                dp.addFeature(dest_feat)
                count += 1
                if count % 100 == 0:
                    feedback.setProgress(top_level_count / total_count * 100)
                    feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        except ValueError:
            feedback.reportError(
                "ファイルの読み込みに失敗しました。正常なファイルかどうか確認してください。", fatalError=True
            )

        feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        for layer in layers.layers():
            layer.updateFields()

        QgsProject.instance().addMapLayers(layers.layers(), True)
        # QgsProject.instance().addMapLayers(layers.layers(), False)
        # group = QgsProject.instance().layerTreeRoot().addGroup(Path(filename).stem)

        return {}
