FROM python:3.11

RUN apt-get update \
    # && apt-get install -y --no-install-recommends \
    # build-essential \
    # libpq-dev \
    # apt-transport-https \
    # ca-certificates \
    # curl \
    # gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip \
  && pip install poetry \
  && poetry config virtualenvs.create false
