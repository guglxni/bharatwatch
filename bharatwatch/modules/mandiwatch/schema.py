from pydantic import BaseModel
from typing import Optional, Any

class MandiwatchItem(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    mandi: Optional[str] = None
    crop: Optional[str] = None
    variety: Optional[str] = None
    min_price: Optional[Any] = None
    max_price: Optional[Any] = None
    modal_price: Optional[Any] = None
    date: Optional[str] = None
