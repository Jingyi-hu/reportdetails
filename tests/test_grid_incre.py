import unittest

import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
import shapely
from shapely import wkt
import geopandas as gpd
from shapely.geometry import mapping
import math
from math import cos,sin

def grid_increment(gdf,x):

    R = 6371.004
    lon_min = gdf.geometry.x.min()
    lon_max = gdf.geometry.x.max()
    lat_min = gdf.geometry.y.min()
    lat_max = gdf.geometry.y.max()
    perimeter = 2*math.pi*R*1000
    radian = perimeter*cos(((lat_min+lat_max)/2)*(2*math.pi/360))
   
    lon_incre = x*360/radian
    lat_incre = x*360/perimeter
    
    return lon_incre,lat_incre

class TestGridIncrement(unittest.TestCase):
    def test_grid_increment(self):        
        points = gpd.GeoDataFrame({
                'geometry': [shapely.geometry.Point([0, 0]),
                 shapely.geometry.Point([0, 1]),
                 shapely.geometry.Point([1, 1]),
                 shapely.geometry.Point([1, 0])]
                })
        
        self.assertEqual(round(grid_increment(points,55500)[0],1), 0.5)
        self.assertEqual(round(grid_increment(points,55500)[1],1), 0.5)
        
        
unittest.main()