import json
import os
from typing import List, Dict, Iterable, Optional

import strawberry

from .dataset import Dataset
from .section_def import SectionDef
from .user import User


####### Main Type #######################


@strawberry.type
class Entry(strawberry.relay.Node):
    """
    Stores information from the entry.
    """
    id: strawberry.relay.NodeID[str]
    source_repo: str = "Nomad"
    authors: List[User]
    calc_id: Optional[str] = None
    comment: Optional[str] = None
    datasets: Optional[List[Dataset]] = None
    domain: Optional[str] = None
    entry_create_time: str
    entry_id: str
    entry_name: Optional[str] = None
    entry_type: Optional[str] = None
    external_db: Optional[str] = None
    external_id: Optional[str] = None
    files: List[Optional[str]]
    last_processing_time: str
    license: str
    main_author: User
    mainfile: str
    n_quantities: int
    nomad_commit: str
    nomad_distro_commit_url: Optional[str] = None
    nomad_version: str
    optimade: Optional[str] = None
    origin: str
    parser_name: str
    pid: Optional[str] = None
    processed: bool
    processing_errors: List[Optional[str]]
    publish_time: Optional[str] = None
    published: bool
    quantities: List[str]
    readonly: Optional[bool] = None
    references: List[str]
    results: Optional[str] = None
    section_defs: Optional[List[SectionDef]] = None
    sections: Optional[List[str]] = None
    text_search_contents: Optional[List[Optional[str]]] = None
    upload_create_time: str
    upload_id: str
    upload_name: Optional[str] = None
    viewer_groups: Optional[List[Optional[str]]] = None
    viewers: List[User]
    with_embargo: bool
    writer_groups: Optional[List[Optional[str]]] = None
    writers: List[User]
