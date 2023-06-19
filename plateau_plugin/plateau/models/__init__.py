from .base import ProcessorRegistory
from .bridge import BRIDGE, BRIDGE_BOUNDARY_SURFACE
from .building import BUILDING, BUILDING_BOUNDARY_SURFACE
from .cityfurniture import CITY_FURNITURE
from .landslide import LAND_SLIDE
from .landuse import LAND_USE
from .transportation import ROAD, TRAFFIC_AREA
from .waterbody import WATER_BODY

processors = ProcessorRegistory(
    [
        BUILDING,
        BUILDING_BOUNDARY_SURFACE,
        BRIDGE,
        BRIDGE_BOUNDARY_SURFACE,
        ROAD,
        TRAFFIC_AREA,
        CITY_FURNITURE,
        LAND_SLIDE,
        LAND_USE,
        WATER_BODY,
    ]
)
