from .base import (
    Attribute,
    ChildrenPaths,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

ROAD = ProcessorDefinition(
    id="Road",
    target_elements=["tran:Road"],
    lod_detection=LODDetection(
        lod1=["./tran:lod1MultiSurface"],
        lod2=["./tran:lod2MultiSurface"],
        lod3=["./tran:lod3MultiSurface"],
        lod4=["./tran:lod4MultiSurface"],
    ),
    attributes=[
        Attribute(
            name="class",
            path="./tran:class",
            datatype="string",
            codelist="TransportationComplex_class",
        ),
        Attribute(
            name="function",
            path="./tran:function",
            datatype="[]string",
            codelist="Road_function",
        ),
        Attribute(
            name="usage",
            path="./tran:usage",
            datatype="[]string",
            codelist="Road_usage",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(elem_paths=["./tran:lod1MultiSurface//gml:Polygon"]),
        lod2=Emission(elem_paths=["./tran:*//tran:lod2MultiSurface//gml:Polygon"]),
        lod3=Emission(elem_paths=["./tran:*//tran:lod3MultiSurface//gml:Polygon"]),
        lod4=Emission(elem_paths=["./tran:*//tran:lod4MultiSurface//gml:Polygon"]),
    ),
    children=ChildrenPaths(
        lod2=["./tran:trafficArea/tran:TrafficArea"],
        lod3=["./tran:trafficArea/tran:TrafficArea"],
        lod4=["./tran:trafficArea/tran:TrafficArea"],
    ),
)

# Road > TrafficArea および Road > AuxiliaryTrafficArea を扱う
TRAFFIC_AREA = ProcessorDefinition(
    id="Traffic Area",
    target_elements=["tran:TrafficArea", "tran:AuxiliaryTrafficArea"],
    attributes=[
        Attribute(
            name="function",
            path="./tran:function",
            datatype="[]string",
            codelist="TrafficArea_function",
        ),
        Attribute(
            name="surfaceMaterial",
            path="./tran:surfaceMaterial",
            datatype="string",
            codelist="TrafficArea_surfaceMaterial",
        ),
    ],
    lod_detection=LODDetection(
        lod2=["./tran:lod2MultiSurface"],
        lod3=["./tran:lod3MultiSurface"],
        lod4=["./tran:lod4MultiSurface"],
    ),
    emissions=Emissions(
        lod2=Emission(elem_paths=["./tran:lod2MultiSurface//gml:Polygon"]),
        lod3=Emission(elem_paths=["./tran:lod3MultiSurface//gml:Polygon"]),
        lod4=Emission(elem_paths=["./tran:lod4MultiSurface//gml:Polygon"]),
    ),
)
