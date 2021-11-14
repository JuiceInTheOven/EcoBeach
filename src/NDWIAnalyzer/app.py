from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, to_json, array, col


def main():
    spark = setUpSparkSession()
    dataFrame = loadKafkaTopicStream(spark)
    # dataFrame = analyzeNdwiImages(dataFrame)
    # writeKafkaTopic(dataFrame)
    spark.stop()


def setUpSparkSession():
    return SparkSession.builder.appName("ndwi-analyzer") \
        .config('spark.master', 'spark://spark-master:7077') \
        .config('spark.executor.cores', 1) \
        .config('spark.cores.max', 1) \
        .config('spark.executor.memory', '1g') \
        .config('spark.sql.streaming.checkpointLocation', 'hdfs://namenode:9000/stream-checkpoint/') \
        .getOrCreate()


def loadKafkaTopicStream(spark):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "helsinki.faurskov.dev:9093, falkenstein.faurskov.dev:9095, nuremberg.faurskov.dev:9097") \
        .option("subscribe", "ndwi_images") \
        .load()


def analyzeNdwiImages(dataFrame):
    data = dataFrame.selectExpr(
        "CAST(value AS STRING)"
    )
    print(data)
    data = dataFrame.selectExpr(
        "CAST(countryCode AS STRING)",
        "CAST(locationName AS STRING)",
        "CAST(geoPosition AS STRING)",
        "CAST(date AS STRING)",
        "CAST(imageName AS STRING)",
        "CAST(image_bytes AS STRING"
    )
    print(data)
    #resultSchema = createResultSchema()
    #resultDataFrame
    #mergedColumns = filteredWordCounts.withColumn('value', array(columns))
    #return


def createResultSchema():
    return [col('countryCode'),
            col('locationName'),
            col('geoPosition'),
            col('date'),
            col('land_squareMeters'),
            col('land_percentages'),
            col('water_squareMeters'),
            col('water_percentages')]


def writeKafkaTopic(dataFrame):
    dataFrame.selectExpr("CAST(value AS STRING)").writeStream \
        .format('kafka') \
        .option("kafka.bootstrap.servers", "kafka:9092") \
        .option("topic", "sentences") \
        .start().awaitTermination()


if __name__ == '__main__':
    main()
