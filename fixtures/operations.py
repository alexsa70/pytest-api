from typing import Iterator

import pytest

from clients.operations_client import OperationsClient, get_operations_client
from config import Settings
from schema.operations import OperationSchema


@pytest.fixture
def operations_client(settings: Settings) -> OperationsClient:
    """
    Фикстура создаёт экземпляр API-клиента для работы с операциями.
    
    :param settings: Объект с настройками тестовой сессии.
    :return: Экземпляр OperationsClient.
    """
    return get_operations_client(settings)


@pytest.fixture
def function_operation(operations_client: OperationsClient) -> Iterator[OperationSchema]:
    """
    Фикстура создаёт тестовую операцию перед тестом и удаляет её после выполнения теста.
    
    :param operations_client: API-клиент для работы с операциями.
    :return: Созданная тестовая операция.
    """
    operation = operations_client.create_operation()
    yield operation

    operations_client.delete_operation_api(operation.id)