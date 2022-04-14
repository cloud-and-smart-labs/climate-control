FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN pip install pyserial websockets
COPY subscribe.py .
CMD [ "python3", "/usr/src/app/subscribe.py"]