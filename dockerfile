# syntax=docker/dockerfile:1

FROM python:3.9
RUN apk add --update \
  build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  postgresql-client \
  postgresql-dev \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev
WORKDIR /usr/src/app

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python", "app.py"]
