from typing import List

import strawberry

from .resolvers import get_elements, get_element, search_nomad_entries
from .types import Element, Entry


@strawberry.type(description="The Nomad query interface")
class Query:
    element: Element = strawberry.field(description="Element with given name.",
                                        resolver=get_element)
    elements: List[Element] = strawberry.field(description="All elements",
                                               resolver=get_elements)

    entries: List[Entry] = strawberry.field(
            description="Interface to NomadSearch API",
            resolver=search_nomad_entries)
