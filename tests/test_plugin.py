# from pathlib import Path
#
# from PyQt5.QtGui import QIcon
# from qgis.core import QgsApplication, QgsVectorLayer


# def test_registered(qgis_app: QgsApplication, provider: str):
#     registory = QgsApplication.processingRegistry()
#     provider = registory.providerById("plateauloader")
#     assert provider is not None
#     assert len(provider.name()) > 0
#     assert isinstance(provider.icon(), QIcon)
#
#     alg = registory.algorithmById("plateauloader:plateauloader")
#     assert alg is not None
#     assert alg.group() is None
#     assert alg.groupId() is None
#     assert isinstance(alg.displayName(), str)
#     assert isinstance(alg.shortHelpString(), str)
#
#
# def test_load_xml(qgis_app: QgsApplication, provider: str):
#     import processing
#
#     result = processing.run(
#         "plateauloader:plateauloader",
#         {
#             "INPUT": "testdata/15222-1107-1553.xml",
#             "OUTPUT": "memory:",
#         },
#     )
#     v: QgsVectorLayer = result["OUTPUT"]
#     assert v.featureCount() == 1051
#
#
# def test_load_xml_to_file(qgis_app: QgsApplication, provider: str, tmp_path: Path):
#     import processing
#
#     output_path = str(tmp_path / "test.gpkg")
#     result = processing.run(
#         "plateauloader:plateauloader",
#         {
#             "INPUT": "testdata/15222-1107-1553.xml",
#             "OUTPUT": output_path,
#         },
#     )
#     assert result["OUTPUT"] == output_path
#
#
# def test_load_zip(qgis_app: QgsApplication, provider: str):
#     import processing  # pyright: ignore
#
#     result = processing.run(
#         "plateauloader:plateauloader",
#         {
#             "INPUT": "testdata/14103-0200.zip",
#             "INCLUDE_CHIKUGAI": True,
#             "OUTPUT": "memory:",
#         },
#     )
#     layer: QgsVectorLayer = result["OUTPUT"]
#     assert layer.featureCount() == 453
#
#     result = processing.run(
#         "plateauloader:plateauloader",
#         {
#             "INPUT": "testdata/14103-0200.zip",
#             "INCLUDE_CHIKUGAI": False,
#             "OUTPUT": "memory:",
#         },
#     )
#     layer: QgsVectorLayer = result["OUTPUT"]
#     assert layer.featureCount() == 446
#
#     result = processing.run(
#         "plateauloader:plateauloader",
#         {
#             "INPUT": "testdata/14103-0200.zip",
#             "INCLUDE_ARBITRARY_CRS": True,
#             "INCLUDE_CHIKUGAI": False,
#             "OUTPUT": "memory:",
#         },
#     )
#     layer: QgsVectorLayer = result["OUTPUT"]
#     assert layer.featureCount() == 27237
#
