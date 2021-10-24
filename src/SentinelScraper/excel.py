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

dfs = pd.read_excel("DK_beaches.xlsx", sheet_name="DK_BW2020")
for i in range(len(dfs)-1000):
    print(f'{dfs.iloc[i][3]},{dfs.iloc[i][6]},{dfs.iloc[i][7]}')