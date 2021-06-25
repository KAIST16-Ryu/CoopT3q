FROM python:3

RUN mkdir /examples
WORKDIR "/examples"

COPY requirements.txt ./
COPY bootstrapper.py ./
COPY Train.py ./

RUN pip3 install --no-cache-dir -r requirements.txt

