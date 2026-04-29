FROM python:3.14-alpine
WORKDIR /home/kozRandBot

RUN apk add --no-cache su-exec

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
