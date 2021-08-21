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
from shapely.geometry import Polygon

def grid_create(gdf,lon_incre,lat_incre):

    lon_min = gdf.geometry.x.min()
    lat_min = gdf.geometry.y.min()
    gdf['lon_id'] = gdf.apply(lambda r:int((r.geometry.x-lon_min)/lon_incre),axis=1)
    gdf['lat_id'] = gdf.apply(lambda r:int((r.geometry.y-lat_min)/lat_incre),axis=1)
    log_num = len(gdf['lon_id'].unique())
    lat_num = len(gdf['lat_id'].unique())
    geometry = []
    
    for i in range(len(gdf['lon_id'].unique())):
        for j in range(len(gdf['lat_id'].unique())):
            geometry.append(Polygon([
                (lon_min+i*lon_incre,lat_min+j*lat_incre),
                (lon_min+(i+1)*lon_incre,lat_min+j*lat_incre),
                (lon_min+(i+1)*lon_incre,lat_min+(j+1)*lat_incre),
                (lon_min+i*lon_incre,lat_min+(j+1)*lat_incre)]))
        
    created_grid = gpd.GeoDataFrame()
    created_grid['geometry'] = geometry

    grip_map = created_grid[created_grid.intersects(gdf.unary_union)]
    
    return created_grid,grip_map,gdf

class TestGridCreate(unittest.TestCase):
    def test_grid_create(self):
        
        points = gpd.GeoDataFrame({
                'geometry': [shapely.geometry.Point([0, 0]),
                 shapely.geometry.Point([0.5, 1]),
                 shapely.geometry.Point([1, 0])]
                })
        test0 = gpd.GeoDataFrame({
                'geometry': [
                    shapely.geometry.Polygon([(0,0),(1,0),(1,1),(0,1),(0,0)]),
                    shapely.geometry.Polygon([(0,1),(1,1),(1,2),(0,2),(0,1)]),
                    shapely.geometry.Polygon([(1,0),(2,0),(2,1),(1,1),(1,0)]),
                    shapely.geometry.Polygon([(1,1),(2,1),(2,2),(1,2),(1,1)])]
                })
        test1 = gpd.GeoDataFrame({
                'geometry': [
                    shapely.geometry.Polygon([(0,0),(1,0),(1,1),(0,1),(0,0)]),
                    shapely.geometry.Polygon([(0,1),(1,1),(1,2),(0,2),(0,1)]),
                    shapely.geometry.Polygon([(1,0),(2,0),(2,1),(1,1),(1,0)])]
                })
        
        test2 = gpd.GeoDataFrame({
                'geometry': points.geometry,
                'lon_id': [0,0,1],
                'lat_id': [0,1,0]
                })
        
        pd.testing.assert_frame_equal(grid_create(points,1,1)[0].reset_index(drop=True), test0)
        pd.testing.assert_frame_equal(grid_create(points,1,1)[1].reset_index(drop=True), test1)
        pd.testing.assert_frame_equal(grid_create(points,1,1)[2].reset_index(drop=True), test2)
        

    
unittest.main()
        
        
        
        