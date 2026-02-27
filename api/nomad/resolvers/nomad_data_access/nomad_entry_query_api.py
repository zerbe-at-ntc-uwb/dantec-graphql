"""
Interface to simplify data access through Nomad API.
"""

from typing import Any, Dict, List, Tuple

import requests

from .nomad_pagination import NomadPaginationInput
from ....resolvers.inputs import SearchRecordInput, PaginationInput


class NomadEntryQueryAPI:
    _base_url = 'http://nomad-lab.eu/prod/v1/api/v1/entries/query'

    def __init__(self, query: Dict ={},
                 page_input: PaginationInput
                 = PaginationInput(source_repo="Nomad")):
        self._query = query
        self._pagination = NomadPaginationInput(size=page_input.size,
                                                after=page_input.after)

    def __len__(self):
        return len(self._query)

    def insert(self, key: str , value: Any):
        if (isinstance(value, list)):
            try:
                self._query[key].extend(value)
            except KeyError:
                self._query[key] = value
        elif (isinstance(value, dict)):
            try:
                self._query[key].update(value)
            except KeyError:
                self._query[key] = value
        else:
            self._query[key] = value

    def dict(self) -> Dict:
        return {"query": self._query,
                "pagination": self._pagination.dict()}

    def post(self) -> Dict:
        if len(self) < 1:
            msg: str = "The nomad query needs to be initialized before use."
            raise SyntaxError(msg)
        return requests.post(f'{self._base_url}',
                             json=self.dict()
                            ).json()

    def translate_query(self, sr_in: SearchRecordInput) -> None:
        """
        Translates the SearchRecordInput fields
        to the needed language of the query object and inserts the data
        to the query object.
        """
        if sr_in.authors and (len(sr_in.authors) > 0):
            self.insert("authors", sr_in.authors)
        if sr_in.elements and len(sr_in.elements) > 0:
            self.insert("results.material.elements", sr_in.elements)
        if sr_in.method_name:
            self.insert("results.method.method_name", sr_in.method_name)
        if sr_in.simulation_program:
            self.insert("results.method.simulation.program_name",
                        sr_in.simulation_program)
