from typing import Dict

import strawberry

from .cursor import encode_cursor

####### Main Type #######################


@strawberry.type(
    description="Basic record with contents for viewing."
)
class Record(strawberry.relay.Node):
    cursor: strawberry.relay.NodeID[str]
    contents: strawberry.scalars.JSON = strawberry.field(
        description="JSON formatted contents of record."
    )

