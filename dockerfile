# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
