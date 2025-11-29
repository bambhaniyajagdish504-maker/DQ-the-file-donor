FROM python:3.10-slim-bookworm

RUN apt update && apt upgrade -y
RUN apt install git -y

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "bot.py"]