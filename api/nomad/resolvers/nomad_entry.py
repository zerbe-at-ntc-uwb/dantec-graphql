"""
Resolver(s) for loading entry objects from Nomad.
"""
import json
from typing import Dict, Iterable, List, Optional

import requests
import strawberry

from ...resolvers.inputs import SearchRecordInput, PaginationInput
from ...types import ForwardPageInfo, Record, RecordConnection, encode_cursor
from .nomad_data_access import NomadEntryQueryAPI


def entries_from_response_dict(response_dict: Dict) -> List[Record]:
    entries : List[Record] = []
    for entry_dict in response_dict["data"]:
        entries.append(Record(id=encode_cursor("Nomad:", entry_dict["entry_id"]),
                              contents={**entry_dict["results"],
                                        "source_repo": "Nomad"}
                             )
                      )
    return entries


def page_info_from_response_dict(response_dict: Dict) -> ForwardPageInfo:
    page_size = response_dict["pagination"]["page_size"]
    response_size = len(response_dict["data"])
    if response_size == 0:
        return ForwardPageInfo(has_next_page=False)
    if response_size < page_size:
        has_next_page = False
    else:
        has_next_page = True
    return ForwardPageInfo(
        has_next_page=has_next_page,
        end_cursor=response_dict["data"][-1]["entry_id"]
    )


def get_nomad_entries(entry_ids: List[str]) -> List[Record]:
    """
    Resolver to load a list of NomadEntry types given their [nomad] entry_id.
    """
    nomad_api = NomadEntryQueryAPI(page_input=PaginationInput(size=len(entry_ids)))
    nomad_api.add("entry_id:any", entry_ids)
    return entries_from_response_dict(nomad_api.post())


def search_nomad_entries(search_record_input: SearchRecordInput,
                         page_input: PaginationInput
                        ) -> RecordConnection:
    """
    Resolver providing access to Nomad's entry search API.
    """
    
    nomad_api = NomadEntryQueryAPI(page_input=page_input)
    nomad_api.translate_query(search_record_input)
    response_dict = nomad_api.post()

    return RecordConnection(
        page_info=page_info_from_response_dict(response_dict),
        records=entries_from_response_dict(response_dict)
    )
