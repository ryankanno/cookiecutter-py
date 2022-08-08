FROM python:{{ cookiecutter.python_version }}-slim-buster

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION={{ cookiecutter.poetry_version }}

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

LABEL maintainers="{{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>"

LABEL org.opencontainers.image.created="${BUILD_DATETIME}" \
      org.opencontainers.image.title="{{ cookiecutter.project_name }}" \
      org.opencontainers.image.description="{{ cookiecutter.project_short_description }}" \
      org.opencontainers.image.authors="{{ cookiecutter.author_email }}" \
      org.opencontainers.image.revision="${REVISION}" \
      org.opencontainers.image.source="${REPOSITORY}" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.licenses="{{ cookiecutter.project_license }}"

SHELL ["/bin/bash", "-exo", "pipefail",  "-c"]

RUN apt-get update \
    && apt-get install --no-install-recommends -y wget python3-pip \
	&& apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip
RUN wget -qO- https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python3

ENV PATH="~/.local/bin:${PATH}"

COPY pyproject.toml poetry.* /

RUN /bin/bash -c "poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi --no-root"

# Specify entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
