"""
Resolver(s) for loading entry objects from Nomad.
"""
import json
from typing import Dict, Iterable, List, Optional, Tuple, TypeAlias

import requests
import strawberry

from ...resolvers.inputs import SearchRecordInput, PaginationInput
from ...resolvers.record_connection import RecordConnection
from ...types import Record, StandardCursorFactory
from .nomad_data_access import NomadEntryQueryAPI


EntryInfo: TypeAlias = Tuple[StandardCursorFactory, List[Record]]
PageInfo: TypeAlias = Tuple[str, str, bool]


def entries_from_response_dict(response_dict: Dict) -> EntryInfo:
    data = response_dict["data"]
    if len(data) == 0:
        return None, []

    entry_cursor_factory = StandardCursorFactory("Nomad", "Record")
    pack = entry_cursor_factory.pack
    entries : List[Record] = []
    for entry_dict in response_dict["data"]:
        entries.append(Record(cursor=pack(entry_dict["entry_id"]),
                              contents={**entry_dict["results"],
                                        "source_repo": "Nomad"}
                             )
                      )
    return entry_cursor_factory, entries


def page_info_from_response_dict(response_dict: Dict) -> PageInfo:
    data = response_dict["data"]
    response_size = len(data)
    if response_size == 0:
        first_id = None
        last_id = None
        has_next_page = False
    else:
        id_key = "entry_id" 
        first_id = data[0][id_key]
        last_id = data[-1][id_key]
        page_size = response_dict["pagination"]["page_size"]
        if response_size < page_size:
            has_next_page = False
        else:
            has_next_page = True
    return first_id, last_id, has_next_page


def get_nomad_entries(entry_ids: List[str]) -> EntryInfo:
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
    entry_cursor_factory, entries = entries_from_response_dict(response_dict)
    first_id, last_id, has_next_page = page_info_from_response_dict(response_dict)

    return RecordConnection.resolve_connection(entries,
                                               entry_cursor_factory,
                                               first_id=first_id,
                                               last_id=last_id,
                                               has_next_page=has_next_page)
