from __future__ import annotations

from datetime import date
from pydantic import BaseModel, ConfigDict, Field, RootModel

from tools.fakers import fake


class CreateOperationSchema(BaseModel):
    """
    Модель для создания новой банковской операции.

    Поля:
    - debit (float | None): Сумма списания со счёта
    - credit (float | None): Сумма зачисления на счёт
    - category (str): Категория операции
    - description (str): Описание операции
    - transaction_date (date): Дата транзакции (передаётся в формате "transactionDate")
    """
    model_config = ConfigDict(
        populate_by_name=True)  # Позволяет использовать alias при сериализации/десериализации
    debit: float | None = None
    credit: float | None = None
    category: str = Field(default_factory=fake.category)
    description: str = Field(default_factory=fake.sentence)
    # Указываем alias для соответствия API
    transaction_date: date = Field(default_factory=fake.date, alias="transactionDate")


class UpdateOperationSchema(BaseModel):
    """
   Модель для обновления банковской операции (используется в PATCH запросах).

   Все поля являются необязательными, так как можно обновлять только часть данных.

   Поля:
   - debit (float | None): Новая сумма списания
   - credit (float | None): Новая сумма зачисления
   - category (str | None): Новая категория
   - description (str | None): Новое описание
   - transaction_date (date | None): Новая дата транзакции (alias "transactionDate")
   """
    model_config = ConfigDict(
        populate_by_name=True)  # Позволяет использовать alias при сериализации/десериализации
    debit: float | None = None
    credit: float | None = None
    category: str | None = None
    description: str | None = None
    transaction_date: date | None = Field(None, alias="transactionDate")


class OperationSchema(CreateOperationSchema):
    """
    Модель банковской операции, содержащая ID.

    Наследуется от CreateOperationSchema и добавляет поле:
    - id (str | int): Уникальный идентификатор операции (API возвращает строку)
    """
    id: str | int


class OperationsSchema(RootModel):
    """
    Контейнер для списка операций.

    Поле:
    - root (list[OperationSchema]): Список операций
    """
    root: list[OperationSchema]
