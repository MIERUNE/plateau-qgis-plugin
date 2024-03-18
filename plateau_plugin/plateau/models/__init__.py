from .attr_disaster_risk import (
    ATTR_DISASTER_RISK_HIGH_TIDE,
    ATTR_DISASTER_RISK_INLAND_FLOODING,
    ATTR_DISASTER_RISK_LAND_SLIDE,
    ATTR_DISASTER_RISK_RIVER_FLOODING,
    ATTR_DISASTER_RISK_TSUNAMI,
)
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
    BUILDING_DETAIL,
    BUILDING_FURNITURE,
    BUILDING_INSTALLATION,
    BUILDING_INT_INSTALLATION,
    BUILDING_OPENING,
    LARGE_CUSTOMER_FACILITY_ATTRIBUTE,
)
from .cityfurniture import CITY_FURNITURE, CITY_FURNITURE_DETAIL_ATTRIBUTE
from .generics import GENERIC_CITY_OBJECT
from .landuse import LAND_USE
from .relief import RELIEF
from .transportation import (
    AUXILIARY_TRAFFIC_AREA,
    RAILWAY,
    RAILWAY_TRACK_ATTRIBUTE,
    ROAD,
    SQUARE,
    TRACK,
    TRAFFIC_AREA,
    URO_CONTROL_POINT,
    WATERWAY,
)
from .tunnel import (
    TUNNEL,
    TUNNEL_BOUNDARY_SURFACE,
    TUNNEL_FURNITURE,
    TUNNEL_INSTALLATION,
    TUNNEL_INT_INSTALLATION,
    TUNNEL_OPENING,
)
from .urf_landslide import URF_SEDIMENT_DISASTER_PRONE_AREA
from .urf_zone import DEFS as URF_DEFS
from .uro_dm import DM_GEOMETRIC
from .uro_other_construction import (
    OTHER_CONSTRUCTION,
    OTHER_CONSTRUCTION_BOUNDARY_SURFACE,
    OTHER_CONSTRUCTION_INSTALLATION,
    URO_ELEVATION,
    URO_HEIGHT,
)
from .uro_underground_building import UNDERGROUND_BUILDING
from .uro_utility_network import (
    LENGTH_ATTRIBUTE,
    OFFSET_DEPTH,
    THEMATIC_SHAPE,
    UTILITY_LINK,
    UTILITY_NODE,
    UTILITY_NODE_CONTAINER,
)
from .vegetation import PLANT_COVER, SOLITARY_VEGETATION_OBJECT
from .waterbody import WATER_BODY, WATER_BOUNDARY_SURFACE

processors = ProcessorRegistory(
    [
        # buliding
        BUILDING,
        BUILDING_BOUNDARY_SURFACE,
        BUILDING_INSTALLATION,
        BUILDING_INT_INSTALLATION,
        BUILDING_OPENING,
        BUILDING_FURNITURE,
        BUILDING_DETAIL,
        LARGE_CUSTOMER_FACILITY_ATTRIBUTE,
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
        TRACK,
        SQUARE,
        WATERWAY,
        TRAFFIC_AREA,
        AUXILIARY_TRAFFIC_AREA,
        RAILWAY_TRACK_ATTRIBUTE,
        # tunnel
        TUNNEL,
        TUNNEL_BOUNDARY_SURFACE,
        TUNNEL_FURNITURE,
        TUNNEL_INSTALLATION,
        TUNNEL_INT_INSTALLATION,
        TUNNEL_OPENING,
        # cityfurniture
        CITY_FURNITURE,
        CITY_FURNITURE_DETAIL_ATTRIBUTE,
        # vegetation
        SOLITARY_VEGETATION_OBJECT,
        PLANT_COVER,
        # landuse
        LAND_USE,
        # relief
        RELIEF,
        # waterbody
        WATER_BODY,
        WATER_BOUNDARY_SURFACE,
        # generics
        GENERIC_CITY_OBJECT,
        # uro - other construction
        OTHER_CONSTRUCTION,
        OTHER_CONSTRUCTION_BOUNDARY_SURFACE,
        OTHER_CONSTRUCTION_INSTALLATION,
        URO_ELEVATION,
        URO_HEIGHT,
        URO_CONTROL_POINT,
        # uro - underground building
        UNDERGROUND_BUILDING,
        # uro - underground city furniture
        UTILITY_LINK,
        UTILITY_NODE,
        UTILITY_NODE_CONTAINER,
        LENGTH_ATTRIBUTE,
        OFFSET_DEPTH,
        THEMATIC_SHAPE,
        # urf - sediment disaster
        URF_SEDIMENT_DISASTER_PRONE_AREA,
        # urf - Zone
        *URF_DEFS,
        # attributes: uro:DisasterRiskAttribute, uro:BuildingDisasterRiskAttribute
        ATTR_DISASTER_RISK_HIGH_TIDE,
        ATTR_DISASTER_RISK_INLAND_FLOODING,
        ATTR_DISASTER_RISK_LAND_SLIDE,
        ATTR_DISASTER_RISK_RIVER_FLOODING,
        ATTR_DISASTER_RISK_TSUNAMI,
        # uro - dm
        DM_GEOMETRIC,
    ]
)
