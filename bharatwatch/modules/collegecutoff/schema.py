from pydantic import BaseModel
from typing import Optional, Any

class CollegecutoffItem(BaseModel):
    institute: Optional[str] = None
    branch: Optional[str] = None
    opening_rank: Optional[Any] = None
    closing_rank: Optional[Any] = None
    round: Optional[str] = None
    status: Optional[str] = None
