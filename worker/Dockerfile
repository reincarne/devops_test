FROM python:3.11-slim

RUN groupadd -g 1000 workeruser && useradd -u 1000 -g workeruser -d /app -s /sbin/nologin workeruser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]