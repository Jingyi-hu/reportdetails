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

def grid(gdf):
 
    gdf['grid'] = gdf.apply(lambda x:(x['lon_id'],x['lat_id']),axis=1)
    gdf = gdf.sort_values(by = ['lon_id','lat_id'])
    grid = [0]*len(gdf['grid'].unique())

    for grids in gdf['grid'].unique():
        grid_data = gdf[gdf['grid'].isin([grids])]
        grid.append(grid_data)   
    grid = list(filter(lambda x: not isinstance(x, int), grid))
    
    return grid

class TestGrid(unittest.TestCase):
    def test_grid(self):
        
        points = gpd.GeoDataFrame({
            'geometry': [shapely.geometry.Point([0, 0]),
                         shapely.geometry.Point([0.5, 1]),
                         shapely.geometry.Point([1, 0]),
                         shapely.geometry.Point([1.5, 0.5])]
                })
        points_new = grid_create(points,1,1)[2]
        
        test0 = gpd.GeoDataFrame({
                'geometry': [shapely.geometry.Point([0, 0])],
                'lon_id': [0],
                'lat_id': [0],
                'grid':[(0,0)]
                })
        test2 = gpd.GeoDataFrame({
                'geometry': [shapely.geometry.Point([1, 0]),
                             shapely.geometry.Point([1.5, 0.5])],
                'lon_id': [1,1],
                'lat_id': [0,0],
                'grid':[(1,0),(1,0)]
                })
        
        pd.testing.assert_frame_equal(grid(points_new)[0].reset_index(drop=True), test0)
        pd.testing.assert_frame_equal(grid(points_new)[2].reset_index(drop=True), test2)
        

unittest.main()