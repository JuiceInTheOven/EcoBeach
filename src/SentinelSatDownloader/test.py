import logging
import os
from osgeo import gdal
import matplotlib.pyplot as plt
from sentinelloader import Sentinel2Loader
from shapely.geometry import Polygon

sl = SentinelLoader('/notebooks/data/output/sentinelcache', 
                    'mycopernicususername', 'mycopernicuspassword',
                    apiUrl='https://scihub.copernicus.eu/apihub/', showProgressbars=True, loglevel=logging.DEBUG)

area = Polygon([(-47.873796, -16.044801), (-47.933796, -16.044801),
        (-47.933796, -15.924801), (-47.873796, -15.924801)])

geoTiffs = sl.getRegionHistory(area, 'TCI', '60m', '2019-01-06', '2019-01-30', daysStep=5)
for geoTiff in geoTiffs:
    print('Desired image was prepared at')
    print(geoTiff)
    os.remove(geoTiff)