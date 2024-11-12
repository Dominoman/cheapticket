# Don't use it!!!!
FROM python:3.12.7-slim-bullseye
LABEL authors="oraveczl"

WORKDIR /app

COPY . .

RUN mkdir tmp
RUN pip install -r requirements.txt
RUN alembic upgrade head

ENTRYPOINT ["python"]

CMD ["main.py"]
