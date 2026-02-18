import strawberry

####### Main Type #######################


@strawberry.type
class SectionDef(strawberry.relay.Node):
    """
    Stores information from the entry.
    """
    id: strawberry.relay.NodeID[int]
    source_repo: str = "Nomad"
    used_directly: bool
    definition_id: str
    definition_qualified_name: str
