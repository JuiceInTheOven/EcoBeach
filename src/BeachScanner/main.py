import folium
import geopandas as gdp
from pandas.core import api
from sentinelsat import SentinelAPI
import rasterio
#import matplotlib.pyplot as plt
#from rasterio import plot
#from rasterio.plot import show
#from rasterio.mask import geometry_mask
#from osgeo import gdal

def main():
    m = folium.Map([50.20, 11.4], zoom_start=11)
    boundary = gdp.read_file("./map.geojson")
    folium.GeoJson(boundary).add_to(m)
    footprint = None
    for i in boundary['geometry']:
        footprint = i
    
    user = "nikolai.damm"
    password = "fywfuP-qekfut-xomki3"

    api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')
    products = api.query(footprint,
                     date = ('20200109', '20200510'),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0, 20))
    gdf = api.to_geodataframe(products)
    gdf_sorted = gdf.sort_values(['cloudcoverpercentage'], ascending=[True])
    api.download(i);
    bands = r'...\GRANULE\L2A_T18TWL_A025934_20200609T155403\IMG_DATA\R10m'
    blue = rasterio.open(bands+'\T18TWL_20200609T154911_B02_10m.jp2') 
    green = rasterio.open(bands+'\T18TWL_20200609T154911_B03_10m.jp2') 
    red = rasterio.open(bands+'\T18TWL_20200609T154911_B04_10m.jp2') 
    with rasterio.open('image_name.tiff','w',driver='Gtiff', width=blue.width, height=blue.height, count=3, crs=blue.crs,transform=blue.transform, dtype=blue.dtypes[0]) as rgb:
        rgb.write(blue.read(1),3) 
        rgb.write(green.read(1),2) 
        rgb.write(red.read(1),1) 
        rgb.close()
        

if __name__ == '__main__':
    main();