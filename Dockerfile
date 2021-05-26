FROM python:3.9-slim as base

FROM base as builder

RUN mkdir /install

WORKDIR /install

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install --prefix=/install --no-warn-script-location -r /requirements.txt -r /dev-requirements.txt

FROM base

COPY --from=builder /install /usr/local


RUN apt-get update \
 && apt-get install curl -y \
 && apt-get remove curl -y \
 && apt-get autoremove -y \
 && rm -rf /var/lib/apt/lists/*

COPY . /opt/representer

WORKDIR /opt/representer

ENTRYPOINT ["sh","/opt/representer/bin/run.sh"]
