import unittest

import math

def rmse(x):
    a = sum(((x[j] -405) **2) for j in range(len(x)))
    b = a/len(x)
    c = math.sqrt(b)
    
    return c

class TestRMSE(unittest.TestCase):
    def test_rmse(self): 
        numbers = [400,410,420,430,440,450]
        self.assertAlmostEqual(int(rmse(numbers)), 26)
        self.assertEqual(round(rmse(numbers),7), 26.2995564)
    
unittest.main()