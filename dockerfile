# syntax=docker/dockerfile:1

FROM python:3.9


RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
