from __future__ import annotations

import allure
from httpx import Response

from clients.base_client import BaseClient
from schema.operations import AuthenticateRequestSchema
from schema.organizations import OrganizationRetrieveSchema
from schema.devices import DevicesMetaDataSchema
from tools.routes import APIRoutes


class APIClient(BaseClient):
    """Шаблонный async API-клиент."""

    @allure.step("Authenticate user")
    async def authenticate_api(self, payload: AuthenticateRequestSchema) -> Response:
        return await self.post(
            APIRoutes.AUTHENTICATE,
            json=payload.model_dump(mode="json"),
        )

    @allure.step("Organizations: retrieve organization by id")
    async def organizations_retrieve(self, payload: OrganizationRetrieveSchema, token: str) -> Response:
        return await self.get(
            APIRoutes.ORGANIZATIONS_RETRIEVE.format(id=payload.id),
            headers={"Request-ID": str(payload.requestId),
                     "Authorization": f"Bearer {token}"},
        )

    @allure.step("Devices: retrieve device metadata by IMEI")
    async def devices_metadata(self, payload: DevicesMetaDataSchema, token: str) -> Response:
        return await self.get(
            APIRoutes.DEVICES_METADATA.format(IMEI=payload.IMEI),
            headers={"Request-ID": str(payload.requestId),
                     "Authorization": f"Bearer {token}"},
        )
