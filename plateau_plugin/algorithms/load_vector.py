"""Processing algorithm for loading the PLATEAU CityGML as vector layers"""

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

import datetime
import json
import platform
from pathlib import Path
from typing import Any

from PyQt5.QtCore import QCoreApplication, QDate
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsFeatureSink,
    # QgsLayerTreeGroup,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,  # pyright: ignore
    QgsProcessingFeedback,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingUtils,
    QgsProject,
)

from ..geometry import to_qgis_geometry
from ..plateau.parse import ParserSettings, PlateauCityGmlParser
from .utils.layermanger import LayerManager


def _convert_to_qt_value(v: Any) -> Any:
    if isinstance(v, list):
        if not v:
            return None
        elif isinstance(v[0], (str, float, int)):
            return ",".join(str(e) for e in v)
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


_LOD_OPTIONS = {
    0: {
        "label": "最も単純なLODのみを読み込む",
        "prefer_lowest": True,
        "only_first": True,
    },
    1: {
        "label": "最も詳細なLODのみを読み込む",
        "prefer_lowest": False,
        "only_first": True,
    },
    2: {"label": "全てのLODを読み込む", "prefer_lowest": False, "only_first": False},
}

_DESCRIPTION = """3D都市モデル標準製品仕様書 第3.0版に対応した、PLATEAU 3D都市モデルのCityGML (.gml) ファイルを読み込みます。

データは一時スクラッチレイヤに読み込まれます。

同一の都市オブジェクトに複数のLOD (詳細度) が用意されている場合は、デフォルトでは最も単純なLODのみを読み込みます。必要に応じて、"読み込むLOD" オプションで「最も詳細なLODのみを読み込む」または「全てのLODを読み込む」を選択してください。

「地物を構成する部分ごとにレイヤを分ける」を有効にすると、一部のモデルのLOD2以上において、壁や屋根、車道や歩道といった意味論的な子要素ごとにレイヤを分けて地物を読み込みます。このオプションを有効にすると地物の数が大幅に増える可能性があります。

「3Dデータを強制的に平面化する」を有効にすると、3次元の情報を捨てて平面データとして読み込みます。高さをもたないモデル (都市計画決定情報など) はこのオプションにかかわらず常に平面として読み込みます。
"""


class PlateauVectorLoaderAlrogithm(QgsProcessingAlgorithm):
    """Processing algorithm to load PLATEAU 3D City models as vector layers"""

    INPUT = "INPUT"
    SEMANTIC_PARTS = "SEMANTIC_PARTS"
    LOD_PREFERENCE = "LOD_PREFERENCE"
    FORCE_2D = "FORCE_2D"
    APPEND_MODE = "APPEND_MODE"
    CRS = "CRS"

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
            QgsProcessingParameterEnum(
                self.LOD_PREFERENCE,
                self.tr("読み込むLOD"),
                options=[v["label"] for v in _LOD_OPTIONS.values()],
                defaultValue=0,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.SEMANTIC_PARTS,
                self.tr("地物を構成する部分ごとにレイヤを分ける"),
                defaultValue=False,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.FORCE_2D,
                self.tr("3次元データを強制的に2次元化する"),
                defaultValue=False,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.APPEND_MODE,
                self.tr("既存の同名レイヤに追記する"),
                defaultValue=True,
                optional=True,
            )
        )
        self.addParameter(
            QgsProcessingParameterCrs(
                self.CRS,
                self.tr("変換先CRS"),
                defaultValue="EPSG:6668",
                optional=True,
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
        return self.tr(_DESCRIPTION)

    def _make_parser(
        self, filename: str, parameters, context, lod_option
    ) -> PlateauCityGmlParser:
        """プロセシングの設定をもとにパーサを作る"""
        load_semantic_parts = self.parameterAsBoolean(
            parameters, self.SEMANTIC_PARTS, context
        )
        settings = ParserSettings(
            load_semantic_parts=load_semantic_parts,
            target_lods=(False, True, True, True, True),
            only_first_found_lod=lod_option["only_first"],
            lowest_lod_first=lod_option["prefer_lowest"],
        )

        if filename is None:
            raise QgsProcessingException(
                self.invalidSourceError(parameters, self.INPUT)
            )  # pragma: no cover
        return PlateauCityGmlParser(filename, settings)

    def flags(self) -> QgsProcessingAlgorithm.Flags:
        if platform.system() == "Windows":
            # NOTE: Windowsでバッチ処理が停止する問題への暫定対応としてメインスレッドで実行する
            return super().flags() | QgsProcessingAlgorithm.FlagNoThreading
        else:
            return super().flags()

    def processAlgorithm(  # noqa: C901
        self,
        parameters: dict[str, Any],
        context: QgsProcessingContext,
        feedback: QgsProcessingFeedback,
    ):
        destination_crs = self.parameterAsCrs(parameters, self.CRS, context)
        force2d = self.parameterAsBoolean(parameters, self.FORCE_2D, context)
        append_mode = self.parameterAsBoolean(parameters, self.APPEND_MODE, context)
        lod_option = _LOD_OPTIONS[
            self.parameterAsEnum(parameters, self.LOD_PREFERENCE, context)
        ]
        layer_manager = LayerManager(
            force2d=force2d,
            crs=destination_crs,
            append_mode=append_mode,
            lod_in_name=not lod_option["only_first"],
            project=context.project(),
        )
        filename = self.parameterAsFile(parameters, self.INPUT, context)

        parser = self._make_parser(filename, parameters, context, lod_option)
        total_count = parser.count_toplevel_cityobjs()
        feedback.pushInfo(
            f"{total_count}個のトップレベル都市オブジェクトが含まれています。"
        )
        feedback.pushInfo("都市オブジェクトを読み込んでいます...")
        top_level_count = 0
        count = 0

        crs_transform = QgsCoordinateTransform(
            QgsCoordinateReferenceSystem("epsg:6697"),
            destination_crs,
            QgsProject.instance(),
        )

        # NOTE: 例外のハンドリングはプロセッシングフレームワークに任せている
        for top_level_count, cityobj in parser.iter_cityobjs():
            if feedback.isCanceled():
                return {}

            layer = layer_manager.get_layer(cityobj)
            provider = layer.dataProvider()
            feature = QgsFeature(provider.fields())

            # Set attributes
            feature.setAttribute("id", cityobj.id)
            feature.setAttribute("source", Path(filename).stem)
            feature.setAttribute("type", cityobj.type)
            feature.setAttribute("lod", cityobj.lod)
            feature.setAttribute("name", cityobj.name)
            feature.setAttribute("description", cityobj.description)
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

            if cityobj.geometry:
                # Should be treated as 2D?
                as2d = False
                if cityobj.lod is not None:
                    lod_def = cityobj.processor.lod_list[cityobj.lod]
                    if lod_def:
                        as2d = force2d or lod_def.is2d

                # Set geometry
                geom = to_qgis_geometry(cityobj.geometry, as2d=as2d)
                geom.transform(crs_transform, transformZ=False)
                feature.setGeometry(geom)

            provider.addFeature(feature, QgsFeatureSink.FastInsert)
            count += 1
            if count % 100 == 0:
                feedback.setProgress(top_level_count / total_count * 100)
                feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        feedback.pushInfo(f"{count} 個の地物を読み込みました。")

        layers = sorted(layer_manager.layers, key=lambda x: x.name())
        for layer in layers:
            layer.dataProvider().flushBuffer()
            layer.updateFields()
            layer.updateExtents()

            if context.project().mapLayer(layer.id()) is None:
                # まだプロジェクトに追加されていないレイヤのみをプロジェクトに追加する
                context.temporaryLayerStore().addMapLayers([layer])
                context.addLayerToLoadOnCompletion(
                    layer.id(),
                    QgsProcessingContext.LayerDetails(
                        layer.name(),
                        context.project(),
                        layer.name(),
                        QgsProcessingUtils.LayerHint.Vector,  # type: ignore
                    ),
                )
            else:
                pass
                # NOTE: 以下はバッチ処理時に多大なパフォーマンス低下を招くため無効化している
                # 既存レイヤに追記した場合は、背後のプロバイダをリロードする
                # layer.dataProvider().reloadData()

        return {}
