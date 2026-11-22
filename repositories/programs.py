from typing import Any

import asyncpg

# ---------- Список программ ----------

BASE_SELECT = """
    SELECT
        p.id,
        u.name              AS "university",
        u.short_name        AS "shortName",
        p.title,
        p.code,
        p.budget_score      AS "budgetScore",
        p.paid_score        AS "paidScore",
        p.city,
        p.degree,
        p.study_form        AS "studyForm",
        p.exams,
        p.language,
        p.military_department AS "militaryDepartment"
    FROM programs p
    JOIN universities u ON u.id = p.university_id
"""


def _build_filters(filters: dict[str, Any]) -> tuple[str, list[Any]]:
    conditions: list[str] = []
    params: list[Any] = []

    def add(cond: str, value: Any) -> None:
        params.append(value)
        conditions.append(cond.format(idx=len(params)))

    if filters.get("query"):
        add(
            "(u.name ILIKE ${idx} OR u.short_name ILIKE ${idx})",
            f"%{filters['query']}%",
        )
    if filters.get("city"):
        add("p.city = ${idx}", filters["city"])
    if filters.get("specialty"):
        add("p.title ILIKE ${idx}", f"%{filters['specialty']}%")
    if filters.get("exams"):
        add("p.exams ILIKE ${idx}", f"%{filters['exams']}%")
    if filters.get("language"):
        add("p.language = ${idx}", filters["language"])
    if filters.get("studyForm"):
        add("p.study_form = ${idx}", filters["studyForm"].value)
    if filters.get("degree"):
        add("p.degree = ${idx}", filters["degree"].value)
    if filters.get("military"):
        add("p.military_department = ${idx}", filters["military"].value)
    if filters.get("minScore") is not None:
        add("p.budget_score <= ${idx}", filters["minScore"])

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


async def list_programs(
    conn: asyncpg.Connection,
    *,
    filters: dict[str, Any],
    limit: int,
    offset: int,
) -> list[asyncpg.Record]:
    where, params = _build_filters(filters)
    limit_idx = len(params) + 1
    offset_idx = len(params) + 2
    sql = f"""
        {BASE_SELECT}
        {where}
        ORDER BY p.title
        LIMIT ${limit_idx} OFFSET ${offset_idx}
    """
    params.extend([limit, offset])
    return await conn.fetch(sql, *params)


async def count_programs(conn: asyncpg.Connection, *, filters: dict[str, Any]) -> int:
    where, params = _build_filters(filters)
    sql = f"""
        SELECT COUNT(*)
        FROM programs p
        JOIN universities u ON u.id = p.university_id
        {where}
    """
    return await conn.fetchval(sql, *params)


# ---------- Одна программа ----------

PROGRAM_DETAIL_SELECT = """
    SELECT
        p.id,
        u.short_name           AS "university",
        u.short_name           AS "shortName",
        p.faculty,
        p.title,
        p.code,
        p.budget_score         AS "budgetScore",
        p.paid_score           AS "paidScore",
        p.city,
        p.degree,
        p.study_form           AS "studyForm",
        p.duration,
        p.exams,
        p.plan,
        p.language,
        p.military_department  AS "militaryDepartment",
        p.dormitory,
        p.address,
        p.phone,
        p.website,
        p.description
    FROM programs p
    JOIN universities u ON u.id = p.university_id
    WHERE p.id = $1
"""

SCORE_HISTORY_SELECT = """
    SELECT year, score
    FROM program_score_history
    WHERE program_id = $1
    ORDER BY year
"""


async def get_program_detail(
    conn: asyncpg.Connection,
    program_id: int,
) -> dict[str, Any] | None:
    row = await conn.fetchrow(PROGRAM_DETAIL_SELECT, program_id)
    if row is None:
        return None

    history = await conn.fetch(SCORE_HISTORY_SELECT, program_id)

    data = dict(row)
    data["scoreHistory"] = [dict(h) for h in history]
    return data