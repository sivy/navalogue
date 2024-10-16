# come back to: https://hynek.me/articles/docker-uv/
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && \
    apt-get install -y libpq-dev gcc

# setup virtual environment
RUN python -m venv /opt/venv

ADD requirements.txt requirements.txt
RUN /opt/venv/bin/python -m pip install -r requirements.txt
RUN rm requirements.txt

FROM python:3.12-slim-bookworm

RUN groupadd -g 2000 appgroup && useradd -m -u 2001 -g appgroup appuser
ADD --chown=appuser:appgroup . /app

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    rm -fr /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

RUN /opt/venv/bin/python /app/monkinetic/manage.py collectstatic --noinput

ENTRYPOINT [ "/opt/venv/bin/python", "/app/monkinetic/manage.py" ]

EXPOSE 8000

CMD [ "runserver", "0.0.0.0:8000"]
