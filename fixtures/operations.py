from typing import AsyncIterator

import pytest_asyncio

from clients.base_client import get_http_client
from clients.operations_client import OperationsClient
from config import Settings
from schema.operations import OperationSchema


@pytest_asyncio.fixture
async def operations_client(settings: Settings) -> AsyncIterator[OperationsClient]:
    """
    Фикстура создаёт асинхронный HTTP-клиент и оборачивает его в OperationsClient.
    AsyncClient закрывается автоматически после теста.
    """
    async with get_http_client(settings.fake_bank_http_client) as http_client:
        yield OperationsClient(client=http_client)


@pytest_asyncio.fixture
async def function_operation(operations_client: OperationsClient) -> AsyncIterator[OperationSchema]:
    """
    Фикстура создаёт тестовую операцию перед тестом и удаляет её после.
    """
    operation = await operations_client.create_operation()
    yield operation
    await operations_client.delete_operation_api(operation.id)
