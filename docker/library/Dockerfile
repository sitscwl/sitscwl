#
# This file is part of sitscwl
# Copyright (C) 2022 INPE.
#
# sitscwl is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

FROM python:3.8-slim-buster

#
# Installing the base packages
#
RUN apt-get update -y \
    && apt-get install -y \
       python3-pip \
       python3-dev \
       git \
       curl \
    && rm -rf /var/lib/apt/lists/* \
    # Installing poetry
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    poetry config virtualenvs.create false

#
# Installing the SITS CWL library
#
COPY . sitscwl

RUN cd sitscwl \
    poetry install
