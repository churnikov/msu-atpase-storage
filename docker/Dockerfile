FROM python:3.9-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV POETRY_VIRTUALENVS_CREATE=false

RUN apt-get update -qy && \
    apt-get install -y libpq-dev gcc

RUN pip install poetry

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

COPY ./msu_atpase_storage  /code/msu_atpase_storage/

RUN poetry install --no-dev --no-interaction --no-ansi

COPY docker/run.sh run.sh
RUN ["chmod", "+x", "/code/run.sh"]

ENTRYPOINT ["/code/run.sh"]
