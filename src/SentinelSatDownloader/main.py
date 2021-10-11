import threading
import flask
import os
import glob
from flask_restful import reqparse
from sentinelsat import SentinelAPI, make_path_filter
from osgeo import gdal


app = flask.Flask(__name__)
# http://x.x.x.x:105/persist?position=10 11&fromdate=YYYYMMDD&todate=YYYYMMDD
@app.route('/download', methods=['GET', 'POST'])
def download():
    args = parseRequestArgs()
    def do_work(args):
        ChangeArgPositionIntoArrayOfFloats(args)

        user = "nikolai.damm"
        password = "fywfuP-qekfut-xomki3"

        rectangleQuery = createRectangleWtkQueryFromArgs(args)

        api, products = querySentinelSatApi(args, user, password, rectangleQuery)

        downloadProducts(api, products)

        convertJP2FilesToTiff()
        

    thread = threading.Thread(target=do_work, kwargs={'args': args})
    thread.start()

    return flask.make_response("Download started!", 201)

def parseRequestArgs():
    parser = reqparse.RequestParser()
    parser.add_argument('position', type=str, help='a list of positions -> lat lon')
    parser.add_argument('fromdate', type=str, help="The earliest date to get map data from -> 'YYYYMMDD'")
    parser.add_argument('todate', type=str, help="The latest date to get map data from -> 'YYYYMMDD' or 'NOW' for current date")

    args = parser.parse_args()
    return args

def ChangeArgPositionIntoArrayOfFloats(args):
    positions = args.position.split()
    args.position = [float(positions[0]), float(positions[1])]

def createRectangleWtkQueryFromArgs(args):
    # Creates a small rectangle boundary box around a position, where the position is at the center of the rectangle.
    latRectSize = 0.005
    longRectSize = 0.0025
    topLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]+longRectSize}"
    bottomLeftCorner = f"{args.position[0]-latRectSize} {args.position[1]-longRectSize}"
    bottomRightCorner = f"{args.position[0]+latRectSize} {args.position[1]-longRectSize}"
    topRightCorner = f"{args.position[0]+latRectSize} {args.position[1]+longRectSize}"

    # Creates a GeoJSON rectangle query in the well known text (wtk) format that queries the sentinel satellite for maps that contain our rectangle query.
    rectangleQuery = f"POLYGON (({topLeftCorner}, {bottomLeftCorner}, {bottomRightCorner}, {topRightCorner}, {topLeftCorner}))"
    return rectangleQuery

def querySentinelSatApi(args, user, password, rectangleQuery):
    api = SentinelAPI(user, password)
    623680114746094
    products = api.query(rectangleQuery,
                platformname = 'Sentinel-2',
                processinglevel = 'Level-2A',
                date = (args.fromdate, args.todate),
                cloudcoverpercentage=(0, 20))
                
    return api,products

def downloadProducts(api, products):
    nodefilter = make_path_filter("*/granule/*/img_data/r10m/*_tci_10m.jp2")
    api.download_all(products, "downloads", nodefilter=nodefilter)

def convertJP2FilesToTiff(outputFolder = "processed"):
    files = GetFiles
    for index, inputRasterPath in enumerate(files):
        # imgRasterInfo = GetRasterInfo(inputRaster=imgPath)
        if not outputFolder:
            newRasterPath = os.path.join(os.path.dirname(inputRasterPath),
                                         os.path.basename(inputRasterPath)[:-4] + ".tif")
            print("newRasterPath=", newRasterPath)
        else:
            newRasterPath = os.path.join(outputFolder,
                                         os.path.basename(inputRasterPath)[:-4] + ".tif")
            print("newRasterPath=", newRasterPath)

        srcDS = gdal.Open(inputRasterPath)
        gdal.Translate(newRasterPath, srcDS, format="GTiff", outputType=gdal.GDT_Float64)
    return

def GetFiles():
    filesList = []
    for file in glob.glob("./downloads/**/granule/**/img_data/r10m/*.jp2"):
        filesList.append(file)
    filesList.sort()
    return filesList

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)