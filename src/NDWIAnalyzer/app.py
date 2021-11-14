from pyspark.sql import SparkSession
# Start a SparkSession, and configure it like last time
spark = SparkSession.builder.appName('streamTest') \
    .config('spark.master','spark://spark-master:7077') \
    .config('spark.executor.cores', 1) \
    .config('spark.cores.max',1) \
    .config('spark.executor.memory', '2g') \
    .config('spark.yarn.executor.memoryOverhead', 500) \
    .config('spark.sql.streaming.checkpointLocation','hdfs://namenode:9000/stream-checkpoint/') \
    .getOrCreate()

print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")
print("I Work!!!!")

# df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", "host1:port1,host2:port2") \
#   .option("subscribe", "topic1") \
#   .load()
# df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# df.selectExpr("CAST(value AS STRING)").writeStream \
#     .format('kafka') \
#     .option("kafka.bootstrap.servers", "kafka:9092") \
#     .option("topic", "sentences") \
#     .start().awaitTermination()

#spark.stop()