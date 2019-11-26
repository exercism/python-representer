FROM python:3.7-alpine

RUN apk add --no-cache gcc libc-dev unixodbc-dev

RUN mkdir /opt/representer
COPY . /opt/representer
WORKDIR /opt/representer

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/opt/representer/bin/generate.sh"]
