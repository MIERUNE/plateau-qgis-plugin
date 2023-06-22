from .base import ProcessorRegistory
from .bridge import (
    BRIDGE,
    BRIDGE_BOUNDARY_SURFACE,
    BRIDGE_CONSTRUCTION_ELEMENT,
    BRIDGE_INSTALLATION,
)
from .building import (
    BUILDING,
    BUILDING_BOUNDARY_SURFACE,
    BUILDING_INSTALLATION,
    BUILDING_INT_INSTALLATION,
    BUILDING_OPENING,
)
from .cityfurniture import CITY_FURNITURE
from .generics import GENERIC_CITY_OBJECT
from .landuse import LAND_USE
from .relief import RELIEF
from .sediment import SEDIMENT_DISASTER_PRONE_AREA
from .transportation import RAILWAY, ROAD, TRAFFIC_AREA
from .vegetation import PLANT_COVER, SOLITARY_VEGETATION_OBJECT
from .waterbody import WATER_BODY

processors = ProcessorRegistory(
    [
        # buliding
        BUILDING,
        BUILDING_BOUNDARY_SURFACE,
        BUILDING_INSTALLATION,
        BUILDING_INT_INSTALLATION,
        BUILDING_OPENING,
        # bridge
        BRIDGE,
        BRIDGE_BOUNDARY_SURFACE,
        BRIDGE_CONSTRUCTION_ELEMENT,
        BRIDGE_INSTALLATION,
        # transportation
        ROAD,
        RAILWAY,
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
        # generics
        GENERIC_CITY_OBJECT,
        # urf (sediment disaster)
        SEDIMENT_DISASTER_PRONE_AREA,
    ]
)
