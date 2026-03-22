from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from clients.operations_client import APIClient
from config import Settings
from schema.devices import DevicesMetaDataSchema, DevicesMetaDataResponseSchema


@pytest.mark.devices
@pytest.mark.integration
class TestDevicesMetaData:
    @allure.title("Devices: retrieve device metadata by IMEI")
    async def test_devices_metadata(
        self,
        api_client: APIClient,
        auth_token: str,
        settings: Settings,
    ) -> None:
        payload = DevicesMetaDataSchema(
            IMEI=settings.imei
        )
        response = await api_client.devices_metadata(payload, token=auth_token)

        assert response.status_code == HTTPStatus.OK

        device_response = DevicesMetaDataResponseSchema.model_validate_json(
            response.text)
        # assert isinstance(device_response.data.IMEI, int)
        # assert isinstance(device_response.data.model, str)
