# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
python -m pytest tests/

# Run only regression tests (used in CI)
python -m pytest tests/ -m regression

# Run a single test
python -m pytest tests/test_operations.py::TestOperations::test_create_operation

# Run tests by marker
python -m pytest tests/ -m operations

# Run with Allure report
python -m pytest tests/ --alluredir=allure-results
allure serve allure-results
```

## Architecture

The project is an **async API test framework** built around pytest + httpx.AsyncClient.

### Request flow

```
Test → Fixture (operations_client) → OperationsClient → BaseClient → httpx.AsyncClient → API
```

### Key design decisions

**Two-level client pattern:**

- `BaseClient` (`clients/base_client.py`) — generic async HTTP wrapper (GET/POST/PATCH/DELETE) with Allure steps
- `OperationsClient` (`clients/operations_client.py`) — domain-specific client, adds business methods like `create_operation()`

**AsyncClient lifecycle is managed in fixtures**, not in clients:

```python
# fixtures/operations.py
async with get_http_client(settings.fake_bank_http_client) as http_client:
    yield OperationsClient(client=http_client)
```

`get_http_client()` returns an `AsyncClient` instance (supports `async with`).

**Event hooks must be `async def`** — `AsyncClient` awaits them. See `clients/event_hooks.py`.

**Configuration** is loaded from `.env` via `pydantic-settings` with `env_nested_delimiter='.'`:

```

FAKE_BANK_HTTP_CLIENT.URL=https://...
FAKE_BANK_HTTP_CLIENT.TIMEOUT=100

```
The `config/` package exports `Settings` and `HTTPClientConfig` from `config/__init__.py`. There is also a legacy `config.py` at the root — ignore it, the package takes precedence.

**Schema naming convention:**

- `OperationSchema` — single item (has `id: str | int`)
- `OperationsSchema` — list container (`RootModel[list[OperationSchema]]`)

**`id` is `str | int`** — the external API (sampleapis.com) returns string IDs for new records.

### pytest config

- `asyncio_mode = auto` in `pytest.ini` — all `async def` tests and fixtures run automatically, no `@pytest.mark.asyncio` needed
- Fixtures are registered via `pytest_plugins` in `conftest.py`
- Markers: `regression` (runs in CI), `operations` (all operation tests)

### Known API limitations (sampleapis.com)

- `test_get_operations` is marked `xfail` — API contains a record with invalid date `'09/02/206'`
- `test_update_operation` has no `regression` marker — PATCH endpoint doesn't actually update records

### Contracts

При обновлении контрактов обязательно поднимать версию в `package.json`.

### Python 3.9 compatibility

Files using `X | Y` union syntax require `from __future__ import annotations` at the top. The `eval_type_backport` package is also required for Pydantic v2 to resolve these annotations at runtime.

### Agents roles

**python-expert**: Для код-ревью, планирования фич и соблюдения стиля.
**python-debugger**: Только для исправления ошибок и анализа падений.
