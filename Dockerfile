FROM python:3.8-alpine as base

FROM base as builder

RUN apk add --no-cache gcc libc-dev unixodbc-dev
RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install --prefix=/install -r /requirements.txt -r /dev-requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY . /opt/representer

WORKDIR /opt/representer

ENTRYPOINT ["sh", "bin/generate.sh"]
