# Debugging Notes

## Session: 2026-03-09 — integration test failures

### Failure 1: pydantic ValidationError on Settings init

Full error:
```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
org_id
  Extra inputs are not permitted [type=extra_forbidden, input_value='=122974', input_type=str]
```

Root causes (two separate, compounding):

a) `.env` had `ORG_ID==122974` (double `=`). python-dotenv splits on the first `=` only, so key=`ORG_ID`, value=`=122974`.

b) `config/settings.py` (the one actually imported via `config/__init__.py`) had no `org_id` field. So pydantic-settings passed the env var as an unknown extra kwarg to the model, which has no `extra = "allow"` configured — rejected.

Fix:
- `.env` line 5: `ORG_ID=122974`
- `config/settings.py` line 36: add `org_id: Optional[int] = None`

### Failure 2: ScopeMismatch for auth_token fixture

Full error:
```
ScopeMismatch: You tried to access the function scoped fixture _function_scoped_runner
with a session scoped request object.
Requesting fixture stack:
fixtures/operations.py:35:  def auth_token(...) -> str
```

Root cause:
- `pytest.ini` sets `asyncio_default_fixture_loop_scope = function`
- `auth_token` is declared `@pytest_asyncio.fixture(scope="session")` without specifying `loop_scope`
- pytest-asyncio v1.2.0 creates a `_function_scoped_runner` by default; a session-scoped async fixture cannot use it

Fix:
```python
@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def auth_token(...):
    ...
```

The `loop_scope` parameter is available in pytest-asyncio >= 0.23 (confirmed in v1.2.0).

### Lesson

When a session-scoped async fixture is present AND `asyncio_default_fixture_loop_scope = function` is in `pytest.ini`, ALWAYS add `loop_scope="session"` to the fixture decorator to avoid the ScopeMismatch.
