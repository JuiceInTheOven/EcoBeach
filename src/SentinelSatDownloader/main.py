#import logging
import os
import threading
import flask
from flask_restful import reqparse
from hdfs import InsecureClient
from osgeo import gdal
from sentinelloader import Sentinel2Loader
from shapely.geometry import Polygon

app = flask.Flask(__name__)
@app.route('/download', methods=['GET', 'POST'])
def download():
    args = parseRequestArgs()
    makeDir("downloads")
    def do_work(args):
        geoTiffs = downloadSentinelImages(args)
        saveToHdfs(geoTiffs)
        
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

        area = createBoundaryBox(args.position)
        geoTiffs = sl.getRegionHistory(area, 'TCI', '10m', args.fromdate, args.todate)
        return geoTiffs

def createBoundaryBox(position):
    # Creates a small rectangle boundary box around a position, where the position is at the center of the rectangle.
    longRectSize = 0.02
    latRectSize = 0.01
    topLeftCorner = (position[0]-longRectSize, position[1]+latRectSize)
    bottomLeftCorner = (position[0]-longRectSize, position[1]-latRectSize)
    bottomRightCorner = (position[0]+longRectSize, position[1]-latRectSize)
    topRightCorner = (position[0]+longRectSize, position[1]+latRectSize)

    return Polygon([topLeftCorner, bottomLeftCorner,
                    bottomRightCorner, topRightCorner, topLeftCorner])

def saveToHdfs(geoTiffs):
    client = InsecureClient('http://namenode:9870', user='root')
    #for geoTiff in geoTiffs:
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8686)