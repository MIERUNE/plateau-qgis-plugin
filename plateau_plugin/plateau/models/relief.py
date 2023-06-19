"""Relief (dem)"""

from .base import (
    Attribute,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

RELIEF = ProcessorDefinition(
    id="ReliefFeature",
    target_elements=["dem:ReliefFeature"],
    lod_detection=LODDetection(
        lod_n="dem:lod",
    ),
    attributes=[],
    emissions=Emissions(
        # ひとまず TIN のみ対応する
        lod1=Emission(
            elem_paths=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod2=Emission(
            elem_paths=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
        lod3=Emission(
            elem_paths=["./dem:reliefComponent/dem:TINRelief/dem:tin//gml:Triangle"]
        ),
    ),
)
