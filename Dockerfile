FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get clean \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
