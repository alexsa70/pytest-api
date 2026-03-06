from __future__ import annotations

from typing import Any

import allure
from httpx import Client, URL, Response, QueryParams
from httpx._types import RequestData, RequestFiles

from clients.event_hooks import log_request_event_hook, log_response_event_hook
from tools.logger import get_logger
from config import HTTPClientConfig


class BaseClient:
    """
    Базовый клиент для выполнения HTTP-запросов.

    Этот класс предоставляет основные методы для выполнения HTTP-запросов
    (GET, POST, PATCH, DELETE) и использует httpx.Client для выполнения
    запросов. Каждый метод добавлен с использованием allure для генерации
    отчетов о тестах.
    """

    def __init__(self, client: Client):
        """
        Инициализация клиента.
        :param client: Экземпляр httpx.Client
        """
        self.client = client

    @allure.step("Make GET request to {url}")
    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """
        Выполняет GET-запрос.

        :param url: URL эндпоинта
        :param params: Query параметры запроса
        :return: HTTP-ответ
        """
        return self.client.get(url, params=params)

    @allure.step("Make POST request to {url}")
    def post(
            self,
            url: URL | str,
            json: Any | None = None,
            data: RequestData | None = None,
            files: RequestFiles | None = None
    ) -> Response:
        """
        Выполняет POST-запрос.

        :param url: URL эндпоинта
        :param json: JSON тело запроса
        :param data: Данные формы
        :param files: Файлы для загрузки
        :return: HTTP-ответ
        """
        return self.client.post(url, json=json, data=data, files=files)

    @allure.step("Make PATCH request to {url}")
    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """
        Выполняет PATCH-запрос.

        :param url: URL эндпоинта
        :param json: JSON тело запроса
        :return: HTTP-ответ
        """
        return self.client.patch(url, json=json)

    @allure.step("Make DELETE request to {url}")
    def delete(self, url: URL | str) -> Response:
        """
        Выполняет DELETE-запрос.

        :param url: URL эндпоинта
        :return: HTTP-ответ
        """
        return self.client.delete(url)


def get_http_client(config: HTTPClientConfig) -> Client:
    """
    Функция для инициализации HTTP-клиента.

    :param config: Конфигурация HTTP-клиента
    :return: Экземпляр httpx.Client
    """
    return Client(
        timeout=config.timeout,  # Устанавливаем таймаут для всех запросов
        base_url=config.client_url,  # Базовый URL для API
        event_hooks={
            # Добавляем хук для логирования запросов
            "request": [log_request_event_hook],
            # Добавляем хук для логирования ответов
            "response": [log_response_event_hook]
        }
    )
