# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./db /usr/src/app

EXPOSE 3000

CMD ["python", "app.py"]
