-- ============================================================
-- Схема БД kuda_post
-- Идемпотентно: можно запускать многократно
-- ============================================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ---------- Университеты ----------
CREATE TABLE IF NOT EXISTS universities (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    short_name  TEXT NOT NULL
);

-- ---------- Программы ----------
CREATE TABLE IF NOT EXISTS programs (
    id                  SERIAL PRIMARY KEY,
    university_id       INT NOT NULL REFERENCES universities(id),
    faculty             TEXT NOT NULL,
    title               TEXT NOT NULL,
    short_name          TEXT NOT NULL,
    code                TEXT NOT NULL UNIQUE,
    budget_score        INT,
    paid_score          INT,
    city                TEXT NOT NULL,
    degree              TEXT NOT NULL,
    study_form          TEXT NOT NULL,
    duration            TEXT NOT NULL,
    exams               TEXT NOT NULL,
    plan                TEXT NOT NULL,
    language            TEXT NOT NULL,
    military_department TEXT NOT NULL,
    dormitory           TEXT NOT NULL,
    address             TEXT NOT NULL,
    phone               TEXT NOT NULL,
    website             TEXT NOT NULL,
    description         TEXT
);

-- ---------- История проходных баллов ----------
CREATE TABLE IF NOT EXISTS program_score_history (
    program_id  INT  NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
    year        TEXT NOT NULL,
    score       INT  NOT NULL,
    PRIMARY KEY (program_id, year)
);

-- ---------- Индексы под фильтры ----------
CREATE INDEX IF NOT EXISTS idx_programs_city         ON programs(city);
CREATE INDEX IF NOT EXISTS idx_programs_degree       ON programs(degree);
CREATE INDEX IF NOT EXISTS idx_programs_study_form   ON programs(study_form);
CREATE INDEX IF NOT EXISTS idx_programs_language     ON programs(language);
CREATE INDEX IF NOT EXISTS idx_programs_military     ON programs(military_department);
CREATE INDEX IF NOT EXISTS idx_programs_budget_score ON programs(budget_score);

-- ---------- Триграммы для ILIKE '%...%' ----------
CREATE INDEX IF NOT EXISTS idx_universities_name_trgm  ON universities USING gin(name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_universities_short_trgm ON universities USING gin(short_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_programs_title_trgm     ON programs     USING gin(title gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_programs_exams_trgm     ON programs     USING gin(exams gin_trgm_ops);