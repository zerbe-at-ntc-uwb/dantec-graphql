import os
from typing import List, Dict, Iterable

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
    appearance: str
    atomic_mass: float 
    boil: float 
    category: str
    color: str
    density: float
    discovered_by: str
    melt: float
    molar_heat: float
    named_by: str
    number: int
    period: int
    phase: str
    source: str
    spectral_img: str
    summary: str
    symbol: str
    xpos: int
    ypos: int
    shells: List[int]


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
