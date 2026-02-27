from typing import List

import strawberry
from .forward_page_info import ForwardPageInfo

####### Main Type #######################


@strawberry.type(
    description="Basic record with contents for viewing."
)
class Record:
    id: str
    contents: strawberry.scalars.JSON = strawberry.field(
        description="JSON formatted contents of record."
    )


@strawberry.type
class RecordConnection:
    page_info: ForwardPageInfo = strawberry.field(
        description="Information to aid in forward pagination across sources."
    )

    records: List[Record] = strawberry.field(
        description="A list of records from the connection."
    )
