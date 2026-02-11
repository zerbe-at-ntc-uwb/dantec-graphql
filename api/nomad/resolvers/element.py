from typing import List

import strawberry

from ..types import Element, element_resource


def get_elements() -> List[Element]:
    """
    Exposes the _element_dict.
    """
    return element_resource.list


def get_element(symbol: str) -> Element:
    """
    Get element by symbol.
    """
    return element_resource.element_symbol_dict[symbol]
