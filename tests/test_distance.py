import unittest

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import geopandas as gpd
import math
from math import sin,cos

#The algorithm is only for the data of east longitude and north latitude
def distance(longitudeA,latitudeA,longitudeB,latitudeB):

    #define radius of earth
    R = 6371.004
    MLonA = longitudeA
    MLonB = longitudeB
    #since points are at north latitude
    MLatA = 90 - latitudeA
    MLatB = 90 - latitudeB
    
    C = sin(MLatA)*sin(MLatB)*cos(MLonA-MLonB)+cos(MLatA)*cos(MLatB)
    #here ignore 1000since want to test in kilometers
    distance = round(R*np.arccos(C)*math.pi/180,0)
    
    return distance

class TestDistance(unittest.TestCase):
    def test_distance(self):
        #Approximately 111 kilometers at a longitude
        self.assertEqual(distance(190,35,191,35), 111)
        #Approximately 111 kilometers at a latitude
        self.assertEqual(distance(190,35,190,36), 111)
        
        

unittest.main()
        
        

