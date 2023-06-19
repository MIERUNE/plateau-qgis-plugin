from dataclasses import dataclass
from functools import cached_property
from typing import Iterable, Literal, Optional

import lxml.etree as et

from ..namespaces import _NS, to_qualified_name


@dataclass
class LODDetection:
    """各LODの存在を確認するための XML Paths を列挙する"""

    lod0: Optional[list[str]] = None
    lod1: Optional[list[str]] = None
    lod2: Optional[list[str]] = None
    lod3: Optional[list[str]] = None
    lod4: Optional[list[str]] = None
    lod_n: Optional[str] = None


@dataclass
class Emission:
    elem_paths: list[str]
    geometry_loader: Literal["polygons"] = "polygons"


@dataclass
class Emissions:
    """LODごとの地物の出力について記述する"""

    lod0: Optional[Emission] = None
    lod1: Optional[Emission] = None
    lod2: Optional[Emission] = None
    lod3: Optional[Emission] = None
    lod4: Optional[Emission] = None


@dataclass
class ChildrenPaths:
    lod0: Optional[list[str]] = None
    lod1: Optional[list[str]] = None
    lod2: Optional[list[str]] = None
    lod3: Optional[list[str]] = None
    lod4: Optional[list[str]] = None


@dataclass
class Attribute:
    name: str
    xpath: str
    datatype: Literal["string", "integer", "double", "datetime", "[]string"]
    codelist: Optional[str] = None


@dataclass
class FieldDefinition:
    name: str
    datatype: Literal["string", "integer", "double", "datetime", "[]string"]


@dataclass
class TableDefinition:
    fields: list[FieldDefinition]


@dataclass
class ProcessorDefinition:
    id: str
    target_elements: list[str]  # "tran:Road"
    lod_detection: LODDetection
    attributes: list[Attribute]
    emissions: Emissions
    children: Optional[ChildrenPaths] = None

    def get_lods(self, elem: et._Element):
        det = self.lod_detection
        if det.lod_n:
            lod = int(elem.find(det.lod_n, _NS).text)
            return [lod == i for i in range(5)]
        return (
            bool(det.lod0 and any(elem.find(p, _NS) is not None for p in det.lod0)),
            bool(det.lod1 and any(elem.find(p, _NS) is not None for p in det.lod1)),
            bool(det.lod2 and any(elem.find(p, _NS) is not None for p in det.lod2)),
            bool(det.lod3 and any(elem.find(p, _NS) is not None for p in det.lod3)),
            bool(det.lod4 and any(elem.find(p, _NS) is not None for p in det.lod4)),
        )

    @cached_property
    def emissions_list(self) -> tuple[Optional[Emission], ...]:
        emissions = self.emissions
        return (
            emissions.lod0,
            emissions.lod1,
            emissions.lod2,
            emissions.lod3,
            emissions.lod4,
        )

    @cached_property
    def children_paths_list(self) -> tuple[Optional[list[str]], ...]:
        children = self.children
        if children is None:
            return (None, None, None, None, None)
        return (
            children.lod0,
            children.lod1,
            children.lod2,
            children.lod3,
            children.lod4,
        )


class ProcessorRegistory:
    def __init__(self, processors: Optional[Iterable[ProcessorDefinition]] = None):
        self._tag_map = {}
        self._id_map = {}
        if processors:
            for processor in processors:
                self.register_processor(processor)

    def register_processor(self, processor: ProcessorDefinition):
        self._id_map[processor.id] = processor
        for prefixed_name in processor.target_elements:
            qualified_name = to_qualified_name(prefixed_name)
            self._tag_map[prefixed_name] = processor
            self._tag_map[qualified_name] = processor

    def get_processor_by_tag(self, target_tag: str) -> Optional[ProcessorDefinition]:
        return self._tag_map.get(target_tag)

    def get_processor_by_id(self, _id: str) -> ProcessorDefinition:
        return self._id_map[_id]

    def get_table_definition(self, processor_path: list[tuple[str, str]]):
        processor = self.get_processor_by_id(processor_path[-1][0])
        fields = [
            FieldDefinition("id", "string"),
            FieldDefinition("name", "string"),
        ]
        for attr in processor.attributes:
            fields.append(FieldDefinition(attr.name, attr.datatype))

        return TableDefinition(fields=fields)
