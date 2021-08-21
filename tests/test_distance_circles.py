import unittest

import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
from shapely import wkt
import geopandas as gpd
from shapely.geometry import mapping

def distance_circles(gdf,x):

    distance_min = int(gdf['distance'].unique().min())
    distance_max = int(gdf['distance'].unique().max())
    d = [0]*len(gdf.distance.unique())
    for i in range(distance_min,distance_max+1,x):
        d.append(i)
    
    d = list(filter(lambda number : number > 0, d))
    gdf = gdf.loc[gdf['distance'].isin(d),['time','svid','Cn0DbHz','geometry','distance']]
    
    return gdf

class TestDistanceCircles(unittest.TestCase):
    def test_distance_circles(self):
        data = pd.read_csv(r'test_distance_circles.csv')
        #data['geometry'] = data['geometry'].apply(wkt.loads)
        #data = gpd.GeoDataFrame(data, crs='epsg:4979')
        #data = data.drop(['Unnamed: 0'],axis=1)
        #data['time'] = pd.to_datetime(data['time'])        
        
        data_test2 = pd.read_csv(r'circles2.csv')
        data_test2 = data_test2[['time','svid','Cn0DbHz','geometry','distance']]
        
        data_test3 = pd.read_csv(r'circles3.csv')
        data_test3 = data_test3[['time','svid','Cn0DbHz','geometry','distance']]

        
        pd.testing.assert_frame_equal(distance_circles(data,2).reset_index(drop=True), data_test2)
        pd.testing.assert_frame_equal(distance_circles(data,3).reset_index(drop=True), data_test3.reset_index(drop=True))
        

unittest.main()
        
        

