import unittest

import pandas as pd


def random_frac(gdf,x):
    
    df = pd.DataFrame()
    sample = gdf.sample(frac=(x+1)/10,axis=0)
    df = df.append(sample)
    return df

class TestRandomFrac(unittest.TestCase):
    def test_random_frac(self):
        data = {
    'person':['a','b','c','d','e','f','g','h','i','j'],
    'age':[24,23,30,4,21,53,20,45,48,60]}
        df = pd.DataFrame(data)
        
        self.assertEqual(len(random_frac(df,3)), 4)
    

unittest.main()
