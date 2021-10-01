FROM python:latest

ONBUILD COPY requirements.txt /app/
ONBUILD RUN pip3 install -r /app/requirements.txt
	  
COPY main.py /app/