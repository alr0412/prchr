from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

import db
from repositories import programs as repo
from schemas.errors import ErrorResponse
from schemas.programs import (
    Degree,
    Military,
    ProgramDetail,
    ProgramSummary,
    StudyForm,
)

router = APIRouter(prefix="/programs", tags=["programs"])


@router.get(
    "",
    response_model=list[ProgramSummary],
    responses={400: {"model": ErrorResponse, "description": "Ошибка API"}},
)
async def list_programs(
    query: Annotated[str | None, Query(description="Поиск по названию вуза")] = None,
    city: Annotated[str | None, Query(description="Фильтр по городу")] = None,
    specialty: Annotated[str | None, Query(description="Поиск по названию специальности")] = None,
    exams: Annotated[str | None, Query(description="Поиск по вступительным экзаменам")] = None,
    language: Annotated[str | None, Query(description="Фильтр по языку обучения")] = None,
    studyForm: Annotated[StudyForm | None, Query(description="Форма обучения")] = None,
    degree: Annotated[Degree | None, Query(description="Ступень образования")] = None,
    military: Annotated[Military | None, Query(description="Наличие военной кафедры")] = None,
    minScore: Annotated[int | None, Query(ge=0, le=400, description="Минимальный проходной балл")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    filters = {
        "query": query,
        "city": city,
        "specialty": specialty,
        "exams": exams,
        "language": language,
        "studyForm": studyForm,
        "degree": degree,
        "military": military,
        "minScore": minScore,
    }
    async with db.get_pool().acquire() as conn:
        rows = await repo.list_programs(
            conn, filters=filters, limit=limit, offset=offset
        )
    return [dict(r) for r in rows]


@router.get(
    "/{program_id}",
    response_model=ProgramDetail,
    responses={404: {"model": ErrorResponse, "description": "Ошибка API"}},
)
async def get_program(program_id: int):
    async with db.get_pool().acquire() as conn:
        program = await repo.get_program_detail(conn, program_id)

    if program is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "Program not found",
                "message": f"No program with id {program_id}",
            },
        )
    return program