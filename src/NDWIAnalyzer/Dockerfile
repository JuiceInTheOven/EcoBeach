FROM bde2020/spark-python-template:3.1.1-hadoop3.2

COPY README.md .
ONBUILD COPY requirements.txt .
ONBUILD RUN pip3 install -r requirements.txt
	  
ONBUILD COPY analyzer.py .

ENV SPARK_APPLICATION_PYTHON_LOCATION /analyzer.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0"