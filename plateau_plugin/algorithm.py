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

from typing import Iterable

from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (
    QgsFeature,
    QgsField,
    # QgsLayerTreeGroup,
    QgsProcessingAlgorithm,
    QgsProcessingException,  # pyright: ignore
    QgsProcessingParameterFile,
    QgsProject,
    QgsVectorLayer,
)

from .geometry import to_qgis_geometry
from .plateau.models import processors
from .plateau.parser import FileParser
from .plateau.types import CityObject, MultiPolygon

_TYPE_TO_QT_TYPE = {
    "string": QVariant.String,
    "double": QVariant.Double,
    "integer": QVariant.Int,
    "date": QVariant.Date,
    "[]string": QVariant.StringList,
}


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
    SEMANTIC_PARTS = "SEMANTIC_PARTS"
    # OUTPUT = "OUTPUT"

    def tr(self, string: str):
        return QCoreApplication.translate("Processing", string)

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("PLATEAU GMLファイル"),
                fileFilter=self.tr("PLATEAU GML ファイル (*.gml)"),
            )
        )
        # self.addParameter(
        #     QgsProcessingParameterFeatureSink(
        #         self.OUTPUT,
        #         self.tr("出力レイヤ"),
        #         QgsProcessing.TypeVectorPolygon,
        #     )
        # )

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

    def processAlgorithm(self, parameters, context, feedback):
        # Prepare field definition
        layers = LayerManager()

        filename = self.parameterAsFile(parameters, self.INPUT, context)
        if filename is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )  # pragma: no cover

        parser = FileParser(filename)
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
                fields = layer.dataProvider().fields()
                dest_feat = QgsFeature(fields)
                if cityobj.geometry:
                    dest_geoms = to_qgis_geometry(cityobj.geometry)
                    dest_feat.setGeometry(dest_geoms)
                for name, value in cityobj.properties.items():
                    dest_feat.setAttribute(name, value)
                dest_feat.setAttribute("type", cityobj.type)
                layer.dataProvider().addFeature(dest_feat)

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
