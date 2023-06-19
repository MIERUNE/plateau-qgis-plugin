import lxml.etree as et

from .namespaces import _NS
from .parser import FileParser

if __name__ == "__main__":
    filename = (
        # "/Users/fukada/Downloads/11100_saitama-shi_2022_citygml_1_op/udx/bldg/53396489_bldg_6697_op.gml"
        # "/Users/fukada/Downloads/11100_saitama-shi_2022_citygml_1_op/udx/tran/53396531_tran_6668_op.gml"
        "/Users/fukada/Downloads/15100_niigata-shi_2022_citygml_1_op/udx/frn/56397003_frn_6697_op.gml"
        # "/Users/fukada/Downloads/15100_niigata-shi_2022_citygml_1_op/udx/lsld/563950_lsld_6668_op.gml"
    )
    parser = FileParser(filename)
    for count, cityobj in parser.iter_city_objects():
        types = [pname for pname, _pid in cityobj.processor_path]
        print(
            f"{count} [{' / '.join(types)}] {cityobj.type}, {cityobj.lod}, {cityobj.properties}"
        )
