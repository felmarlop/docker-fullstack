# Backend

Django backend application built with **Django REST Framework**.

This service provides the REST API, authentication layer, business logic and database integration.

## 🔐 Authentication

The API uses **JWT authentication** with access and refresh tokens.

Available authentication endpoints:

| Endpoint                     | Description                      |
| ---------------------------- | -------------------------------- |
| `/api/auth/login/`           | Obtain access and refresh tokens |
| `/api/auth/refresh/`         | Refresh access token             |
| `/api/auth/change-password/` | Change user password             |
| `/api/auth/logout/`          | Invalidate refresh token         |

## 🛠️ Django Admin

Create a superuser:

```bash
make shell

python manage.py createsuperuser
```

Access the administration panel:

```text
/admin/
```

## 🛠️ Development

### Code Quality

The project uses:

- **Ruff** for linting, formatting and import sorting.
- **Pyright** for static type checking.

Run quality checks:

```bash
make lint
make type-check
```

---

### Type Hints

Follow modern Python typing practices:

- Type all function arguments and return values.
- Prefer built-in generic types:

```python
list[str]
dict[str, Any]
```

instead of:

```python
List[str]
Dict[str, Any]
```

Additional guidelines:

- Use `Any` only when the type is genuinely unknown.
- Avoid `cast()` unless necessary.
- Avoid `pyright: ignore[...]` unless documenting a verified false positive.

---

### Code Style

The project follows the configured Ruff rules.

Guidelines:

- Use absolute imports.

Example:

```python
from app.authentication.serializers.user import UserSerializer
```

- Keep imports sorted automatically with Ruff.
- Prefer explicit and readable code.

## ✅ Testing

The backend uses **Pytest** for automated testing.

Guidelines:

- Reuse shared fixtures from `conftest.py`.
- Prefer one test per behavior.
- Keep tests focused and maintainable.

Run the test suite:

```bash
make test
```
