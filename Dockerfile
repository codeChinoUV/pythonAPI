FROM python:3.9

WORKDIR /usr/src/api
COPY requeriments.txt .

RUN pip install --no-cache-dir -r requeriments.txt 
COPY . .
