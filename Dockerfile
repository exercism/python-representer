FROM python:3.8-alpine as base

FROM base as builder

RUN apk add --no-cache gcc libc-dev unixodbc-dev curl
RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install --prefix=/install --no-warn-script-location -r /requirements.txt -r /dev-requirements.txt

RUN curl -L -o /install/bin/tooling_webserver "$TOOLING_WEBSERVER_URL" \
 && chmod +x /install/bin/tooling_webserver

FROM base

COPY --from=builder /install /usr/local
COPY . /opt/representer

ENV TOOLING_WEBSERVER_VERSION="0.10.0"
ENV TOOLING_WEBSERVER_URL="https://github.com/exercism/tooling-webserver/releases/download/${TOOLING_WEBSERVER_VERSION}/tooling_webserver"

RUN apk add curl -y \
 && curl -L -o /usr/local/bin/tooling_webserver "$TOOLING_WEBSERVER_URL" \
 && chmod +x /usr/local/bin/tooling_webserver \
 && apk remove curl -y

WORKDIR /opt/representer

ENTRYPOINT ["sh", "bin/generate.sh"]
