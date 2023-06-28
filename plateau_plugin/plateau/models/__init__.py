from .base import ProcessorRegistory
from .bridge import (
    BRIDGE,
    BRIDGE_BOUNDARY_SURFACE,
    BRIDGE_CONSTRUCTION_ELEMENT,
    BRIDGE_FURNITURE,
    BRIDGE_INSTALLATION,
    BRIDGE_INT_INSTALLATION,
    BRIDGE_OPENING,
)
from .building import (
    BUILDING,
    BUILDING_BOUNDARY_SURFACE,
    BUILDING_FURNITURE,
    BUILDING_INSTALLATION,
    BUILDING_INT_INSTALLATION,
    BUILDING_OPENING,
)
from .cityfurniture import CITY_FURNITURE
from .generics import GENERIC_CITY_OBJECT
from .landuse import LAND_USE
from .relief import RELIEF
from .transportation import RAILWAY, ROAD, TRAFFIC_AREA
from .urf_lsld import URF_SEDIMENT_DISASTER_PRONE_AREA
from .urf_zone import URF_ZONE
from .uro_ubld import UNDERGROUND_BUILDING
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
        BUILDING_FURNITURE,
        # bridge
        BRIDGE,
        BRIDGE_BOUNDARY_SURFACE,
        BRIDGE_CONSTRUCTION_ELEMENT,
        BRIDGE_INSTALLATION,
        BRIDGE_INT_INSTALLATION,
        BRIDGE_OPENING,
        BRIDGE_FURNITURE,
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
        # uro - underground building
        UNDERGROUND_BUILDING,
        # urf - sediment disaster
        URF_SEDIMENT_DISASTER_PRONE_AREA,
        # urf - Zone
        URF_ZONE,
    ]
)
