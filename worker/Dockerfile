FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    tini && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser worker.py .
RUN mkdir -p logs && chown -R appuser:appuser logs

USER appuser

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "worker.py"]


