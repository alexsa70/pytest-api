from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuthenticateRequestSchema(BaseModel):
    """Тело запроса для POST /authenticate."""

    email: str
    password: str


class AuthenticateResponseSchema(BaseModel):
    """Ответ от authentication endpoint."""

    class AuthDataSchema(BaseModel):
        token: str
        organizationId: int

    data: AuthDataSchema
    requestId: UUID

    model_config = ConfigDict(extra="forbid")
