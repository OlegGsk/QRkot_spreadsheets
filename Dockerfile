FROM python:3.9.17

WORKDIR /QRKot_Spreadsheets

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install -r /QRKot_Spreadsheets/requirements.txt --no-cache-dir

COPY alembic alembic

COPY alembic.ini alembic.ini

COPY app app
