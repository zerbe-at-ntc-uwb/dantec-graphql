import os

import strawberry

####### Main Type #######################


@strawberry.type
class User(strawberry.relay.Node):
    """
    Stores information from the entry.
    """
    id: strawberry.relay.NodeID[int]
    source_repo: str = "Nomad"
    user_id: str
    name: str
