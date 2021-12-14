import sentinel2loader_lib as sl2
from shapely.geometry import Polygon
import pandas as pd
from datetime import date, timedelta
from matplotlib import colors
import matplotlib.pyplot as plt
import cv2
import os
import shutil
import random
import json
import logging
from kafka import KafkaProducer
import argparse
import base64


def scrape(args):
    user = args.username
    passw = args.password

    sl = sl2.Sentinel2Loader('downloads', user, passw,
                             cloudCoverage=(0, 1), loglevel=logging.INFO)
    dfs = pd.read_excel(
        f"beach_datasets/{args.countrycode}.xlsx", sheet_name=args.countrycode)

    # We shuffle the possible indexes, to randomize which location is queried first, to use the 20 LTA retries on different products.
    for ri in randomIndexesInDfs(dfs):
        countryCode = dfs.iloc[ri][0]
        locationName = dfs.iloc[ri][3].replace(".", "").replace("/", "_").title()
        lon = dfs.iloc[ri][6]
        lat = dfs.iloc[ri][7]

        today = date.today()
        geoTiffImages = sl.getRegionHistory(countryCode, locationName, createSearchArea(
            lon, lat, 2), 'NDWI_MacFeeters', '10m', str(today - timedelta(days=args.days)), str(today))
        processGeoTiffImages(
            args, countryCode, locationName, lon, lat, geoTiffImages)
        removeDownloadFolder()


def randomIndexesInDfs(dfs):
    randomNumberInDfsLen = list(range(len(dfs.index)))
    random.shuffle(randomNumberInDfsLen)
    return randomNumberInDfsLen


def createSearchArea(lon, lat, size):
    # Creates a small rectangle boundary box around a position, where the position is at the center of the rectangle.
    width = size/100
    height = width/2
    topLeftCorner = (lon-width, lat+height)
    bottomLeftCorner = (lon-width, lat-height)
    bottomRightCorner = (lon+width, lat-height)
    topRightCorner = (lon+width, lat+height)

    return Polygon([topLeftCorner, bottomLeftCorner,
                    bottomRightCorner, topRightCorner, topLeftCorner])


def processGeoTiffImages(args, countryCode, locationName, lon, lat, geoTiffImages):
    for geoTiffImage in geoTiffImages:
        # gets the date part from the geoTiff path
        date = geoTiffImage.split("-NDWI_MacFeeters")[0].split("tmp/")[1]
        imageName = f"{countryCode}-{locationName}-{date}.png"
        imagePath = f"processed/{imageName}"
        createProcessingFolder()
        processImage(args, countryCode, locationName, lon, lat,
                     geoTiffImage, date, imageName, imagePath)
        removeProcessedImage(geoTiffImage)

def createProcessingFolder():
    if(not processingFolderExists()):
        os.makedirs("processed")
        
def processingFolderExists():
    return os.path.exists("processed")

def processImage(args, countryCode, locationName, lon, lat, geoTiff, geoTiffDate, imageName, imagePath):
    # We only want create and publish new images.
    if(not processedImageExists(imagePath)):
        createBlackAndWhiteImg(geoTiff, imagePath)
        publishToKafkaTopic(args.kafka_servers, countryCode, locationName, [
                            lon, lat], geoTiffDate, imageName)
def processedImageExists(imagePath):
    return os.path.isfile(imagePath)


def createBlackAndWhiteImg(inFile, outFile):
    # MatPlotLib does not work with Float16 .tiff files, so we use OpenCV to read the .tiff file
    img = cv2.imread(inFile, -1)
    cmap = blackAndWhiteColorMap()
    plt.imsave(outFile, img, cmap=cmap)


def blackAndWhiteColorMap():
    cmap = colors.ListedColormap(
        ['black', 'black', 'black', 'white', 'white'])  # value 3/5 = 0.6
    return cmap


def publishToKafkaTopic(kafka_servers, countryCode, locationName, geoPosition, date, imageName):
    image_bytes = open(f"processed/{imageName}", "rb").read()
    image_bytes_base64 = base64.b64encode(image_bytes)
    producer = KafkaProducer(bootstrap_servers=kafka_servers,
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'), acks='all')
    producer.send('ndwi_images', {"countryCode": countryCode, "locationName": locationName, "geoPosition": {
                  "lon": geoPosition[0], "lat": geoPosition[1]}, "date": date, "image_bytes": image_bytes_base64.decode()})


def removeProcessedImage(geoTiffImage):
    os.remove(geoTiffImage)


def removeDownloadFolder():
    if(downloadFolderExists()):
        shutil.rmtree("downloads")


def downloadFolderExists():
    return os.path.exists("downloads")


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Scrape Sentinel Satellite Imagery based on list of positions (lat, lon), and metadata.')
    parser.add_argument('--days', type=int, default=7,
                        help='Days to scrape for')
    parser.add_argument('--countrycode', type=str, default="dk",
                        help='The country to scrape data for')
    parser.add_argument('--kafka_servers', type=str, default="kafka:9092",
                        help='The kafka servers to produce messages to (comma separated)')
    parser.add_argument('--username', type=str,
                        default="nikolai.damm", help="Cupernicus username")
    parser.add_argument('--password', type=str,
                        default="fywfuP-qekfut-xomki3", help="Cupernicus password")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parseArguments()
    scrape(args)
