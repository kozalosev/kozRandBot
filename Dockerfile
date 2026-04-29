FROM python:3.14-alpine
WORKDIR /home/kozRandBot

RUN apk add --no-cache su-exec

COPY requirements.txt requirements-proxy.txt ./
RUN pip install -r requirements.txt -r requirements-proxy.txt

COPY app ./app
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
