# syntax=docker/dockerfile:1

FROM python:3.9

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    libffi-dev

# Install Rust compiler (from Debian repositories)
RUN apt-get install -y rustc cargo

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
