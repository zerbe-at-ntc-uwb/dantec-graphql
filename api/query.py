import typing

import strawberry

from .resolvers.record_connection import RecordConnection
from .resolvers import RecordSearchResponse, search_records

@strawberry.type(description="The full query interface")
class Query:
    records: RecordSearchResponse = strawberry.field(
        description="The search interface for both Dantec and Nomad.",
        resolver=search_records
    )
