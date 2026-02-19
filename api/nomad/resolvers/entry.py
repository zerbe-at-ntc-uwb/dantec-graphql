import json
from typing import Optional, List, Dict, Tuple

import requests
import strawberry

from ..types import Entry


def make_nomad_query(json_query: Dict) -> Dict:
    base_url: str = 'http://nomad-lab.eu/prod/v1/api/v1'
    return requests.post(f'{base_url}/entries/query', json=json_query).json()


def search_nomad_entries(json_query_str: str) -> List[Entry]:
    entries = []
    response = make_nomad_query(json.loads(json_query_str))
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
