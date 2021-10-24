import os
import threading
import flask
from flask_restful import reqparse
from hdfs import InsecureClient
from osgeo import gdal
from sentinelloader import Sentinel2Loader
from shapely.geometry import Polygon
import pyarrow.parquet as pq
import pandas as pd
import pyarrow as pa

app = flask.Flask(__name__)
@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    args = parseRequestArgs()
    makeDir("downloads")
    def do_work(args):
        geoTiffs = downloadSentinelImages(args)
        saveToHdfs(args.position, geoTiffs)
        
    thread = threading.Thread(target=do_work, kwargs={'args': args})
    thread.start()

    return flask.make_response("Download started!", 201)

def makeDir(dirname):
    try: 
        os.mkdir(dirname) 
    except OSError as error: 
        print(error)  

def parseRequestArgs():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='copernicus account username')
    parser.add_argument('password', type=str, help='copernicus account password')
    parser.add_argument('position', type=str, help='a list of positions -> lat lon')
    parser.add_argument('fromdate', type=str, help="The earliest date to get map data from -> 'YYYYMMDD'")
    parser.add_argument('todate', type=str, help="The latest date to get map data from -> 'YYYYMMDD' or 'NOW' for current date")

    args = parser.parse_args()
    positions = args.position.split()
    args.position = [float(positions[0]), float(positions[1])]
    return args

def downloadSentinelImages(args):
        sl = Sentinel2Loader('downloads', 
            args.username, args.password, cloudCoverage=(0,20), cacheTilesData=False)

        area = createBoundaryBox(args.position, 2)
        geoTiffs = sl.getRegionHistory(area, 'TCI', '10m', args.fromdate, args.todate)
        return geoTiffs

def createBoundaryBox(position, size):
    # Creates a small rectangle boundary box around a position, where the position is at the center of the rectangle.
    longRectSize = size/100
    latRectSize = longRectSize/2
    topLeftCorner = (position[0]-longRectSize, position[1]+latRectSize)
    bottomLeftCorner = (position[0]-longRectSize, position[1]-latRectSize)
    bottomRightCorner = (position[0]+longRectSize, position[1]-latRectSize)
    topRightCorner = (position[0]+longRectSize, position[1]+latRectSize)

    return Polygon([topLeftCorner, bottomLeftCorner,
                    bottomRightCorner, topRightCorner, topLeftCorner])

def saveToHdfs(position, geoTiffs):
    client = InsecureClient('http://namenode:9870', user='root')
    df = pd.DataFrame(columns=["date", 'image_tiff'])
    for geoTiff in geoTiffs:
        date = geoTiff.split("/")[2].split("-TCI")[0]
        bytes = open(geoTiff, "rb").read()
        df = df.append({"date": date, "image_tiff": bytes}, ignore_index=True)
    table = pa.Table.from_pandas(df)
    fileName = f'{position[0]}-{position[1]}.parquet'
    pq.write_table(table, fileName)
    client.upload('/', fileName, overwrite=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)