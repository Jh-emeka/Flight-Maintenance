# syntax=docker/dockerfile:1

FROM python:3.9-alpine

# Install Rust compiler (Rustup)
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Set environment variables for Rust
ENV PATH="/root/.cargo/bin:${PATH}"
ENV USER=root

# Install necessary development tools (e.g., build-essential, libffi-dev)
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev

WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
