from http import HTTPStatus
import allure
import pytest

from clients.operations_client import OperationsClient
from schema.operations import CreateOperationSchema, OperationSchema, UpdateOperationSchema, OperationsSchema
from tools.assertions.base import assert_status_code
from tools.assertions.operations import assert_create_operation, assert_operation
from tools.assertions.schema import validate_json_schema


@pytest.mark.operations
class TestOperations:
    @pytest.mark.regression
    @pytest.mark.xfail(reason="sampleapis.com contains records with corrupted date format")
    @allure.title("Get operations")
    async def test_get_operations(self, operations_client: OperationsClient):
        response = await operations_client.get_operations_api()

        assert_status_code(response.status_code, HTTPStatus.OK)
        validate_json_schema(
            response.json(), OperationsSchema.model_json_schema())

    @pytest.mark.regression
    @allure.title("Get operation")
    async def test_get_operation(
            self,
            operations_client: OperationsClient,
            function_operation: OperationSchema
    ):
        response = await operations_client.get_operation_api(function_operation.id)
        operation = OperationSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_operation(operation, function_operation)
        validate_json_schema(response.json(), operation.model_json_schema())

    @pytest.mark.regression
    @allure.title("Create operation")
    async def test_create_operation(self, operations_client: OperationsClient):
        request = CreateOperationSchema()
        response = await operations_client.create_operation_api(request)
        operation = OperationSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.CREATED)
        assert_create_operation(operation, request)
        validate_json_schema(response.json(), operation.model_json_schema())

    @allure.title("Update operation")
    async def test_update_operation(
            self,
            operations_client: OperationsClient,
            function_operation: OperationSchema
    ):
        request = UpdateOperationSchema()
        response = await operations_client.update_operation_api(
            function_operation.id, request)
        operation = OperationSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_operation(operation, request)
        validate_json_schema(response.json(), operation.model_json_schema())

    @pytest.mark.regression
    @allure.title("Delete operation")
    async def test_delete_operation(
            self,
            operations_client: OperationsClient,
            function_operation: OperationSchema
    ):
        delete_response = await operations_client.delete_operation_api(
            function_operation.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = await operations_client.get_operation_api(
            function_operation.id)
        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
