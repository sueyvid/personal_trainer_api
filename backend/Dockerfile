FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

COPY requirements.txt .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
