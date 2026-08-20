from pydantic import BaseModel
from typing import Optional

class NauktrialertItem(BaseModel):
    title: str | None = None
    department: str | None = None
    notification_date: str | None = None
    last_application_date: str | None = None
    exam_date: str | None = None
    number_of_vacancies: int | None = None
    qualification_required: str | None = None
    and official_link: str | None = None
