from typing import List

import strawberry

from .resolvers import get_elements, get_element, search_nomad_entries
from .types import Element
from ..types import RecordConnection


@strawberry.type(description="The Nomad query interface")
class Query:
    element: Element = strawberry.field(description="Element with given name.",
                                        resolver=get_element)
    elements: List[Element] = strawberry.field(description="All elements",
                                               resolver=get_elements)

    records: RecordConnection = strawberry.field(
        description="Interface with Nomad entry query API.",
        resolver=search_nomad_entries
    )
