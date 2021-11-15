from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, to_json, array, col
import argparse


def main(args):
    spark = setUpSparkSession()
    dataFrame = loadKafkaTopicStream(spark, args.kafka_servers)
    dataFrame = mapToOriginScheme(dataFrame)
    dataFrame = analyzeNdwiImages(dataFrame)
    # writeKafkaTopic(dataFrame, args.kafka_servers)
    spark.stop()


def setUpSparkSession():
    # spark = SparkSession.builder.appName("ndwi-analyzer") \
    #     .config('spark.master', 'spark://spark-master:7077') \
    #     .config('spark.executor.cores', 1) \
    #     .config('spark.cores.max', 1) \
    #     .config('spark.executor.memory', '1g') \
    #     .config('spark.sql.streaming.checkpointLocation', 'hdfs://namenode:9000/stream-checkpoint1/') \
    #     .getOrCreate()
    spark = SparkSession.builder.master("local[4]").appName("ndwi-analyzer").getOrCreate()
    spark.sparkContext.setLogLevel('WARN')
    return spark


def loadKafkaTopicStream(spark, kafka_servers):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_servers) \
        .option("startingOffsets", "earliest") \
        .option("subscribe", "ndwi_images") \
        .load()


def mapToOriginScheme(dataFrame):
    schema = createOriginSchema()
    dataFrame = dataFrame.selectExpr("CAST(value AS STRING)")
    dataFrame = dataFrame.select(
        from_json(col("value"), schema).alias("data")).select("data.*")
    return dataFrame


def createOriginSchema():
    return StructType() \
        .add("countryCode", StringType())\
        .add("locationName", StringType())\
        .add("geoPosition", MapType(StringType(), DoubleType()))\
        .add("date", DateType())\
        .add("imageName", StringType())\
        .add("image_bytes", StringType())

def process_row(row):
    print("Pretty pls")
    print(row)

def analyzeNdwiImages(dataFrame):
    query = dataFrame.writeStream.foreach(process_row).start().awaitTermination(10)


def createResultSchema():
    return StructType() \
        .add("countryCode", StringType())\
        .add("locationName", StringType())\
        .add("geoPosition", MapType(StringType(), DoubleType()))\
        .add("date", DateType())\
        .add("land_squareMeters", DoubleType())\
        .add("land_percentages", DoubleType())\
        .add("water_squareMeters", DoubleType())\
        .add("water_percentages", DoubleType())


def writeKafkaTopic(dataFrame, kafka_servers):
    dataFrame.writeStream\
        .format('kafka')\
        .option("kafka.bootstrap.servers", kafka_servers)\
        .option("topic", "ndwi_results")\
        .start().awaitTermination()


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Analyze sentinel 2 NDWI images saved in ndwi_images kafka topic')
    parser.add_argument('--kafka_servers', type=str, default="kafka:9092",
                        help='The kafka servers to consume/produce messages from/to (comma separated)')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()
    main(args)
