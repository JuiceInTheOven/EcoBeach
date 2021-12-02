FROM bde2020/spark-submit:3.1.1-hadoop3.2

COPY template.sh /

RUN apk add zlib-dev jpeg-dev gcc musl-dev python3-dev

COPY requirements.txt /app/
RUN cd /app \
      && pip3 install -r requirements.txt

COPY . /app

ENV ENABLE_INIT_DAEMON false
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/app.py
ENV SPARK_APPLICATION_ARGS ""
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2"

CMD ["/bin/bash", "/template.sh"]