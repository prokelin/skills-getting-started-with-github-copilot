## Plan: Add FastAPI Backend Tests

Add a dedicated `tests/backend/` suite for the FastAPI application, preserving the current in-memory data while making every test isolated and covering all public route behavior and expected validation errors.

**Steps**
1. Add `pytest` to `requirements.txt` alongside the existing `fastapi` and `httpx` test dependencies so the test command works from a fresh environment.
2. Create `tests/backend/conftest.py` with an autouse fixture that snapshots `src.app.activities` deeply before each test and restores each activity's participant list afterward. This is required because signup and unregister mutate module-level state and test order must not affect results.
3. Move or recreate the existing unregister success test in `tests/backend/test_app.py`, then expand the module with `TestClient(app)` coverage for:
   - `GET /` returning the expected redirect to `/static/index.html` without following the redirect.
   - `GET /activities` returning the activity mapping and expected activity fields.
   - Successful signup adding a new email and returning the expected message.
   - Signup for an unknown activity returning 404 and `Activity not found`.
   - Duplicate signup returning 400 and the existing duplicate-registration detail.
   - Successful unregister removing the email and returning the expected message.
   - Unregister from an unknown activity returning 404.
   - Unregistering an email that is not present returning 404 and the existing detail.
   Each test should follow the AAA pattern: arrange inputs and initial state, perform one request in the act phase, then assert the response and relevant state change. Keep fixture cleanup outside those phases; use parameterization only where it preserves readability for repeated validation cases.
4. Update the relevant README test/setup documentation with the environment setup and focused command `pytest`, noting that backend state is in memory and isolated per test by the fixture. Keep the API implementation unchanged unless a test exposes an actual contract mismatch.
5. Run the focused backend suite first, then the full pytest suite, and verify that tests pass regardless of execution order.

**Relevant files**
- `/workspaces/skills-getting-started-with-github-copilot/src/app.py` — reuse the existing `app`, `activities`, and route contracts; no planned production change.
- `/workspaces/skills-getting-started-with-github-copilot/tests/test_app.py` — migrate the existing unregister test into the dedicated backend suite or retain only if the final layout avoids duplicate coverage.
- `/workspaces/skills-getting-started-with-github-copilot/tests/backend/conftest.py` — new shared state-isolation fixture.
- `/workspaces/skills-getting-started-with-github-copilot/tests/backend/test_app.py` — new comprehensive FastAPI endpoint tests.
- `/workspaces/skills-getting-started-with-github-copilot/requirements.txt` — add the test runner dependency.
- `/workspaces/skills-getting-started-with-github-copilot/README.md` or `/workspaces/skills-getting-started-with-github-copilot/src/README.md` — document test setup and invocation, choosing the project-level README if test instructions should be repository-wide.
- `/workspaces/skills-getting-started-with-github-copilot/pytest.ini` — retain `pythonpath = .`; optionally add a backend marker only if the suite needs selective marker-based execution.

**Verification**
1. Install requirements in a clean environment if needed.
2. Run `pytest tests/backend -q` and confirm all backend tests pass.
3. Run `pytest -q` and confirm the migrated/remaining existing suite also passes.
4. Run the backend tests in a shuffled order, such as `pytest tests/backend --randomly-seed=...`, only if a random-order plugin is already available; otherwise repeat the suite and rely on the autouse snapshot/restore fixture review.
5. Confirm the redirect test disables redirect following and the mutation tests leave the original activity data unchanged after each test.

**Decisions**
- Use `tests/backend/` as the separate backend test directory, based on the user's selection.
- Target all routes and both success and error cases, based on the user's selection.
- Prefer a fixture over manual `try/finally` cleanup so every test gets isolation consistently.
- Do not refactor the API or introduce a database abstraction as part of test addition.
- Avoid adding a random-order dependency solely for this task; use the existing pytest setup unless the repository already adopts one.
