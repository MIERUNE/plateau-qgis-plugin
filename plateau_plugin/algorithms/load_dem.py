"""Processing algorithm for loading a PLATEAU dem file as a mesh layer"""

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

import lxml.etree as et
import numpy as np
from PyQt5.QtCore import QCoreApplication
from qgis.core import (
    # QgsLayerTreeGroup,
    QgsProcessingAlgorithm,
    QgsProcessingContext,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingUtils,
)

from ..plateau.namespaces import BASE_NS

_PLY_HEADER_TEMPLATE = """ply
format binary_little_endian 1.0
comment crs: GEOGCRS["JGD2011",DATUM["Japanese Geodetic Datum 2011",ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",0.0174532925199433]],CS[ellipsoidal,2],AXIS["geodetic latitude (Lat)",north,ORDER[1],ANGLEUNIT["degree",0.0174532925199433]],AXIS["geodetic longitude (Lon)",east,ORDER[2],ANGLEUNIT["degree",0.0174532925199433]],USAGE[SCOPE["Horizontal component of 3D system."],AREA["Japan - onshore and offshore."],BBOX[17.09,122.38,46.05,157.65]],ID["EPSG",6668]]
element vertex {n_verts}
property float x
property float y
property float z
element face {n_faces}
property list uchar uint vertex_indices
end_header\n"""


_DESCRIPTION = """PLATEAU の地形モデル (./dem/) の CityGML ファイルを QGIS のメッシュレイヤとして読み込みます。"""


def convert_citygml_relief_to_ply(src_filename: str, dst_filename: str) -> None:
    doc = et.parse(src_filename, None)
    index_map = {}
    points = []
    faces = []
    for pos_list in doc.iterfind(".//dem:TINRelief//gml:posList", BASE_NS):
        tri_verts = [float(v) for v in pos_list.text.split()]
        tri_indices = [b"\x03"]
        for i in range(3):
            y, x, z = tri_verts[i * 3 : i * 3 + 3]
            key = (x, y)
            if (idx := index_map.get(key)) is None:
                idx = index_map[key] = len(index_map)
                points.extend((x, y, z))
            tri_indices.append(idx.to_bytes(4, "little"))
        faces.append(b"".join(tri_indices))

    with open(dst_filename, "wb") as f:
        f.write(
            _PLY_HEADER_TEMPLATE.format(
                n_verts=len(points) // 3, n_faces=len(faces)
            ).encode("ascii")
        )
        f.write(np.asarray(points, dtype="<f4").tobytes())
        f.write(b"".join(faces))


class PlateauDEMLoaderAlrogithm(QgsProcessingAlgorithm):
    """Processing algorithm to load CityGML Relief (DEM) models as mesh layers"""

    INPUT = "INPUT"
    OUTPUT_MESH = "OUTPUT_MESH"

    def tr(self, string: str):
        return QCoreApplication.translate("Processing", string)

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT,
                self.tr("PLATEAU 地形モデルの CityGML ファイル"),
                fileFilter=self.tr("PLATEAU CityGML ファイル (*.gml)"),
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_MESH,
                self.tr("出力メッシュファイル"),
                fileFilter=self.tr("Stanford PLY メッシュファイル (*.ply)"),
                optional=True,
            )
        )

    def createInstance(self):
        return PlateauDEMLoaderAlrogithm()

    def name(self):
        return "load_dem_as_mesh"

    def group(self):
        return None

    def groupId(self):
        return None

    def displayName(self):
        return self.tr("PLATEAU 地形モデルをメッシュとして読み込む")

    def shortHelpString(self) -> str:
        return self.tr(_DESCRIPTION)

    def processAlgorithm(self, parameters, context, feedback):
        input_filename = self.parameterAsFile(parameters, self.INPUT, context)
        output_filename = self.parameterAsFile(parameters, self.OUTPUT_MESH, context)

        feedback.pushInfo(f"Converting {input_filename} to {output_filename}")
        feedback.setProgressText("地形モデルをメッシュに変換しています")
        try:
            convert_citygml_relief_to_ply(input_filename, output_filename)
        except Exception as e:
            feedback.reportError(
                "変換に失敗しました。ファイルがTIN地形モデルを含んでいない可能性があります",
                fatalError=True,
            )
            raise e

        context.addLayerToLoadOnCompletion(
            output_filename,
            QgsProcessingContext.LayerDetails(
                "TINRelief", context.project(), "TIN", QgsProcessingUtils.Mesh
            ),
        )

        return {
            "OUTPUT_MESH": output_filename,
        }
