"""
とりあえずのテスト実行用の __main__.py

python3 -m plateau /path/to/21201_gifu-shi_2022_citygml_1_op/udx/fld/natl/kisogawa_ibigawa/53360501_fld_6697_l2_op.gml
"""

import sys

from .models import processors
from .parse.parser import ParserSettings, PlateauCityGmlParser

if __name__ == "__main__":
    processors.validate_processors()

    # settings = ParseSettings(load_semantic_parts=True)
    settings = ParserSettings(
        only_first_found_lod=False, load_semantic_parts=False, load_apperance=True
    )
    parser = PlateauCityGmlParser(sys.argv[1], settings)
    for count, cityobj in parser.iter_cityobjs():
        print(
            f"{count} [{cityobj.processor.id}] {cityobj.type}, {cityobj.name}, LoD={cityobj.lod}, {cityobj.attributes}"
        )
