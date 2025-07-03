FROM python:3.12-bullseye AS base
ENV PYTHONUNBUFFERED=1

RUN apt update
RUN apt install gettext -y

RUN mkdir /code

WORKDIR /code

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

FROM base AS development

RUN poetry install 
RUN poetry run playwright install --with-deps

COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT ["/code/start-django.sh"]

FROM base AS production

RUN poetry install --only main

COPY . .
RUN chmod 755 /code/start-django.sh

EXPOSE 8000

ENTRYPOINT ["/code/start-django.sh"]