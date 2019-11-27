FROM python:3.8-alpine

RUN apk add --no-cache gcc libc-dev unixodbc-dev

COPY *requirements.txt /opt/representer/
WORKDIR /opt/representer

RUN pip install -r requirements.txt -r dev-requirements.txt

COPY . /opt/representer

ENTRYPOINT ["sh", "/opt/representer/bin/generate.sh"]
