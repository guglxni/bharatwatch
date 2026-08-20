from pydantic import BaseModel
from typing import Optional

class NaukriAlertItem(BaseModel):
    title: str
    department: str
    notification_date: Optional[str] = None
    last_application_date: Optional[str] = None
    exam_date: Optional[str] = None
    number_of_vacancies: Optional[int] = None
    qualification_required: Optional[str] = None
    official_link: Optional[str] = None
