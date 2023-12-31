# syntax=docker/dockerfile:1

FROM python:3.9


RUN sudo apt-get install build-essential libffi-dev python3-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
