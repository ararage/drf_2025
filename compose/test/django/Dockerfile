FROM alpine:3.22

ENV PYTHONUNBUFFERED 1

RUN \
  apk update && \
  apk -U upgrade && \
  apk add --virtual build-dependencies \
    # to reach GitHub's https
    openssl ca-certificates \
    build-base cmake musl-dev linux-headers \
  #Python
  && apk add python3 py3-pip \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # Cryptography
  && apk add --no-cache openssl-dev \
  && apk add gcc cargo \
  && apk add rust \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  && apk add g++ \
  && apk add make \
  && apk add py3-psycopg2

RUN apk add --update --no-cache postgresql-dev python3-dev gcc musl-dev

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements

# Virtualenv
RUN python3 -m venv /env && \
    . /env/bin/activate &&\
    pip install --upgrade pip &&\
    pip install -r /requirements/local.txt

COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

# ENTRYPOINT ["/entrypoint"]
