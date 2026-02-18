import os
from typing import List, Dict, Iterable, Optional, Tuple

import strawberry

####### Main Type #######################


@strawberry.type
class Dataset(strawberry.relay.Node):
    """
    Stores information from the entry.
    """
    id: strawberry.relay.NodeID[int]
    source_repo: str = "Nomad"
    dataset_create_time: str
    dataset_id: str
    dataset_modified_time: Optional[str]
    dataset_name: str
    dataset_type: Optional[str]
    doi: Optional[str]
    m_annotations: Optional[List[Tuple[str, List[str]]]]
