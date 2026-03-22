from http import HTTPStatus

import allure
import pytest

from clients.operations_client import APIClient
from schema.operations import AuthenticateRequestSchema


@pytest.mark.template
class TestAuthTemplate:
    @allure.title("Template: local auth payload schema check")
    def test_auth_payload_schema(self) -> None:
        payload = AuthenticateRequestSchema(
            email="user@example.com",
            password="secret",
        )

        assert isinstance(payload.email, str)
        assert isinstance(payload.password, str)

    @pytest.mark.integration
    @allure.title("Template: authenticate")
    async def test_authenticate(
        self,
        auth_token: str,
    ) -> None:
        assert auth_token

    @pytest.mark.integration
    @allure.title("Template: authenticate with incorrect email")
    async def test_authenticate_incorrect_email(
        self,
        api_client: APIClient,
        auth_payload: AuthenticateRequestSchema,
    ) -> None:
        invalid_payload = AuthenticateRequestSchema(
            email="incorrect_email@example.com",
            password=auth_payload.password,
        )
        response = await api_client.authenticate_api(invalid_payload)

        assert response.status_code != HTTPStatus.OK

    @pytest.mark.integration
    @allure.title("Template: authenticate with incorrect password")
    async def test_authenticate_incorrect_password(
        self,
        api_client: APIClient,
        auth_payload: AuthenticateRequestSchema,
    ) -> None:
        invalid_payload = AuthenticateRequestSchema(
            email=auth_payload.email,
            password="incorrect_password",
        )
        response = await api_client.authenticate_api(invalid_payload)

        assert response.status_code != HTTPStatus.OK

    @pytest.mark.integration
    @allure.title("Template: authenticate with empty payload")
    async def test_authenticate_empty_payload(
        self,
        api_client: APIClient,
    ) -> None:
        empty_payload = AuthenticateRequestSchema(
            email="",
            password="",
        )
        response = await api_client.authenticate_api(empty_payload)

        assert response.status_code != HTTPStatus.OK
