"""区域モデル (./area/)、都市計画決定情報モデル (./urf/)"""

from .district_dev_plans import DEFS as DISTRICT_DEV_PLAN_DEFS
from .district_facilities import DEFS as DISTRICT_FACILITY_DEFS
from .district_plans import DEFS as DISTRICT_PLAN_DEFS
from .districts_and_zones import DEFS as DISTRICTS_AND_ZONES_DEFS
from .promotion_areas import DEFS as PROMOTION_AREA_DEFS
from .scheduled_areas import DEFS as SCHEDULED_AREA_DEFS
from .simple import DEFS as SIMPLE_DEFS
from .urban_dev_projects import DEFS as URBAN_DEV_PROJECT_DEFS
from .urban_facilities import DEFS as URBAN_FACILITY_DEFS

DEFS = [
    *SIMPLE_DEFS,
    *URBAN_FACILITY_DEFS,
    *DISTRICT_PLAN_DEFS,
    *DISTRICT_DEV_PLAN_DEFS,
    *DISTRICT_FACILITY_DEFS,
    *SCHEDULED_AREA_DEFS,
    *PROMOTION_AREA_DEFS,
    *URBAN_DEV_PROJECT_DEFS,
    *DISTRICTS_AND_ZONES_DEFS,
]
