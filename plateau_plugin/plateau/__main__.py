import sys

from .parser import FileParser
from .types import ParseSettings

if __name__ == "__main__":
    settings = ParseSettings(load_semantic_parts=True)
    parser = FileParser(sys.argv[1], settings)
    for count, cityobj in parser.iter_city_objects():
        types = [pname for pname, _pid in cityobj.processor_path]
        print(
            f"{count} [{' / '.join(types)}] {cityobj.type}, {cityobj.name}, {cityobj.lod}, {cityobj.properties}"
        )
