from osgeo import gdal
import sentinel2loader as sl2
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

def scrape(args):
    user = args.user
    passw = args.parser

    sl = sl2.Sentinel2Loader('downloads', user, passw, cloudCoverage=(0,1), loglevel=logging.INFO)
    dfs = pd.read_excel("DK_beaches.xlsx", sheet_name="DK_BW2020")

    # We shuffle the possible indexes, to randomize which location is queried first, to use the 20 LTA retries on different products.
    for ri in range(1): #randomIndexesInDfs(dfs):
        locationName = dfs.iloc[ri][3]
        lon = dfs.iloc[ri][6]
        lat = dfs.iloc[ri][7]

        today = date.today()
        week_ago = today - date.timedelta(days=7)
        area = createSearchArea(lon, lat, 2)
        geoTiffs = []
        if(args.days != None):
            geoTiffs = sl.getRegionHistory(area, 'NDWI2', '10m', str(today - date.timedelta(days=args.days)), today)
        else:
            geoTiffs = sl.getRegionHistory(area, 'NDWI2', '10m', str(week_ago), str(today), daysStep=1)
        for geoTiff in geoTiffs:  
            geoTiffDate = geoTiff.split("-NDWI2")[0].split("tmp/")[1] # gets the date part from the geoTiff path
            imageName = f"{locationName}-{geoTiffDate}.png"
            imagePath = f"processed/{imageName}"
            if(not os.path.exists("processed")):
                os.mkdir("processed")
            if(not os.path.isfile(imagePath)): #We only want create and publish new images.
                createBlackAndWhiteImg(geoTiff, imagePath)
                #publishToKafkaTopic(locationName, [lon, lat], geoTiffDate, imageName)
            os.remove(geoTiff) # We remove tmp files after they are used
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
    cmap = colors.ListedColormap(['black', 'white'])
    bounds=[0,6,10]
    colors.BoundaryNorm(bounds, cmap.N)
    return cmap

def publishToKafkaTopic(locationName, geoPosition, date, imageName):
    image_bytes = open(f"processed/{imageName}", "rb").read()
    producer = KafkaProducer(bootstrap_servers='helsinki.faurskov.dev:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send('ndwi_images', {"locationName": locationName, "geoPosition": {"lon": geoPosition[0], "lat": geoPosition[1]}, "date": date, "imageName": imageName, "image_bytes": image_bytes })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape Sentinel Satellite Imagery based on list of positions (lat, lon), and metadata.')
    parser.add_argument('--days', type=int, default=None, help='Days to scrape for')
    parser.add_argument('--user', type=str, default="nikolai.damm", help="Cupernicus username")
    parser.add_argument('--pass', type=str, default="fywfuP-qekfut-xomki3", help="Cupernicus password")
    args = parser.parse_args()
    scrape(args)