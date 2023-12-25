FROM python:3.11.5-alpine3.18

COPY requirements.txt /requirements.txt
COPY dev-requirements.txt /dev-requirements.txt

RUN pip install -r /requirements.txt -r /dev-requirements.txt

RUN apk update && apk upgrade\
 && apk --no-cache add curl bash\
 && apk cache clean

COPY . /opt/representer

WORKDIR /opt/representer

ENTRYPOINT ["sh","/opt/representer/bin/run.sh"]

