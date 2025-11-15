FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd -m svcuser

RUN mkdir -p /app/data && chown -R svcuser:svcuser /app/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

COPY storage.py .
RUN mkdir -p /app/data && chown -R svcuser:svcuser /app/data

COPY post_weekly.py .

USER svcuser

CMD ["python", "app.py"]
