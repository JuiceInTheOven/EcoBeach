FROM python:latest

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY map.geojson .  
COPY main.py .

CMD [ "python", "main.py" ]