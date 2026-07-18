# Backend

This project contains the Django backend built with Django REST Framework.

## Authentication

The API uses JWT authentication with access and refresh tokens.

Available authentication endpoints:

- `/api/auth/login/`
- `/api/auth/refresh/`
- `/api/auth/change-password/`
- `/api/auth/logout/`

## Django Admin

Create a superuser:

```bash
make shell
>> python manage.py createsuperuser
```

Then access the Django Admin at:

```
/admin/
```

## Development

### Code quality

- Ruff is used for linting, formatting and import sorting.
- Pyright is used for static type checking.
- Run all quality checks before pushing changes.
  ```
  make lint
  make type-check
  ```

### Type hints

- Type all function arguments.
- Type all return values.
- Use modern Python type hints.
- Prefer `dict[str, Any]` over `Dict[str, Any]`.
- Prefer `list[str]` over `List[str]`.
- Use `Any` only when the type is genuinely unknown or represents arbitrary data.
- Avoid `cast()` unless there is no cleaner solution.
- Avoid `pyright: ignore[...]` except for documented false positives in third-party libraries.

### Code style

- Ruff is used for linting, formatting and import sorting.
- Follow the configured Ruff rules and formatting.
- Use absolute imports (for example, `app.authentication.serializers.user`).

### Testing

- Pytest is used for all backend tests.
- Reuse shared fixtures from the global `conftest.py`.
- Prefer one test per behavior.

Run the test suite with:

```
make test
```
