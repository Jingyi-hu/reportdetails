import unittest

import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
from shapely import wkt
import geopandas as gpd
from shapely.geometry import mapping


def direction_south(gdf,building):

    longitude1 = gdf.geometry.x.min()
    longitude2 = gdf.geometry.x.max()
    building_list = list(mapping(building)['bbox'])
    building_list.sort()
    latitude1 = gdf.geometry.y.min()
    latitude2 = building_list[0]
    south = gdf.cx[longitude1:longitude2,latitude1:latitude2]
    return south

class TestDirectionSouth(unittest.TestCase):
    def test_direction_south(self):
        
        data = pd.read_csv(r'test_direction.csv')
        data['geometry'] = data['geometry'].apply(wkt.loads)
        data = gpd.GeoDataFrame(data, crs='epsg:4979')
        data = data.drop(['Unnamed: 0'],axis=1)
        data['time'] = pd.to_datetime(data['time'])        
        mymap = gpd.read_file('test.geojson')
        
        data_test = pd.read_csv(r'south.csv')
        data_test['geometry'] = data_test['geometry'].apply(wkt.loads)
        data_test = gpd.GeoDataFrame(data_test, crs='epsg:4979')
        data_test = data_test.drop(['Unnamed: 0'],axis=1)
        data_test['time'] = pd.to_datetime(data_test['time'])
  
        pd.testing.assert_frame_equal(direction_south(data,mymap).reset_index(drop=True), data_test)

    
unittest.main()