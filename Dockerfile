FROM python:3.7-alpine

WORKDIR /home/kozRandBot

COPY requirements.txt .
RUN pip install -r requirements.txt

# www-data
USER 33
COPY app ./app

CMD ["python", "app/bot.py"]
