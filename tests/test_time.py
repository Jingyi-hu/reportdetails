import unittest

import warnings
warnings.filterwarnings("ignore")
import copy
import pandas as pd
import numpy as np
from shapely import wkt
import geopandas as gpd
from shapely.geometry import mapping

def time_interval(gdf,x):

    gdf = gdf.sort_values(by = 'time')
    gdf['minute'] = gdf.apply(lambda x: (60*x['time'].hour+x['time'].minute), axis=1)

    gdf['minite_diff'] = gdf['minute']- gdf.iloc[0]['minute']
    
    time_min = int(gdf['minite_diff'].unique().min())
    time_max = int(gdf['minite_diff'].unique().max())
    t = [0]*len(gdf.minite_diff.unique())
    for i in range(time_min,time_max+1,x):
        t.append(i)
    t = list(filter(lambda number : number > 0, t))
    t.append(0)
    
    gdf = gdf.loc[gdf['minite_diff'].isin(t),['time','svid','Cn0DbHz','geometry','minute','minite_diff']]
    
    return gdf

class TestTime(unittest.TestCase):
    def test_time_interval(self):
        data = pd.read_csv(r'test_time.csv')
        data['geometry'] = data['geometry'].apply(wkt.loads)
        data = gpd.GeoDataFrame(data, crs='epsg:4979')
        data['time'] = pd.to_datetime(data['time'])
        data = data[['time','svid','Cn0DbHz','geometry']]
        
        data_test3 = pd.read_csv(r'time_interval3.csv')
        data_test3['geometry'] = data_test3['geometry'].apply(wkt.loads)
        data_test3 = gpd.GeoDataFrame(data_test3, crs='epsg:4979')
        data_test3['time'] = pd.to_datetime(data_test3['time'])
        
        data_test2 = pd.read_csv(r'time_interval2.csv')
        data_test2['geometry'] = data_test2['geometry'].apply(wkt.loads)
        data_test2 = gpd.GeoDataFrame(data_test2, crs='epsg:4979')
        data_test2['time'] = pd.to_datetime(data_test2['time'])
                
                
        
        pd.testing.assert_frame_equal(time_interval(data,3)[['time','svid','Cn0DbHz','geometry']].reset_index(drop=True).sort_values(by = ['time']), data_test3[['time','svid','Cn0DbHz','geometry']].sort_values(by = ['time']))
        
        pd.testing.assert_frame_equal(time_interval(data,2)[['time','svid','Cn0DbHz','geometry']].reset_index(drop=True).sort_values(by = ['time']), data_test2[['time','svid','Cn0DbHz','geometry']].sort_values(by = ['time']))
        
        pd.testing.assert_frame_equal(time_interval(data,1)[['time','svid','Cn0DbHz','geometry']].reset_index(drop=True).sort_values(by = ['time']), data)
        
        
unittest.main()
        
        

