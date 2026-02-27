from typing import Literal, Optional

from pydantic import BaseModel, Field, StrictInt


class NomadPaginationInput(BaseModel):
    """
    Nomad uses pagination input for querying.
    """
    page_size: Optional[StrictInt] = Field(10, gt=-1, alias="size")
    page_after_value: Optional[str] = Field(None, alias="after")
    order_by: Optional[str] = Field(None)
    order: Optional[Literal["asc", "desc"]] = Field(None)

    def dict(self):
        return BaseModel.dict(self, exclude_none=True)
