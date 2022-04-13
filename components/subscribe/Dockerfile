FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN pip install pyserial
COPY controller.py .
CMD [ "python3", "/usr/src/app/controller.py"]