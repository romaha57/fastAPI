FROM python:3.11.6-alpine3.18

RUN mkdir /bookings

WORKDIR /bookings

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .