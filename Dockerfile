FROM python:3.12-slim

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --no-cache-dir -r requirements-docker.txt

COPY . .

EXPOSE 8050

CMD ["gunicorn", "-b", "0.0.0.0:8050", "--workers", "2", "app:server"]