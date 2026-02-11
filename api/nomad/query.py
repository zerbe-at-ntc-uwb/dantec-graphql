from typing import List

import strawberry

from .resolvers import get_elements, get_element
from .types import Element


@strawberry.type(description="The Nomad query interface")
class Query:
    element: Element = strawberry.field(description="Element with given name.",
                                        resolver=get_element)
    elements: List[Element] = strawberry.field(description="All elements",
                                               resolver=get_elements)

