FROM python:{{ cookiecutter.python_version }}-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random

FROM base as builder

ENV PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PATH="~/.local/bin:/venv/bin:${PATH}" \
  VIRTUAL_ENV="/venv" \
  POETRY_VERSION={{ cookiecutter.poetry_version }} \
  POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

SHELL ["/bin/bash", "-exo", "pipefail",  "-c"]

RUN apt-get update \
    && apt-get install --no-install-recommends -y curl \
	&& apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - --version ${POETRY_VERSION}
RUN python3 -m venv ${VIRTUAL_ENV}

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-interaction --no-ansi --no-root
COPY . ./
RUN poetry install --no-interaction --no-ansi

FROM base as final

ARG REPOSITORY={{ cookiecutter.project_url }}
ARG BUILD_DATETIME
ARG VERSION
ARG REVISION
ARG BRANCH

ENV REPOSITORY ${REPOSITORY}
ENV BUILD_DATETIME ${BUILD_DATETIME:-null}
ENV VERSION ${VERSION:-null}
ENV REVISION ${REVISION:-null}
ENV BRANCH ${BRANCH:-main}

ENV PATH="/venv/bin:${PATH}" \
  VIRTUAL_ENV="/venv"

LABEL maintainers="{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>"

LABEL org.opencontainers.image.created="${BUILD_DATETIME}" \
      org.opencontainers.image.title="{{ cookiecutter.project_name }}" \
      org.opencontainers.image.description="{{ cookiecutter.project_short_description }}" \
      org.opencontainers.image.authors="{{ cookiecutter.author_email }}" \
      org.opencontainers.image.revision="${REVISION}" \
      org.opencontainers.image.source="${REPOSITORY}" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.licenses="{{ cookiecutter.project_license }}"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY --from=builder /app /app

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x '/docker-entrypoint.sh'
