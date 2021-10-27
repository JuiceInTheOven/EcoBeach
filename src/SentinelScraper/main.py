from osgeo import gdal
import sentinel2loader as sl2
from shapely.geometry import Polygon
import pandas as pd
from datetime import date
import time
from matplotlib import colors
import matplotlib.pyplot as plt
import cv2
import os
import shutil

def scrape():
    user = "nikolai.damm"
    passw = "fywfuP-qekfut-xomki3"

    sl = sl2.Sentinel2Loader('downloads', user, passw, cloudCoverage=(0,20))
    dfs = pd.read_excel("DK_beaches.xlsx", sheet_name="DK_BW2020")

    # len(dfs.index)
    for i in range(len(dfs.index)):
        locationName = dfs.iloc[i][3]
        lon = dfs.iloc[i][6]
        lat = dfs.iloc[i][7]

        area = createSearchArea(lon, lat, 2)

        geoTiffs = sl.getRegionHistory(area, 'NDWI2', '10m', "2015-01-01", str(date.today()))
        for geoTiff in geoTiffs:
            cmap = blackAndWhiteColorMap()
            img = cv2.imread(geoTiff, -1) #plt.imread does not work, so we use OpenCV to read the .tiff file
            geoTiffDate = geoTiff.split("-NDWI2")[0].split("tmp/")[1] # gets the date part from the geoTiff path
            processedImg = f"processed/{locationName}-{geoTiffDate}.png"
            if(not os.path.exists("processed")):
                os.mkdir("processed")
            plt.imsave(processedImg, img, cmap=cmap)
            #publishToTopic(locationName, [lon, lat], geoTiffDate, processedImg)
            os.remove(geoTiff)
        shutil.rmtree("downloads")

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

def blackAndWhiteColorMap():
    cmap = colors.ListedColormap(['black', 'white'])
    bounds=[0,5,10]
    colors.BoundaryNorm(bounds, cmap.N)
    return cmap

if __name__ == '__main__':
    scrape()