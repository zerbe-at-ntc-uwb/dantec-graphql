from typing import List, Optional

import strawberry


@strawberry.type
class ForwardPageInfo:
    has_next_page: bool = strawberry.field(
        description = "Are there more items at the source?"
    )

    end_cursor: Optional[str] = strawberry.field(
        description = "When there are more items, the current last id."
    )
