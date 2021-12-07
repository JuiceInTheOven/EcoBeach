from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_json, struct, to_json, col, udf
import argparse
import base64
import io
from collections import Counter
from PIL import Image


def main(args):
    spark = setUpSparkSession()
    dataFrame = loadKafkaTopicStream(spark, args.kafka_servers)
    dataFrame = mapToOriginScheme(dataFrame)
    dataFrame = processNdwiImages(dataFrame)
    writeKafkaTopic(dataFrame, args.kafka_servers)
    spark.stop()


def setUpSparkSession():
    spark = SparkSession.builder \
        .appName("ndwi-analyzer") \
        .master('spark://spark-master:7077')\
        .config('spark.executor.memory', '2g') \
        .config('spark.sql.streaming.checkpointLocation', 'webhdfs://namenode:9000') \
        .getOrCreate()
    spark.sparkContext.setCheckpointDir('webhdfs://namenode:9000')
    spark.sparkContext.setLogLevel('WARN')
    return spark


def loadKafkaTopicStream(spark, kafka_servers):
    return spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_servers) \
        .option("startingOffsets", "earliest")\
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


def processNdwiImages(dataFrame):
    dataFrame = dataFrame.withColumn(
        "land_squareMeters", calculateLandSquareMeters(dataFrame.image_bytes))  # cant refactor this method, as the parameters are validated by spark to match dataframe column names.
    dataFrame = dataFrame.withColumn(
        "land_percentage",  calculatePercentage(dataFrame.image_bytes, dataFrame.land_squareMeters))
    dataFrame = dataFrame.withColumn(
        "water_squareMeters",  calculateWaterSquareMeters(dataFrame.image_bytes))
    dataFrame = dataFrame.withColumn(
        "water_percentage",  calculatePercentage(dataFrame.image_bytes, dataFrame.water_squareMeters))
    dataFrame = dropUnneededTables(dataFrame)
    return dataFrame


@udf(returnType=IntegerType())
def calculateLandSquareMeters(imageBytes):
    return countPixelsFromRgb(createImage(imageBytes), (0, 0, 0, 255)) * 10


@udf(returnType=DoubleType())
def calculatePercentage(imageBytes, squareMeters):
    image = createImage(imageBytes)
    width, height = image.size
    return squareMeters/((width * height) * 10)


@udf(returnType=IntegerType())
def calculateWaterSquareMeters(imageBytes):
    return countPixelsFromRgb(createImage(imageBytes), (255, 255, 255, 255)) * 10


def createImage(imageBytes):
    base64_imageBytes = imageBytes.encode()
    imageBytes = base64.b64decode(base64_imageBytes)
    return Image.open(io.BytesIO(imageBytes))


def countPixelsFromRgb(image, rgb):
    pixels = image.getdata()
    counter = Counter(pixels)
    return counter[rgb]


def dropUnneededTables(dataFrame):
    dataFrame = dataFrame.drop(dataFrame.imageName)
    dataFrame = dataFrame.drop(dataFrame.image_bytes)
    return dataFrame


def writeKafkaTopic(dataFrame, kafka_servers):
    dataFrame.select(to_json(struct([dataFrame[x] for x in dataFrame.columns])).alias("value")).select("value")\
        .writeStream\
        .format('kafka')\
        .outputMode("append")\
        .option("kafka.bootstrap.servers", kafka_servers)\
        .option("topic", "ndwi_results")\
        .start().awaitTermination(3600)


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Analyze sentinel 2 NDWI images saved in ndwi_images kafka topic')
    parser.add_argument('--kafka_servers', type=str, default="kafka:9092",
                        help='The kafka servers to consume/produce messages from/to (comma separated)')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()
    results = []
    main(args)
