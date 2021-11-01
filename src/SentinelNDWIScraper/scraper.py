from sys import api_version
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

    sl = sl2.Sentinel2Loader('downloads', user, passw, cloudCoverage=(0,1), loglevel=logging.INFO)
    dfs = pd.read_excel(f"{args.countrycode}.xlsx", sheet_name=args.countrycode)

    # We shuffle the possible indexes, to randomize which location is queried first, to use the 20 LTA retries on different products.
    for ri in randomIndexesInDfs(dfs):
        locationName = dfs.iloc[ri][3].lower().replace('.', '')
        lon = dfs.iloc[ri][6]
        lat = dfs.iloc[ri][7]

        today = date.today()
        geoTiffs = sl.getRegionHistory(createSearchArea(lon, lat, 2), 'NDWI2', '10m', str(today - timedelta(days=args.days)), str(today), daysStep=1)
        for geoTiff in geoTiffs:  
            geoTiffDate = geoTiff.split("-NDWI2")[0].split("tmp/")[1] # gets the date part from the geoTiff path
            imageName = f"{locationName}-{geoTiffDate}.png"
            imagePath = f"processed/{imageName}"
            if(not os.path.exists("processed")):
                os.mkdir("processed")
            if(not os.path.isfile(imagePath)): #We only want create and publish new images.
                createBlackAndWhiteImg(geoTiff, imagePath)
                publishToKafkaTopic(args.kafka_servers, locationName, [lon, lat], geoTiffDate, imageName)
            os.remove(geoTiff) # We remove tmp files after they are used
        if(os.path.exists("downloads")):
            shutil.rmtree("downloads") # We have to cleanup cached products when we have used them, as they take up a lot of space.

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

def createBlackAndWhiteImg(inFile, outFile):
    img = cv2.imread(inFile, -1) #MatPlotLib does not work with Float16 .tiff files, so we use OpenCV to read the .tiff file
    cmap = blackAndWhiteColorMap()
    plt.imsave(outFile, img, cmap=cmap)

def blackAndWhiteColorMap():
    cmap = colors.ListedColormap(['black', 'black', 'black', 'white', 'white']) # value 3/5 = 0.68 
    return cmap

def publishToKafkaTopic(kafka_servers, locationName, geoPosition, date, imageName):
    image_bytes = open(f"processed/{imageName}", "rb").read()
    image_bytes_base64 = base64.b64encode(image_bytes)
    producer = KafkaProducer(bootstrap_servers=kafka_servers, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('ndwi_images_test', {"locationName": locationName, "geoPosition": {"lon": geoPosition[0], "lat": geoPosition[1]}, "date": date, "imageName": imageName, "image_bytes": image_bytes_base64.decode() })

def parseArguments():
    parser = argparse.ArgumentParser(description='Scrape Sentinel Satellite Imagery based on list of positions (lat, lon), and metadata.')
    parser.add_argument('--days', type=int, default=7, help='Days to scrape for')
    parser.add_argument('--countrycode', type=str, default="dk", help='The country to scrape data for')
    parser.add_argument('--kafka_servers', type=str, default="helsinki.faurskov.dev:9093, falkenstein.faurskov.dev:9095, nuremberg.faurskov.dev:9097", help='The kafka servers to produce messages to (comma separated)')
    parser.add_argument('--username', type=str, default="nikolai.damm", help="Cupernicus username")
    parser.add_argument('--password', type=str, default="fywfuP-qekfut-xomki3", help="Cupernicus password")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parseArguments()
    scrape(args)