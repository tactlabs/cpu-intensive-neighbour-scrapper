FROM python:3.9.4-slim-buster

RUN apt update

RUN apt install stress

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ADD . .

CMD ["./run.sh"]