from pydantic import BaseModel
from typing import Optional, Any

class StartuppulseItem(BaseModel):
    title: Optional[str] = None
    ministry: Optional[str] = None
    scheme_type: Optional[str] = None
    deadline: Optional[str] = None
    summary: Optional[str] = None
    link: Optional[str] = None
