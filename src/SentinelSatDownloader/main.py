import rasterio
from rasterio import plot
from rasterio.plot import show
from rasterio.mask import geometry_mask
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
from datetime import date
from zipfile import ZipFile
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Download Sentinel Sattelite Map Data based on list of positions (lat, lon), and metadata.')
parser.add_argument('--position', type=float, nargs="+", help='a list of positions -> lat lon')
parser.add_argument('--fromdate', type=str, help="The earliest date to get map data from -> 'YYYYMMDD'")
parser.add_argument('--todate', type=str, default="NOW", help="The latest date to get map data from -> 'YYYYMMDD' or 'NOW' for current date")

args = parser.parse_args()

#Download satelite imagery of beach locations to sentinelsat/downloads
user = "nikolai.damm"
password = "fywfuP-qekfut-xomki3"

latRectSize = 0.005
longRectSize = 0.003

topLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]+longRectSize}"
bottomLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]-longRectSize}"
bottomRightCorner = f"{args.position[0]+latRectSize} {args.position[1]-longRectSize}"
topRightCorner = f"{args.position[0]+latRectSize} {args.position[1]+longRectSize}"

rectangleQuery = f"POLYGON (({topLeftCorner}, {bottomLeftCorner}, {bottomRightCorner}, {topRightCorner}, {topLeftCorner}))"

api = SentinelAPI(user, password)
623680114746094
products = api.query(rectangleQuery,
            platformname = 'Sentinel-2',
            processinglevel = 'Level-2A',
            date = (args.fromdate, args.todate),
            cloudcoverpercentage=(0, 20))

nodefilter = make_path_filter("*/granule/*/img_data/r10m/*_tci_10m.jp2")
api.download_all(products, "sentinelsat/downloads", nodefilter=nodefilter)

# Unpack all zip archives in sentinelsat_downloads to sentinelsat/unprocessed


# Save pj2 images to hdfs
