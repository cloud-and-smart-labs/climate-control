FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN pip install websockets
COPY broker.py .
CMD [ "python3", "/usr/src/app/broker.py"]