"""Main plugin class"""

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

import contextlib

from PyQt5.QtWidgets import QAction
from qgis.core import QgsApplication
from qgis.gui import QgisInterface

from .provider import PlateauProcessingProvider

with contextlib.suppress(ImportError):
    from processing import execAlgorithmDialog


class PlateauPlugin:
    """PLATEAU QGIS plugin"""

    def __init__(self, iface: QgisInterface):
        self.iface = iface

    def initGui(self):
        self.provider = PlateauProcessingProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

        if self.iface:
            icon = self.provider.icon()
            self._toolbar_action = QAction(
                icon, "PLATEAU 3D都市モデルを読み込む", self.iface.mainWindow()
            )
            self._toolbar_action.triggered.connect(self._show_processing_dialog)
            self.iface.addToolBarIcon(self._toolbar_action)

    def _show_processing_dialog(self):
        execAlgorithmDialog("plateau_plugin:load_as_vector", {})

    def unload(self):
        if self.iface:
            self.iface.removeToolBarIcon(self._toolbar_action)
        QgsApplication.processingRegistry().removeProvider(self.provider)
