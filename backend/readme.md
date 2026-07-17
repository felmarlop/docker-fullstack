# Backend

This directory contains the Django REST API.

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
