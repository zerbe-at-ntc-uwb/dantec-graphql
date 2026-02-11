import typing

import strawberry

from .nomad import Query as NomadQuery

@strawberry.type(description="The full query interface")
class Query(NomadQuery):
    pass
