import sys

from .parser import FileParser

if __name__ == "__main__":
    parser = FileParser(sys.argv[1])
    for count, cityobj in parser.iter_city_objects():
        types = [pname for pname, _pid in cityobj.processor_path]
        print(
            f"{count} [{' / '.join(types)}] {cityobj.type}, {cityobj.lod}, {cityobj.properties}"
        )
