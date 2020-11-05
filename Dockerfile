FROM python:3.8-slim as base

FROM base as builder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install --prefix=/install --no-warn-script-location -r /requirements.txt -r /dev-requirements.txt

FROM base

COPY --from=builder /install /usr/local

ENV TOOLING_WEBSERVER_VERSION="0.10.0"
ENV TOOLING_WEBSERVER_URL="https://github.com/exercism/tooling-webserver/releases/download/${TOOLING_WEBSERVER_VERSION}/tooling_webserver"

RUN apt-get update \
 && apt-get install curl -y \
 && curl -L -o /usr/local/bin/tooling_webserver "$TOOLING_WEBSERVER_URL" \
 && chmod +x /usr/local/bin/tooling_webserver \
 && apt-get remove curl -y \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY . /opt/representer

WORKDIR /opt/representer

ENTRYPOINT ["sh","/opt/representer/bin/run.sh"]
