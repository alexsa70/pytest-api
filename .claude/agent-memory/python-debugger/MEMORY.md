# python-debugger Agent Memory

## Key Architectural Facts

- `config/__init__.py` imports from `config/settings.py` (NOT from root-level `config.py`).
  Both files define `Settings`; they must stay in sync. `config.py` is the root-level duplicate — canonical source is `config/settings.py`.
- `asyncio_default_fixture_loop_scope = function` is set in `pytest.ini`. Session-scoped async fixtures need `loop_scope="session"` on their decorator.

## Known Bugs Fixed

### 1. `.env` typo: `ORG_ID==122974` (double `=`)
- Symptom: `pydantic_core.ValidationError: Extra inputs are not permitted [input_value='=122974']`
- Cause: python-dotenv parses `ORG_ID==122974` and produces value `"=122974"` (a string starting with `=`).
- Fix: Correct the `.env` line to `ORG_ID=122974`.
- See: `debugging.md` for full trace.

### 2. `config/settings.py` missing `org_id` field
- Symptom: Same ValidationError as above — `org_id` treated as unknown extra field.
- Cause: `config/settings.py` lacked `org_id: Optional[int] = None` while `config.py` had it.
- Fix: Add `org_id: Optional[int] = None` to `config/settings.py`.

### 3. `ScopeMismatch` on session-scoped async fixture `auth_token`
- Symptom: `ScopeMismatch: function scoped fixture _function_scoped_runner used by session scoped request`
- Cause: `pytest-asyncio` (v1.2.0) with `asyncio_default_fixture_loop_scope = function` creates only a function-scoped runner by default. A `scope="session"` async fixture with no `loop_scope` argument tries to use the function-scoped runner — scope mismatch.
- Fix: Add `loop_scope="session"` to the decorator: `@pytest_asyncio.fixture(scope="session", loop_scope="session")`.
- File: `fixtures/operations.py`, fixture `auth_token`.

## General Patterns

- When `pydantic-settings` raises `Extra inputs are not permitted`, always check `.env` for typos AND verify the `Settings` model has a field for every env var that could be read.
- When `pytest-asyncio` raises `ScopeMismatch` for `_scoped_runner`, check that the `loop_scope` on the fixture decorator matches its `scope`. They must match for session/module/package-scoped async fixtures.
- Detailed notes: `debugging.md`
