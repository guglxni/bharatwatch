from pydantic import BaseModel
from typing import Optional

class TendersentryItem(BaseModel):
    tender_id: str | None = None
    title: str | None = None
    department: str | None = None
    estimated_value: int | None = None
    closing_date: str | None = None
    and document_link: str | None = None
