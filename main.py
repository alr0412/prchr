from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import db
from config import settings
from routers import programs as programs_router
from schemas.errors import ErrorResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_pool(settings.database_url)
    yield
    await db.close_pool()


app = FastAPI(title="Kuda API", lifespan=lifespan)

from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    field = ".".join(str(x) for x in first["loc"][1:])
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "message": f"{field}: {first['msg']}",
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error="HTTP error", message=str(exc.detail)).model_dump(),
    )

@app.get("/health")
async def health():
    async with db.get_pool().acquire() as conn:
        await conn.fetchval("SELECT 1")
    return {"status": "ok"}

app.include_router(programs_router.router)