# Python 3.13 slim as the base image.
# Most common option, only needed requirements and excellent compatibility.
FROM python:3.13-slim

# Set the default working folder
WORKDIR /app

# Host: backend/requirements.txt
# Container /app/requirements.txt
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["bash", "-c", "echo 'Backend container started'; python --version; sleep infinity"]