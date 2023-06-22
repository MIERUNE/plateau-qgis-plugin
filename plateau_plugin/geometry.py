"""ジオメトリ関係の処理"""

from qgis.core import (
    QgsGeometry,
    # QgsLayerTreeGroup,
    QgsLineString,
    QgsMultiPolygon,
    QgsPolygon,
)

from .plateau.types import Geometry, MultiPolygon


def to_qgis_geometry(src_geom: Geometry) -> QgsGeometry:
    """PLATEAUモジュールのジオメトリをQGISのジオメトリに変換する"""

    if isinstance(src_geom, MultiPolygon):
        dest_geoms = QgsMultiPolygon()
        for src_rings in src_geom.polygons:
            # exterior ring
            src_ring = src_rings[0]
            dest_ring = QgsLineString(src_ring[:, 1], src_ring[:, 0], src_ring[:, 2])
            dest_poly = QgsPolygon(dest_ring)
            for src_ring in src_rings[1:]:
                # interior rings
                dest_ring = QgsLineString(
                    src_ring[:, 1], src_ring[:, 0], src_ring[:, 2]
                )
                dest_poly.addInteriorRing(dest_ring)
            dest_geoms.addGeometry(dest_poly)
    else:
        raise RuntimeError(f"Unsupported geometry type: {type(src_geom)}")

    return dest_geoms
