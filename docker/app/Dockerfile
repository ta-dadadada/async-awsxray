FROM alpine:3.10.0
ENV APP_ROOT="/opt/app"

RUN apk add --virtual .useradd-deps \
    shadow \
    && groupadd app -g 1000 \
    && useradd -c app -d ${APP_ROOT} -s /bin/sh -u 1000 -g app -G app -r app \
    && apk del .useradd-deps

RUN apk add --update \
    make \
    gcc \
    libc-dev \
    coreutils \
    mariadb-dev \
    libffi-dev \
    libnsl-dev \
    linux-headers \
    ncurses-dev \
    zlib-dev \
    openssl-dev \
    python3 \
    python3-dev

RUN pip3 install -U pip pipenv

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system
COPY src src
COPY docker/app/entrypoint.sh entrypoint.sh

ENV API_HOST "0.0.0.0"
ENV API_PORT 5000
ENTRYPOINT ["./entrypoint.sh"]
