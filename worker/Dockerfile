FROM debian:bookworm-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.3 /uv /uvx /bin/

ENV UV_PYTHON_INSTALL_DIR=/opt/python

RUN uv venv /opt/venv --python 3.11

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

FROM debian:bookworm-slim

RUN useradd --create-home appuser && mkdir -p /home/appuser/code/logs && chown -R appuser:appuser /home/appuser/code/logs

COPY --from=builder /opt/python /opt/python
COPY --from=builder /opt/venv /opt/venv

USER appuser
WORKDIR /home/appuser/code
COPY . .

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

CMD ["/opt/venv/bin/celery", "-A", "worker.celery_app", "worker", "--loglevel=info"]
