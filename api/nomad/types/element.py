import os
from typing import List, Dict, Iterable, Optional

import strawberry

from api.utils.json_resource import JSONResource


####### Main Type #######################


@strawberry.type
class Element(strawberry.relay.Node):
    """
    Stores information from the periodic table of elements.
    """
    id: strawberry.relay.NodeID[int]
    source_repo: str = "Nomad"
    name: str
    appearance: Optional[str]
    atomic_mass: Optional[float] 
    boil: Optional[float] 
    category: Optional[str]
    color: Optional[str]
    density: Optional[float]
    discovered_by: Optional[str]
    melt: Optional[float]
    molar_heat: Optional[float]
    named_by: Optional[str]
    number: Optional[int]
    period: Optional[int]
    phase: Optional[str]
    source: Optional[str]
    spectral_img: Optional[str]
    summary: Optional[str]
    symbol: str
    xpos: Optional[int]
    ypos: Optional[int]
    shells: Optional[List[int]]


    @classmethod
    def resolve_nodes(
        cls,
        *,
        info: strawberry.Info,
        node_ids: Iterable[str],
        required: bool = False,
    ):
        """
        Pattern for Relay for resolving pulling objects from node ID.
        """
        el_id_dict: Dict[int, Element] = get_element_resource().element_id_dict

        return [
            el_id_dict[int(nid)] if required
            else el_id_dict().get(nid) for nid in node_ids
        ]


####### Class for loading and prepping JSON element data #######################


class ElementResource(JSONResource):
    """
    Accesses the "database in the elementData.json file.
    """
    _this_dir: str = os.path.dirname(__file__)
    _elements_filepath: str = os.path.join(_this_dir, "json_files", "elementData.json")
    _deref_path = ["elements"]  # Data will now point to a list not dict.

    def __init__(self):
        super().__init__(Element, self._elements_filepath,
                         self._deref_path)
        # Initialize lazy loading of properties.
        self._element_symbol_dict: Dict[str, Element] = {}
        self._element_id_dict: Dict[int, Element] = {}

    @property
    def element_symbol_dict(self) -> Dict[str, Element]:
        """
        Lazy load a dictionary of elements keyed by name.
        """
        if len(self._element_symbol_dict) == 0:
            for element in self.list:
                self._element_symbol_dict[element.symbol] = element
        return self._element_symbol_dict

    @property
    def element_id_dict(self) -> Dict[int, Element]:
        """
        Lazy load a dictionary of elements keyed by name.
        """
        if len(self._element_id_dict) == 0:
            for element in self.list:
                self._element_id_dict[int(element.id)] = element
        return self._element_id_dict


element_resource = ElementResource()


def get_element_resource():
    return element_resource
