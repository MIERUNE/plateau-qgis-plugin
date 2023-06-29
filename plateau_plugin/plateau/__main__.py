"""
テスト実行用 __main__.py

python3 -m plateau /path/to/21201_gifu-shi_2022_citygml_1_op/udx/fld/natl/kisogawa_ibigawa/53360501_fld_6697_l2_op.gml
"""

import sys

from .models import processors
from .parser import FileParser, ParseSettings

if __name__ == "__main__":
    processors.validate_processors()

    settings = ParseSettings(load_semantic_parts=True)
    parser = FileParser(sys.argv[1], settings)
    for count, cityobj in parser.iter_cityobjs():
        types = [pname for pname, _pid in cityobj.processor_path]
        print(
            f"{count} [{' / '.join(types)}] {cityobj.type}, {cityobj.name}, {cityobj.lod}, {cityobj.attributes}"
        )
