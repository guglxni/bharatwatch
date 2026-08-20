from pydantic import BaseModel
from typing import Optional

class StartuppulseItem(BaseModel):
    title: str | None = None
    ministry: str | None = None
    scheme_type: str | None = None
    deadline: str | None = None
    summary: str | None = None
    and link: str | None = None
