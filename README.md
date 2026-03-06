# pytest-API (learning)

Учебный проект для изучения автоматизации тестирования REST API с использованием pytest.

Тесты работают с [sampleapis.com](https://api.sampleapis.com) — публичным mock-API, имитирующим банковские операции.

## Стек

| Инструмент | Версия | Назначение |
|---|---|---|
| Python | 3.9+ | Язык |
| pytest | 8.4+ | Тест-фреймворк |
| httpx | 0.28+ | HTTP-клиент |
| pydantic | 2.12+ | Валидация схем |
| pydantic-settings | 2.11+ | Загрузка конфигурации из `.env` |
| allure-pytest | 2.15+ | Отчёты о тестировании |
| faker | 37+ | Генерация тестовых данных |
| jsonschema | 4.25+ | Валидация JSON-схем |
| eval-type-backport | 0.3+ | Поддержка `X \| Y` типов в Python 3.9 |

## Установка

```bash
# 1. Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 2. Установить зависимости
pip install pytest httpx pydantic pydantic-settings allure-pytest faker jsonschema eval_type_backport

# 3. Создать файл с конфигурацией
cp .env.example .env  # или создать вручную
```

### Содержимое `.env`

```env
FAKE_BANK_HTTP_CLIENT.URL="https://api.sampleapis.com"
FAKE_BANK_HTTP_CLIENT.TIMEOUT=100
```

## Запуск тестов

```bash
# Все тесты
python -m pytest tests/

# С подробным выводом
python -m pytest tests/ -v

# Только по маркеру
python -m pytest tests/ -m operations
python -m pytest tests/ -m regression

# Только один тест
python -m pytest tests/test_operations.py::TestOperations::test_create_operation

# С Allure-отчётом
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results
 # 1. Запустить тесты и сохранить результаты                                                                                                                  
  python -m pytest tests/ --alluredir=allure-results                                                                                                           
                                                                                                                                                               
  # 2. Открыть отчёт в браузере                                                                                                                                
  allure serve allure-results                                                                                                                                  
                                                                                                                                                               
  allure serve сам запустит локальный сервер и откроет браузер. Если хочешь просто сгенерировать HTML без автооткрытия:                                        
                                                                                                                                                               
  allure generate allure-results -o allure-report --clean                                                                                                      
  open allure-report/index.html


## Структура проекта

```
├── tests/                  # Тестовые файлы (test_*.py)
├── fixtures/               # pytest-фикстуры (клиенты, тестовые данные)
├── clients/                # HTTP-клиенты для API
│   ├── base_client.py      # Базовый клиент (GET/POST/PATCH/DELETE)
│   ├── operations_client.py
│   └── event_hooks.py      # Логирование запросов/ответов
├── schema/                 # Pydantic-модели для валидации
│   └── operations.py
├── tools/
│   ├── assertions/         # Функции проверок (assert_*)
│   ├── fakers.py           # Генерация тестовых данных
│   ├── routes.py           # URL-маршруты API
│   └── logger.py
└── config/                 # Настройки приложения
    └── settings.py
```

## Как добавлять новые тесты

**1. Новый тест в существующем классе** (`tests/test_operations.py`):

```python
@allure.title("My new test")
def test_something(self, operations_client: OperationsClient):
    response = operations_client.get_operations_api()
    assert_status_code(response.status_code, HTTPStatus.OK)
```

**2. Новая фикстура с teardown** (`fixtures/operations.py`):

```python
@pytest.fixture
def my_fixture(operations_client: OperationsClient) -> Iterator[OperationSchema]:
    operation = operations_client.create_operation()
    yield operation
    operations_client.delete_operation_api(operation.id)  # teardown
```

**3. Новый API-маршрут** (`tools/routes.py`):

```python
class APIRoutes(str, Enum):
    MY_ENDPOINT = "/fakebank/my-endpoint"
```

## Исправленные ошибки

| Файл | Проблема | Исправление |
|---|---|---|
| `config/__init__.py` | Пустой — не экспортировал классы | Добавлен `from config.settings import Settings, HTTPClientConfig` |
| `config/settings.py` | Устаревший Pydantic v1 `BaseSettings` | Переписан под Pydantic v2 + `pydantic-settings` |
| `schema/operations.py` | `OperationSchema` и `OperationsSchema` перепутаны местами | Имена исправлены |
| `schema/operations.py` | `configDict` — неверное имя | Исправлено на `ConfigDict` |
| `schema/operations.py` | Поля `category`, `description`, `transactionDate` — required без дефолтов | Добавлены `default_factory=fake.xxx` |
| `schema/operations.py` | `id: int`, а API возвращает строку | Изменено на `id: str \| int` |
| `clients/operations_client.py` | Импорт с маленькой `s`: `Operationschema` | Исправлен регистр на `OperationSchema` |
| `clients/base_client.py`, `schema/operations.py`, `tools/assertions/operations.py` | Синтаксис `X \| Y` (Python 3.10+) в Python 3.9 | Добавлен `from __future__ import annotations` |
