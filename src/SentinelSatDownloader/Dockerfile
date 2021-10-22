FROM python:latest

RUN apt-get update &&\
    apt-get install -y libgdal-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD [ "python", "main.py"]