FROM bde2020/spark-submit:3.1.1-hadoop3.2

COPY template.sh /
COPY requirements.txt /app/requirements.txt
COPY app.py /app/app.py
COPY submit.sh /submit.sh

ENV ENABLE_INIT_DAEMON false
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/app.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"

CMD ["/bin/bash", "/template.sh"]