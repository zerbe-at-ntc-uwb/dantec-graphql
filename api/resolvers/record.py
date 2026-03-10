
from typing import Annotated, Dict, Union

import strawberry

from ..nomad.resolvers import search_nomad_entries
from .inputs import SearchRecordInput, PaginationInput
from .record_connection import RecordConnection
from ..types import RecordSearchError


RecordSearchResponse = Annotated[
    Union[RecordConnection, RecordSearchError],
    strawberry.union("RecordSearchResponse")
]

search_resolvers_map: Dict = {
    "Nomad": search_nomad_entries
}


def search_records(search_record_input: SearchRecordInput,
                   page_input: PaginationInput
                  ) -> RecordSearchResponse:
    """
    A common interface for retrieving searched records from multiple APIs.
    """
    try:
        resolver = search_resolvers_map[page_input.source_repo]
    except KeyError:
        msg: str = "Unsupported source_repo, " + page_input.source_repo
        msg += ".  Supported source_repo keys: "
        msg += ", ".join(search_resolvers_map.keys())
        return RecordSearchError(msg=msg)
    try:
        return resolver(search_record_input, page_input)
    except Exception as e:
        msg: str = "Uncaught error.  Details follow: "
        msg += str(e)
        return RecordSearchError(msg=msg)
