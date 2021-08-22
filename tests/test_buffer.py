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
from shapely.geometry import Point,Polygon

def buffer(gdf,building,x):
    
    bools_map = []
    for i in range (len(gdf)):
        bools_map.append(building.geometry.buffer(x).contains(gdf.iloc[i].geometry))   
    
    list_pd = pd.Series(bools_map,name = 'newbools')
    list_pd = list_pd.apply(lambda r:int(r))
    gdf = pd.concat([gdf,list_pd],axis = 1)
    gdf = gdf[gdf['newbools'] == 1]
    
    return gdf

class TestBuffer(unittest.TestCase):
    def test_buffer(self):
        
        polygon = gpd.GeoDataFrame({
            'geometry': [shapely.geometry.Polygon([(3, 3), (4, 3), (4, 4), (3, 4),(3, 3)])]
                })
        
        data = gpd.GeoDataFrame({
            'geometry': [shapely.geometry.Point([3.5, 3]),
                 shapely.geometry.Point([4.5, 4]),
                 shapely.geometry.Point([5, 2]),
                 shapely.geometry.Point([2, 6]),
                 shapely.geometry.Point([1, 2])
                ]
                })
        data_test = gpd.GeoDataFrame({
            'geometry': [shapely.geometry.Point([3.5, 3]),
                         shapely.geometry.Point([4.5, 4])
                ]
                })
                
        pd.testing.assert_frame_equal(buffer(data,polygon,1)[['geometry']].reset_index(drop=True), data_test)

unittest.main()