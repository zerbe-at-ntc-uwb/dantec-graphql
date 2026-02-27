from inspect import cleandoc
from typing import List, Literal, Optional


import strawberry

@strawberry.input(description=cleandoc("""
                   Pagination interface for passing potential
                   information to the data source.
                   This is forward pagination only.
                   "Backward" pagination is not supported by the
                   API --- if you want to have the ability to
                   go "backwards", you need to cache the results
                   locally.
                   All fields are optional and are as follows:
                     after: indicates the string identifying the record
                            after which results will be displayed.
                            If not supplied, tells the data source
                            to start from the beginning.
                     size: indicates the number of records pulled.
                  """))
class PaginationInput:
    source_repo: str = strawberry.field(
        description="Name of the source repo to pull from."
    )
    size: Optional[int] = strawberry.field(
        default=10,
        description="Number of results returned."
    )
    after: Optional[str]  = strawberry.field(
        default=None,
        description="Unique id in repo after which results are returned."
    )
