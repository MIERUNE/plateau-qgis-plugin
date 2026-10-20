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
import re
from pathlib import Path
from typing import Any

from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsFeatureSink,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingException,  # pyright: ignore
    QgsProcessingFeedback,
    QgsProcessingLayerPostProcessorInterface,
    QgsProcessingParameterBoolean,
    QgsProcessingParameterCrs,
    QgsProcessingParameterEnum,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingUtils,
    QgsProject,
    QgsProviderRegistry,
    QgsVectorFileWriter,
    QgsVectorLayer,
)
from qgis.PyQt.QtCore import QCoreApplication, QDate

from ..geometry import to_qgis_geometry
from ..plateau.parse import ParserSettings, PlateauCityGmlParser
from .utils.layermanger import LayerManager, set_default_3d_renderer


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

"出力先 GeoPackage" を指定しない場合、データは一時スクラッチレイヤに読み込まれます (QGIS を閉じると消えます)。指定した場合は、レイヤごとに1つのテーブルとして GeoPackage に保存してから読み込みます。

「既存の同名レイヤに追記する」が有効なとき、出力先を指定しない場合はプロジェクト内の同名レイヤに追記します。出力先を指定した場合は、その GeoPackage が既にあれば同名のテーブルに追記します (上書き確認が表示されても、ファイルは置き換えずに追記します)。無効にすると GeoPackage を作り直します。

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
    OUTPUT = "OUTPUT"

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
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT,
                self.tr("出力先 GeoPackage"),
                fileFilter=self.tr("GeoPackage (*.gpkg)"),
                optional=True,
                createByDefault=False,
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
        output_path = self.parameterAsFileOutput(parameters, self.OUTPUT, context)
        if (
            output_path
            and not append_mode
            and any(
                _same_source(lyr, output_path)
                for lyr in context.project().mapLayers().values()
            )
        ):
            # 開いているファイルを作り直すと、読み込み済みのレイヤが古いデータを指したままになる (Windows では削除に失敗する)
            raise QgsProcessingException(
                f"{output_path} はプロジェクトで開かれているため作り直せません。"
                "レイヤを削除してから実行するか、「既存の同名レイヤに追記する」を有効にしてください。"
            )
        lod_option = _LOD_OPTIONS[
            self.parameterAsEnum(parameters, self.LOD_PREFERENCE, context)
        ]
        layer_manager = LayerManager(
            force2d=force2d,
            crs=destination_crs,
            # ファイル出力時は無関係なプロジェクトレイヤに書き込まないよう、プロジェクト内は探さない
            append_mode=append_mode and not output_path,
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
        if output_path:
            _write_to_gpkg(layers, output_path, append_mode, context, feedback)
            return {self.OUTPUT: output_path}

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


class _Renderer3DPostProcessor(QgsProcessingLayerPostProcessorInterface):
    def postProcessLayer(self, layer, context, feedback):
        if isinstance(layer, QgsVectorLayer):
            set_default_3d_renderer(layer)


# NOTE: PostProcessor の所有権は C++ 側に移るが、Python 側の参照が消えて GC されないよう保持しておく
_post_processors: list[_Renderer3DPostProcessor] = []


def _table_name(layer_name: str) -> str:
    """レイヤ名を GeoPackage のテーブル名に使える文字列にする ("|" などは URI を壊すため)"""
    return re.sub(r"\W+", "_", layer_name).strip("_") or "layer"


def _same_source(layer, path: str, table: str | None = None) -> bool:
    """レイヤが GeoPackage (のテーブル) を参照しているか"""
    if layer.providerType() != "ogr":
        return False
    parts = QgsProviderRegistry.instance().decodeUri("ogr", layer.source())
    return Path(parts.get("path", "")).resolve() == Path(path).resolve() and (
        table is None or parts.get("layerName") == table
    )


def _write_to_gpkg(
    layers: list[QgsVectorLayer],
    path: str,
    append_mode: bool,
    context: QgsProcessingContext,
    feedback: QgsProcessingFeedback,
):
    """メモリレイヤを GeoPackage に1テーブルずつ書き出し、読み込み対象に登録する"""
    # ponytail: 全件をメモリに載せてから書き出すため、メモリのピークは一時レイヤと同じ。
    # 問題になったら LayerManager が GeoPackage に直接書き込むようにする
    append = append_mode and Path(path).exists()
    used_tables: set[str] = set()
    for i, layer in enumerate(layers):
        layer.dataProvider().flushBuffer()
        layer.updateFields()
        layer.updateExtents()

        options = QgsVectorFileWriter.SaveVectorOptions()
        options.driverName = "GPKG"
        options.fileEncoding = "UTF-8"
        options.actionOnExistingFile = (
            QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteFile
            if i == 0 and not append
            else QgsVectorFileWriter.ActionOnExistingFile.CreateOrOverwriteLayer
        )

        # 同名のテーブルがあれば、ジオメトリ型と CRS が一致するときだけ追記する。
        # 一致しなければ連番を付けた別のテーブルにする
        base = _table_name(layer.name())
        n = 1
        while True:
            table = base if n == 1 else f"{base}_{n}"
            n += 1
            if table in used_tables:
                continue
            if not append or not QgsVectorFileWriter.targetLayerExists(path, table):
                break
            existing = QgsVectorLayer(f"{path}|layername={table}", "", "ogr")
            if existing.wkbType() == layer.wkbType() and (
                not existing.isSpatial() or existing.crs() == layer.crs()
            ):
                options.actionOnExistingFile = (
                    QgsVectorFileWriter.ActionOnExistingFile.AppendToLayerAddFields
                )
                break
        used_tables.add(table)
        options.layerName = table

        error, message, *_ = QgsVectorFileWriter.writeAsVectorFormatV3(
            layer, path, context.transformContext(), options
        )
        if error != QgsVectorFileWriter.WriterError.NoError:
            raise QgsProcessingException(
                f"{path} のテーブル {table} への書き出しに失敗しました: {message}"
            )
        feedback.pushInfo(
            f"{layer.featureCount()} 個の地物を {table} に書き出しました。"
        )

        uri = f"{path}|layername={table}"
        loaded = [
            lyr
            for lyr in context.project().mapLayers().values()
            if _same_source(lyr, path, table)
        ]
        if loaded:
            # 既にプロジェクトに読み込まれているテーブルは追加せず、再描画だけする
            for lyr in loaded:
                lyr.triggerRepaint()
            continue

        details = QgsProcessingContext.LayerDetails(
            layer.name(),
            context.project(),
            layer.name(),
            QgsProcessingUtils.LayerHint.Vector,  # type: ignore
        )
        post_processor = _Renderer3DPostProcessor()
        _post_processors.append(post_processor)
        details.setPostProcessor(post_processor)
        context.addLayerToLoadOnCompletion(uri, details)
