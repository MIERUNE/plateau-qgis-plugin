"""Processing provider for this plugin"""

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

from pathlib import Path

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from .algorithms.load_dem import PlateauDEMLoaderAlrogithm
from .algorithms.load_vector import PlateauVectorLoaderAlrogithm


class PlateauProcessingProvider(QgsProcessingProvider):
    def loadAlgorithms(self, *args, **kwargs):
        self.addAlgorithm(PlateauVectorLoaderAlrogithm())
        self.addAlgorithm(PlateauDEMLoaderAlrogithm())

    def id(self, *args, **kwargs):
        return "plateau_plugin"

    def name(self, *args, **kwargs):
        return self.tr("Project PLATEAU")

    def icon(self):
        path = (Path(__file__).parent / "icon.png").resolve()
        return QIcon(str(path))
