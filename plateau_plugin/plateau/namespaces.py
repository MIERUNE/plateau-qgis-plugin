"""定数値"""

import re

BASE_NS = {
    "gml": "http://www.opengis.net/gml",
    "core": "http://www.opengis.net/citygml/2.0",
    "app": "http://www.opengis.net/citygml/appearance/2.0",
    "bldg": "http://www.opengis.net/citygml/building/2.0",
    "brid": "http://www.opengis.net/citygml/bridge/2.0",
    "dem": "http://www.opengis.net/citygml/relief/2.0",
    "frn": "http://www.opengis.net/citygml/cityfurniture/2.0",
    "grp": "http://www.opengis.net/citygml/cityobjectgroup/2.0",
    "luse": "http://www.opengis.net/citygml/landuse/2.0",
    "tran": "http://www.opengis.net/citygml/transportation/2.0",
    "veg": "http://www.opengis.net/citygml/vegetation/2.0",
    "wtr": "http://www.opengis.net/citygml/waterbody/2.0",
    "tun": "http://www.opengis.net/citygml/tunnel/2.0",
    "uro2": "https://www.geospatial.jp/iur/uro/2.0",
    "urf2": "https://www.geospatial.jp/iur/urf/2.0",
    "uro3": "https://www.geospatial.jp/iur/uro/3.0",
    "urf3": "https://www.geospatial.jp/iur/urf/3.0",
}
"""XML Namespaces"""


class Namespace:
    def __init__(self, update: dict):
        self.nsmap: dict[str, str] = dict(**BASE_NS, **update)
        self.inverted = {v: k for k, v in self.nsmap.items()}

    @classmethod
    def from_document_nsmap(cls, src_nsmap: dict[str, str]) -> "Namespace":
        _ns_update = {}
        for ns in src_nsmap.values():
            if ns.startswith("https://www.geospatial.jp/iur/uro/"):
                _ns_update["uro"] = ns
            if ns.startswith("https://www.geospatial.jp/iur/urf/"):
                _ns_update["urf"] = ns
        return cls(_ns_update)

    def to_qualified_name(self, prefixed_name: str) -> str:
        return re.sub(
            r"^(.+?):()", lambda m: "{" + self.nsmap[m.group(1)] + "}", prefixed_name
        )

    def to_prefixed_name(self, qualified_name: str) -> str:
        return re.sub(
            r"^{([^}]+)}", lambda m: f"{self.inverted[m.group(1)]}:", qualified_name
        )
