# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY . /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]

