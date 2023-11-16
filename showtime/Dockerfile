FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .

RUN apt update && \
    apt install -y build-essential python3-dev

RUN pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt --no-cache-dir

ADD . .

ENV PYTHONUNBUFFERED=1

RUN python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. showtime.proto

ENTRYPOINT ["python3", "showtime.py"]