# Async API Test Template (pytest)

Шаблон для асинхронного тестирования API на `pytest + pytest-asyncio + httpx.AsyncClient`.

## Пример: перенос cURL в template

Исходный запрос:

```bash
curl --location 'https://api.stage2.surfsight.net/v2/authenticate' \
--header 'Content-Type: application/json' \
--data-raw '{
  "email": "your-email@example.com",
  "password": "your-password"
}'
```

Что этому соответствует в проекте:

1. `URL` и `timeout` в `.env`
2. endpoint в `tools/routes.py` (`AUTHENTICATE = "/authenticate"`)
3. body-схема в `schema/operations.py` (`AuthenticateRequestSchema`)
4. метод клиента в `clients/operations_client.py` (`authenticate_api`)
5. фикстура payload из `.env` в `fixtures/operations.py` (`auth_payload`)
6. integration-тест в `tests/test_operations.py` (`test_authenticate`)

## Установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Настройка `.env`

```env
API_HTTP_CLIENT.URL=https://api.stage2.surfsight.net/v2
API_HTTP_CLIENT.TIMEOUT=30
AUTH_CREDENTIALS.EMAIL=your-email@example.com
AUTH_CREDENTIALS.PASSWORD=your-password
```

## Запуск

```bash
# Локальные (без сети)
python -m pytest tests/ -m template

# Интеграционные (реальный API)
python -m pytest tests/ -m integration
```
