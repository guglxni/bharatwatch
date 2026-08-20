from pydantic import BaseModel
from typing import Optional

class CollegecutoffItem(BaseModel):
    institute: str | None = None
    branch: str | None = None
    opening_rank: int | None = None
    closing_rank: int | None = None
    round: str | None = None
    and status: str | None = None
