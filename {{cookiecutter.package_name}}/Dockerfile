ARG UV_VERSION={{ cookiecutter.uv_version }}
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv-source

FROM python:{{ cookiecutter.python_version }}-slim-buster AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

FROM base as uv

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON={{ cookiecutter.python_version }} \
    UV_PROJECT_ENVIRONMENT=/app \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

SHELL ["/bin/bash", "-exo", "pipefail",  "-c"]

RUN apt-get update \
    && apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false \
	&& apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv-source /uv /usr/local/bin/uv

FROM uv AS deps-builder

COPY pyproject.toml /_project/
COPY uv.lock /_project/

RUN --mount=type=cache,target=/root/.cache <<EOT
    uv venv
EOT

WORKDIR /_project

RUN --mount=type=cache,target=/root/.cache <<EOT
    uv sync --locked --no-dev --no-install-project
EOT

FROM uv AS project-builder

COPY --from=deps-builder /app /app

COPY . /src

WORKDIR /src

# install project
RUN --mount=type=cache,target=/root/.cache <<EOT
    uv sync --locked --no-dev --no-editable
EOT

FROM base AS final

SHELL ["/bin/bash", "-exo", "pipefail",  "-c"]

ENV PATH=/app/bin:$PATH

RUN <<EOT
    groupadd -r app
    useradd -r -d /app -g app -N app
EOT

STOPSIGNAL SIGINT

RUN <<EOT
    apt-get update -qy
    apt-get install -qyy \
    -o APT::Install-Recommends=false \
    -o APT::Install-Suggests=false
    apt-get clean
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

COPY docker-entrypoint.sh /
RUN chmod +x '/docker-entrypoint.sh'
ENTRYPOINT ["/bin/bash", "/docker-entrypoint.sh"]

COPY --from=project-builder --chown=app:app /app /app

USER app
WORKDIR /app
