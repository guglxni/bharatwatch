from pydantic import BaseModel
from typing import Optional, Any

class TendersentryItem(BaseModel):
    tender_id: Optional[str] = None
    title: Optional[str] = None
    department: Optional[str] = None
    estimated_value: Optional[Any] = None
    closing_date: Optional[str] = None
    document_link: Optional[str] = None
