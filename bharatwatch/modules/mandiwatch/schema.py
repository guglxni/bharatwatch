from pydantic import BaseModel
from typing import Optional

class MandiwatchItem(BaseModel):
    state: str | None = None
    district: str | None = None
    mandi: str | None = None
    crop: str | None = None
    variety: str | None = None
    min_price: int | None = None
    max_price: int | None = None
    modal_price: int | None = None
    and date: str | None = None
