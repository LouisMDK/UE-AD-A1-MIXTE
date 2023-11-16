FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m pip install -U pip && \
    pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

ADD . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "booking.py"]