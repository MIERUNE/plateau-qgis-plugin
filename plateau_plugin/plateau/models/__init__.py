from .base import ProcessorRegistory
from .bridge import (
    BRIDGE,
    BRIDGE_BOUNDARY_SURFACE,
    BRIDGE_CONSTRUCTION_ELEMENT,
    BRIDGE_INSTALLATION,
)
from .building import BUILDING, BUILDING_BOUNDARY_SURFACE
from .cityfurniture import CITY_FURNITURE
from .landslide import LAND_SLIDE
from .landuse import LAND_USE
from .relief import RELIEF
from .transportation import ROAD, TRAFFIC_AREA
from .vegetation import PLANT_COVER, SOLITARY_VEGETATION_OBJECT
from .waterbody import WATER_BODY

processors = ProcessorRegistory(
    [
        # buliding
        BUILDING,
        BUILDING_BOUNDARY_SURFACE,
        # bridge
        BRIDGE,
        BRIDGE_BOUNDARY_SURFACE,
        BRIDGE_CONSTRUCTION_ELEMENT,
        BRIDGE_INSTALLATION,
        # transportation
        ROAD,
        TRAFFIC_AREA,
        # cityfurniture
        CITY_FURNITURE,
        # vegetation
        SOLITARY_VEGETATION_OBJECT,
        PLANT_COVER,
        # landuse
        LAND_USE,
        # relief
        RELIEF,
        # waterbody
        WATER_BODY,
        # urf
        LAND_SLIDE,
    ]
)
