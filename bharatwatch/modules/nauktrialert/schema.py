from pydantic import BaseModel
from typing import Optional, Any

class NauktrialertItem(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    notification_date: Optional[str] = None
    last_application_date: Optional[str] = None
    exam_date: Optional[str] = None
    number_of_vacancies: Optional[Any] = None
    qualification_required: Optional[str] = None
    official_link: Optional[str] = None
