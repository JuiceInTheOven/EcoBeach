import logging
import os
import flask
import threading
from flask_restful import reqparse
from osgeo import gdal
import matplotlib.pyplot as plt
from sentinelloader import Sentinel2Loader
from shapely.geometry import Polygon

app = flask.Flask(__name__)
@app.route('/download', methods=['GET', 'POST'])
def download():
    args = parseRequestArgs()
    def do_work(args):
        sl = Sentinel2Loader('downloads', 
            args.username, args.password,
            apiUrl='https://apihub.copernicus.eu/apihub/', showProgressbars=True, loglevel=logging.DEBUG)

        area = createBoundaryBox(args.position)

        geoTiffs = sl.getRegionHistory(area, 'TCI', '10m', args.fromdate, args.todate, daysStep=5)
        for geoTiff in geoTiffs:
            print('Desired image was prepared at')
            print(geoTiff)

        #saveImagesToHdfs()

        #cleanup()
        
    thread = threading.Thread(target=do_work, kwargs={'args': args})
    thread.start()

    return flask.make_response("Download started!", 201)

def parseRequestArgs():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, help='copernicus account username')
    parser.add_argument('password', type=str, help='copernicus account password')
    parser.add_argument('position', type=str, help='a list of positions -> lat lon')
    parser.add_argument('fromdate', type=str, help="The earliest date to get map data from -> 'YYYYMMDD'")
    parser.add_argument('todate', type=str, help="The latest date to get map data from -> 'YYYYMMDD' or 'NOW' for current date")

    args = parser.parse_args()
    positions = args.position.split(" ")
    args.position = [float(positions[0]), float(positions[1])]
    return args


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

def cleanup():
    dir_path = 'downloads'

    try:
        shutil.rmtree(dir_path)
    except OSError as e:
        print("Error: %s : %s" % (dir_path, e.strerror))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8686)