from .base import (
    Attribute,
    Emission,
    Emissions,
    LODDetection,
    ProcessorDefinition,
)

LAND_SLIDE = ProcessorDefinition(
    id="SedimentDisasterProneArea",
    target_elements=[
        "urf2:SedimentDisasterProneArea",
        "urf3:SedimentDisasterProneArea",
    ],
    lod_detection=LODDetection(
        lod1=["./urf2:lod1MultiSurface", "./urf3:lod1MultiSurface"],
    ),
    attributes=[
        Attribute(
            name="prefecture",
            xpath="(./urf2:prefecture | ./urf3:prefecture)/text()",
            datatype="string",
            codelist="Common_prefecture",
        ),
        Attribute(
            name="location",
            xpath="(./urf2:location | ./urf3:location)/text()",
            datatype="string",
        ),
        Attribute(
            name="disasterType",
            xpath="(./urf2:disasterType | ./urf3:disasterType)/text()",
            datatype="string",
            codelist="SedimentDisasterProneArea_disasterType",
        ),
        Attribute(
            name="areaType",
            xpath="(./urf2:areaType | ./urf3:areaType)/text()",
            datatype="string",
            codelist="SedimentDisasterProneArea_areaType",
        ),
        Attribute(
            name="status",
            xpath="(./urf2:status | ./urf3:status)/text()",
            datatype="string",
            codelist="SedimentDisasterProneArea_status",
        ),
        Attribute(
            name="zoneName",
            xpath="(./urf2:zoneName | ./urf3:zoneName)/text()",
            datatype="string",
        ),
        Attribute(
            name="zoneNumber",
            xpath="(./urf2:zoneNumber | ./urf3:zoneNumber)/text()",
            datatype="string",
        ),
    ],
    emissions=Emissions(
        lod1=Emission(
            elem_paths=[
                "./urf2:lod1MultiSurface//gml:Polygon",
                "./urf3:lod1MultiSurface//gml:Polygon",
            ]
        ),
    ),
)
