from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Краткое описание ошибки",
        examples=["Program not found"],
    )
    message: str = Field(
        ...,
        description="Детали ошибки",
        examples=["No program with id 999"],
    )