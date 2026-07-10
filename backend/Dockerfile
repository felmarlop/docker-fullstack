# Python 3.13 slim as the base image.
# Most common option, only needed requirements and excellent compatibility.
FROM python:3.13-slim

# Python best practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the default working folder
WORKDIR /app

# Host: backend/requirements.txt
# Container /app/requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]