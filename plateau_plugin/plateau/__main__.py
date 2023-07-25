"""
テスト実行用 __main__.py

python3 -m plateau /path/to/21201_gifu-shi_2022_citygml_1_op/udx/fld/natl/kisogawa_ibigawa/53360501_fld_6697_l2_op.gml
"""

import sys
from pathlib import Path
from typing import Sequence

import numpy as np
import pyproj
import trimesh
import trimesh.scene.cameras
import trimesh.visual
from earcut import earcut
from earcut.utils_3d import project3d_to_2d
from PIL import Image

from .models import processors
from .parser import FileParser, ParseSettings
from .types import Material, PolygonCollection

transformer = pyproj.Transformer.from_crs("epsg:6697", "epsg:6676", always_xy=True)

loaded_textures = {}


def load_texture(basepath: Path, uri: str) -> trimesh.visual.texture.SimpleMaterial:
    if tex := loaded_textures.get(uri):
        return tex
    else:
        img = Image.open(basepath / uri)
        texmat = trimesh.visual.texture.SimpleMaterial(
            image=img, diffuse=(255, 255, 255)
        )
        loaded_textures[uri] = texmat
        return texmat


def load_polygons(
    basepath: Path,
    polygons: list[list[np.ndarray]],
    materials: Sequence[Material] | None,
    textures,
    uvs,
) -> tuple[
    np.ndarray, np.ndarray, np.ndarray, trimesh.visual.texture.TextureVisuals | None
]:
    all_vertices = np.empty((0, 3), dtype=np.float64)
    all_faces = np.empty((0, 3), dtype=np.uint32)
    face_colors = np.empty((0, 3), dtype=np.uint8)
    all_uvs = np.empty((0, 2), dtype=np.float32)
    texmat = None
    loaded_tex = None

    for idx, polygon in enumerate(polygons):
        mat = materials[idx] if materials else None

        # Flatten
        vertices = np.vstack(polygon)

        # texture uv
        rings_uv = uvs[idx] if uvs else None
        if rings_uv and any(uv is not None for uv in rings_uv):
            assert all(uv is not None for uv in rings_uv)
            uv = np.vstack(rings_uv)
            assert uv.shape[0] == vertices.shape[0]
        else:
            uv = np.zeros((vertices.shape[0], 2))
        all_uvs = np.vstack((all_uvs, uv))

        t = textures[idx] if textures else None
        if t:
            if texmat is not None and t != loaded_tex:
                print("warn", t.image_uri, loaded_tex.image_uri)
            loaded_tex = t
            texmat = load_texture(basepath, t.image_uri)

        hole_indices = []
        if len(polygon) > 1:
            hi = polygon[0].shape[0]
            for ring in polygon[1:]:
                hole_indices.append(hi)
                hi += ring.shape[0]
        xx, yy = transformer.transform(vertices[:, 1], vertices[:, 0])
        vertices[:, 0] = np.asarray(xx)
        vertices[:, 1] = np.asarray(yy)
        flatten_vertices = vertices.flatten()

        # Earcut
        flatten_vertices = project3d_to_2d(flatten_vertices, len(polygon[0]))
        if flatten_vertices is not None:
            cut = earcut(flatten_vertices, hole_indices, dim=2)
            if cut:
                start_index = len(all_vertices)
                faces = (np.asarray(cut) + start_index).reshape(-1, 3)
                all_faces = np.vstack((all_faces, faces))
                if mat:
                    color = (np.asarray(mat.diffuse_color) * 255).astype(np.uint8)
                else:
                    color = np.array([255, 255, 255], dtype=np.uint8)
                face_colors = np.vstack(
                    (
                        face_colors,
                        np.tile(color, len(faces)).reshape(-1, 3),
                    )
                )
        all_vertices = np.vstack((all_vertices, vertices))

    if texmat:
        assert len(all_uvs) == len(
            all_vertices
        ), f"uv={len(all_uvs)}, verts={len(all_vertices)}"
    tex_visual = (
        trimesh.visual.TextureVisuals(uv=all_uvs, material=texmat) if texmat else None
    )
    return all_vertices, all_faces, face_colors, tex_visual


if __name__ == "__main__":
    processors.validate_processors()
    meshes = []

    # settings = ParseSettings(load_semantic_parts=True)
    for filename in sys.argv[1:]:
        settings = ParseSettings(
            only_highest_lod=False, load_semantic_parts=False, load_apperance=True
        )
        parser = FileParser(filename, settings)
        parser.load_apperance()
        for count, cityobj in parser.iter_cityobjs():
            if cityobj.lod is None or cityobj.lod != 2:
                continue

            print(
                f"{count} [{cityobj.processor.id}] {cityobj.type}, {cityobj.name}, LoD={cityobj.lod}, {cityobj.attributes}"
            )
            assert isinstance(cityobj.geometry, PolygonCollection)
            vertices, faces, face_colors, visual = load_polygons(
                Path(filename).parent,
                cityobj.geometry.polygons,
                cityobj.geometry.materials,
                cityobj.geometry.textures,
                cityobj.geometry.uvs,
            )
            if "frn" in filename:
                vertices[:, 2] += 0.05

            vertices *= 0.01
            mesh = trimesh.Trimesh(
                vertices=vertices.reshape(-1, 3),
                faces=faces,
                face_colors=face_colors,
                process=False,
            )
            if visual:
                assert len(mesh.vertices) == len(visual.uv.reshape(-1, 2))
                mesh.visual = visual
            meshes.append(mesh)

    print(len(loaded_textures))

    scene = trimesh.Scene(
        meshes,
        camera=trimesh.scene.cameras.Camera(
            name="camera1", fov=(60, 60), z_near=0.01, z_far=1000
        ),
    )
    scene.set_camera((0, 0, 0), 5)
    scene.show(background=[210, 240, 255, 255])
