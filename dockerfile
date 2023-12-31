# syntax=docker/dockerfile:1

FROM debian:latest

# Update package lists and install Python and necessary tools
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
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
