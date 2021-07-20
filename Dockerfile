FROM python:3.8-alpine
WORKDIR /src

COPY src .
COPY config/requirements.txt requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make bash build-base
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps gcc libc-dev make bash