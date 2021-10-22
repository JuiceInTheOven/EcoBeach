FROM osgeo/gdal:latest

RUN apt-get update -y
RUN apt-get install -y git libgeos-dev python3 python3-pip python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY main.py .

CMD [ "python", "main.py"]