from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Degree(str, Enum):
    bachelor = "Бакалавриат"
    master = "Магистратура"
    special = "Специальное"


class StudyForm(str, Enum):
    full_time = "Очная"
    part_time = "Заочная"


class Military(str, Enum):
    yes = "Есть"
    no = "Нет"


class ScoreHistoryItem(BaseModel):
    year: str
    score: int


class ProgramSummary(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    university: str
    shortName: str
    title: str
    code: str
    budgetScore: int | None = None
    paidScore: int | None = None
    city: str
    degree: Degree
    studyForm: StudyForm


class ProgramDetail(ProgramSummary):
    faculty: str
    duration: str
    exams: str
    plan: str
    language: str
    militaryDepartment: Military
    dormitory: str
    address: str
    phone: str
    website: str
    description: str | None = None
    scoreHistory: list[ScoreHistoryItem] = Field(default_factory=list)

class PaginatedPrograms(BaseModel):
    items: list[ProgramSummary]
    total: int
    limit: int
    offset: int