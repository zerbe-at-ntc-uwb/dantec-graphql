from typing import Iterable, Optional

import strawberry

from ..types import StandardCursorFactory, Record

@strawberry.type
class RecordConnection(strawberry.relay.Connection[Record]):
    """
    Applies the Relay connection convention to be exploited by the UI.
    """

    @classmethod
    def resolve_connection(
        cls,
        nodes: Iterable[Record],
        record_cursor_factory: StandardCursorFactory,
        info: Optional[strawberry.Info] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        first: Optional[int] = None,
        last: Optional[int] = None,
        first_id: Optional[str] = None,
        last_id: Optional[str] = None,
        has_next_page: bool = None
    ):
        """
        Necessary method to interface with the Relay Connection Framework.
        Four additional key words beyond the ones needed for this function
        are present:
            record_cursor_factory:  Factory for converting between
                                    cursors and ids.
            first_id: The first unique string from the source repo for the specific
                     object type --- skips the decoding step.
            last_id: The last unique string from the source repo for the specific
                     object type --- skips the decoding step.
            has_next_page:  This can [potentially] be passed by the API query
                            that initially fills the nodes. 
        """
        edges = [strawberry.relay.Edge(node=n,
                                       cursor=n.cursor
                                      ) for n in nodes]
        if len(nodes) == 0:
            first_id = None
            last_id = None
            if has_next_page is None:
                has_next_page = False
        else:
            unpack = record_cursor_factory.unpack
            if first_id is None:
                first_id = unpack(nodes[-1].cursor)
            if last_id is None:
                last_id = unpack(nodes[-1].cursor)
            if has_next_page is None:
                has_next_page = True
        return cls(edges=edges,
                   page_info=strawberry.relay.PageInfo(
                     start_cursor=first_id,
                     end_cursor=last_id,
                     has_previous_page=False,
                     has_next_page=has_next_page))
