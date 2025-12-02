FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/deploy/requirements.txt

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --workers 2"]