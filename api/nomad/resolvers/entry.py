import json
from typing import Optional, List, Dict, Tuple

import requests
import strawberry

from ..types import Entry


def make_nomad_query(json_query: Dict, page_size) -> Dict:
    base_url: str = 'http://nomad-lab.eu/prod/v1/api/v1'
    request_json = {"query": json_query}
    request_json["pagination"] = {"page_size": page_size}
    return requests.post(f'{base_url}/entries/query', json=request_json).json()


def search_nomad_entries(json_query_str: str, page_size: int=10) -> List[Entry]:
    entries = []
    response = make_nomad_query(json.loads(json_query_str), page_size)
    for entry_dict in response["data"]:
        try:
            entry_dict["results"] = json.dumps(entry_dict["results"])
        except KeyError:
            pass
        try:
            entry_dict["optimade"] = json.dumps(entry_dict["optimade"])
        except KeyError:
            pass
        entries.append(Entry(id=entry_dict["entry_id"], **entry_dict))
    return entries
