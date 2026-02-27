from typing import List, Optional

import strawberry


@strawberry.type
class ForwardPageInfo:
    has_next_page: bool = strawberry.field(
        description="When paginating forwards, are there more items?"
    )

    end_cursor: Optional[str] = strawberry.field(
        description="The cursor to continue."
    )
