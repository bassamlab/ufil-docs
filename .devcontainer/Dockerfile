FROM python:3.13-alpine

ENV LC_ALL=C.UTF-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# git + openssh-client: git over SSH (keys mounted read-only from host)
RUN apk add --no-cache git openssh-client

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt
