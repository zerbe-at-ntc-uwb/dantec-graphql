"""
Provides an interface for treating a JSON file
as a data source.
"""
import json
from typing import Any, List

import strawberry


####### Main class #######################
class JSONResource:
    """
    Accesses the database in a file with lazy loading.
    
    Attributes:
        _cls: a strawberry.relay.Node class
            The class used to create the object in the list.

        _filepath: str
            JSON-formatted file where data is stored.

        _path: list or strings or ints
            Optional list to [partially] derefence object
            that is a list of dictionaries to be used for
            initialization of the class object.

        _list: any
            The list of objects (once loaded and derefenced).
    """

    def __init__(self, cls: Any,
                 filepath: str, path: List[str|int]=[]):
        if (not issubclass(cls, strawberry.relay.Node)):
            raise TypeError("Cls must inherit from strawberry.relay.Node")
        self._cls = cls
        self._filepath = filepath
        self._path = path
        self._list = None

    @property
    def list(self) -> List[strawberry.relay.Node]:
        """
        Lazy load data and/or return list of Objects.
        """
        if self._list is None:
            with open(self._filepath, "r") as fh:
                json_obj = json.load(fh)
                # Optionally dereference json_obj with path
                for key in self._path:
                    json_obj = json_obj[key]
                self._list = [self._cls(id=i, **val) for i, val in
                                        enumerate(json_obj)]
        return self._list
