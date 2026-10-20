from pathlib import Path

import pytest
from qgis.core import (
    QgsApplication,
    QgsProcessingContext,
    QgsProcessingFeedback,
    QgsProcessingUtils,
    QgsProject,
    QgsVectorLayer,
)
from qgis.PyQt.QtGui import QIcon

TESTDATA = Path(__file__).parent / "testdata"
BLDG = str(TESTDATA / "64413325_bldg_6697_op.gml")
URF = str(TESTDATA / "533915_urf_6668_yoto_op.gml")


def test_registered(qgis_app: QgsApplication, provider: str):
    registory = QgsApplication.processingRegistry()
    provider = registory.providerById("plateau_plugin")
    assert provider is not None
    assert len(provider.name()) > 0
    assert isinstance(provider.icon(), QIcon)

    alg = registory.algorithmById("plateau_plugin:load_as_vector")
    assert alg is not None
    assert alg.group() is None
    assert alg.groupId() is None
    assert isinstance(alg.displayName(), str)
    assert isinstance(alg.shortHelpString(), str)


def _run(params: dict) -> tuple[dict, list[QgsVectorLayer]]:
    """アルゴリズムを実行し、戻り値と「完了時に読み込まれるレイヤ」(PostProcessor 適用済み) を返す"""
    import processing  # pyright: ignore

    context = QgsProcessingContext()
    feedback = QgsProcessingFeedback()
    context.setProject(QgsProject.instance())
    result = processing.run(
        "plateau_plugin:load_as_vector",
        params,
        context=context,
        feedback=feedback,
    )
    layers = []
    for uri, details in context.layersToLoadOnCompletion().items():
        layer = QgsProcessingUtils.mapLayerFromString(uri, context)
        context.temporaryLayerStore().takeMapLayer(layer)  # outlive the context
        layer.setName(details.name)
        if details.postProcessor():
            details.postProcessor().postProcessLayer(layer, context, feedback)
        layers.append(layer)
    return result, layers


def _gpkg_counts(path) -> dict[str, int]:
    from osgeo import ogr

    ds = ogr.Open(str(path))
    return {
        ds.GetLayer(i).GetName(): ds.GetLayer(i).GetFeatureCount()
        for i in range(ds.GetLayerCount())
    }


@pytest.mark.parametrize("src", [BLDG, URF])
def test_load_to_memory(provider, src):
    result, layers = _run({"INPUT": src})
    assert result == {}
    assert layers
    assert all(lyr.providerType() == "memory" for lyr in layers)
    assert sum(lyr.featureCount() for lyr in layers) > 0


@pytest.mark.parametrize("src", [BLDG, URF])
def test_load_to_gpkg(provider, tmp_path, src):
    _, mem_layers = _run({"INPUT": src})
    out = str(tmp_path / "out.gpkg")
    result, layers = _run({"INPUT": src, "OUTPUT": out})

    assert result["OUTPUT"] == out
    assert all(lyr.providerType() == "ogr" for lyr in layers)
    assert all(lyr.renderer3D() is not None for lyr in layers)
    assert len(_gpkg_counts(out)) == len(layers) == len(mem_layers)
    assert sum(_gpkg_counts(out).values()) == sum(
        lyr.featureCount() for lyr in mem_layers
    )

    # attributes and geometries are kept
    mem = {lyr.name(): lyr for lyr in mem_layers}
    for lyr in layers:
        m = mem[lyr.name()]
        assert lyr.wkbType() == m.wkbType()
        names = m.fields().names()
        assert [n for n in lyr.fields().names() if n != "fid"] == names
        for f_mem, f_gpkg in zip(m.getFeatures(), lyr.getFeatures()):
            assert [f_gpkg[n] for n in names] == [f_mem[n] for n in names]
            # memory layers may hold single polygons; GPKG promotes them to multi
            g = f_mem.geometry()
            g.convertToMultiType()
            assert f_gpkg.geometry().asWkt(3) == g.asWkt(3)  # incl. Z


def test_gpkg_append(provider, tmp_path):
    out = str(tmp_path / "out.gpkg")
    _run({"INPUT": BLDG, "OUTPUT": out})
    first = _gpkg_counts(out)

    result, _ = _run({"INPUT": BLDG, "OUTPUT": out, "APPEND_MODE": True})
    assert result["OUTPUT"] == out
    assert _gpkg_counts(out) == {k: v * 2 for k, v in first.items()}

    _run({"INPUT": BLDG, "OUTPUT": out, "APPEND_MODE": False})
    assert _gpkg_counts(out) == first


def test_gpkg_append_while_loaded(provider, tmp_path):
    out = str(tmp_path / "out.gpkg")
    _, layers = _run({"INPUT": URF, "OUTPUT": out})
    project = QgsProject.instance()
    project.addMapLayers(layers)
    try:
        _, layers2 = _run({"INPUT": URF, "OUTPUT": out})
        assert layers2 == []  # already in the project: not added twice
        counts = _gpkg_counts(out)
        assert all(v % 2 == 0 for v in counts.values())

        # recreating a file that is open in the project is refused
        with pytest.raises(Exception, match="開かれている"):
            _run({"INPUT": URF, "OUTPUT": out, "APPEND_MODE": False})
        assert _gpkg_counts(out) == counts
    finally:
        project.removeAllMapLayers()


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
