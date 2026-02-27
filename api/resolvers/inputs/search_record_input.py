"""
Defines how the SearchEntryInput will look.
"""
from inspect import cleandoc
from typing import List, Optional

import strawberry

@strawberry.input(description=cleandoc("""
                   Common interface for passing potential
                   information to control filtering of Records.
                   All fields are optional and all values undergo
                   "and" logic joins.  The fields are as follows:
                     authors: list of authors for the record.
                     elements: list of elments within the material. 
                     method_name: Name of method from the record.
                     simulation_program: Name of simulation program
                                         used within record.
                  """))
class SearchRecordInput:
    authors: Optional[List[str]] = None
    elements: Optional[List[str]] = None
    method_name: Optional[str] = None
    simulation_program: Optional[str] = None
