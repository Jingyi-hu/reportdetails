import unittest

import copy
import pandas as pd
import numpy as np


def random_row(gdf,x,y):

    df = pd.DataFrame()
    sample = gdf.sample(n = x,random_state = y,axis=0)
    df = df.append(sample)
    return df

class TestRandomRow(unittest.TestCase):
    def test_random_row(self):
        data = {
    'person':['a','b','c','d','e','f','g','h','i','j'],
    'age':[24,23,30,4,21,53,20,45,48,60]}
        df = pd.DataFrame(data)
        
        data_test = pd.DataFrame({
    'person':['e','a','h'],
    'age':[21,24,45]})
  
        pd.testing.assert_frame_equal(random_row(df,3,123).reset_index(drop=True), data_test)
        self.assertEqual(len(random_row(df,3,123)), 3)
    

unittest.main()

