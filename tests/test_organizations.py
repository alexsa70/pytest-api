from http import HTTPStatus
from uuid import uuid4

import allure
import pytest

from clients.operations_client import APIClient
from config import Settings
from schema.organizations import OrganizationRetrieveSchema, OrganizationsResponseSchema


@pytest.mark.organizations
@pytest.mark.integration
class TestOrganizations:
    @allure.title("Organizations: retrieve organization by id")
    async def test_organizations_retrieve(
        self,
        api_client: APIClient,
        auth_token: str,
        settings: Settings,
    ) -> None:
        payload = OrganizationRetrieveSchema(
            id=settings.org_id,
            requestId=uuid4(),
        )
        response = await api_client.organizations_retrieve(payload, token=auth_token)

        assert response.status_code == HTTPStatus.OK

        org_response = OrganizationsResponseSchema.model_validate_json(response.text)
        assert isinstance(org_response.data.id, int)
        assert isinstance(org_response.data.name, str)
        assert isinstance(org_response.data.partnerId, int)
