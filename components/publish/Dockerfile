FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN pip install pyserial websockets
COPY publish.py .
CMD [ "python3", "/usr/src/app/publish.py"]