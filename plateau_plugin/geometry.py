"""ジオメトリ関係の処理"""

from qgis.core import (
    QgsGeometry,
    QgsLineString,
    QgsMultiLineString,
    QgsMultiPoint,
    QgsMultiPolygon,
    QgsPoint,
    QgsPolygon,
)

from .plateau.types import (
    Geometry,
    LineStringCollection,
    PointCollection,
    PolygonCollection,
)


def to_qgis_geometry(src_geom: Geometry, as2d: bool) -> QgsGeometry:
    """Convert geometries from PLATEAU module into QGIS geometry"""

    if as2d:
        return _to_qgis_geometry_2d(src_geom)

    if isinstance(src_geom, PolygonCollection):
        # MultiPolygon
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
    elif isinstance(src_geom, LineStringCollection):
        # MultiLineString
        dest_geoms = QgsMultiLineString()
        for src_line in src_geom.lines:
            dest_line = QgsLineString(src_line[:, 1], src_line[:, 0], src_line[:, 2])
            dest_geoms.addGeometry(dest_line)
    elif isinstance(src_geom, PointCollection):
        # MultiPoint
        dest_geoms = QgsMultiPoint()
        for src_point in src_geom.points:
            x, y, z = src_point
            dest_point = QgsPoint(y, x, z)
            dest_geoms.addGeometry(dest_point)
    else:
        raise RuntimeError(f"Unsupported geometry type: {type(src_geom)}")

    return dest_geoms


def _to_qgis_geometry_2d(src_geom: Geometry) -> QgsGeometry:
    """Convert geometries from PLATEAU module into QGIS geometry"""

    if isinstance(src_geom, PolygonCollection):
        # MultiPolygon
        polygons = []
        for src_rings in src_geom.polygons:
            # exterior ring
            src_ring = src_rings[0]
            dest_ring = QgsLineString(src_ring[:, 1], src_ring[:, 0])
            dest_poly = QgsPolygon(dest_ring)
            for src_ring in src_rings[1:]:
                # interior rings
                dest_ring = QgsLineString(src_ring[:, 1], src_ring[:, 0])
                dest_poly.addInteriorRing(dest_ring)
            polygons.append(dest_poly)

        return QgsGeometry.unaryUnion(QgsGeometry(p) for p in polygons)

    elif isinstance(src_geom, LineStringCollection):
        # MultiLineString
        dest_geoms = QgsMultiLineString()
        for src_line in src_geom.lines:
            dest_line = QgsLineString(src_line[:, 1], src_line[:, 0])
            dest_geoms.addGeometry(dest_line)
    elif isinstance(src_geom, PointCollection):
        # MultiPoint
        dest_geoms = QgsMultiPoint()
        for src_point in src_geom.points:
            x, y, _ = src_point
            dest_point = QgsPoint(y, x)
            dest_geoms.addGeometry(dest_point)
    else:
        raise RuntimeError(f"Unsupported geometry type: {type(src_geom)}")

    return dest_geoms
