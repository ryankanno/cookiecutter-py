FROM python:{{ cookiecutter.python_version }}-slim-buster
MAINTAINER {{ cookiecutter.author_name }} <{{ cookiecutter.author_email }}>

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

RUN apt-get update \
    && apt-get install -y wget python3-pip \
	&& apt-get clean

RUN ln -s /usr/bin/python3 /usr/bin/python && ln -s /usr/bin/pip3 /usr/bin/pip
RUN wget -qO- https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | POETRY_VERSION=$POETRY_VERSION python3

COPY pyproject.toml poetry.* /

RUN /bin/bash -c "source ${HOME}/.poetry/env && poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi"

# Specify entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
