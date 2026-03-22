from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OrganizationRetrieveSchema(BaseModel):
    """Параметры запроса GET /organizations/{id}."""

    id: int
    requestId: UUID


class OrganizationsResponseSchema(BaseModel):
    """Ответ от organizations endpoint."""

    class OrganizationDataSchema(BaseModel):
        id: int
        name: str
        partnerId: int

    data: OrganizationDataSchema
    requestId: UUID

    model_config = ConfigDict(extra="ignore")
