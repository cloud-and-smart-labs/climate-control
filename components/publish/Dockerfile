FROM python:3.9-slim-buster
WORKDIR /usr/src/app
RUN pip install pyserial
COPY read_serial_port.py .
CMD [ "python3", "/usr/src/app/read_serial_port.py"]