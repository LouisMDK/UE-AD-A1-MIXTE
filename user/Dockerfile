FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .

RUN python3 -m pip install -U pip && \
    pip3 install --upgrade setuptools

RUN pip3 install -r requirements.txt

ADD . .

ENTRYPOINT ["python3", "user.py"]