import unittest
from Projcode import stock_utils as su
from Projcode import Pred
import pandas as pd

class TestBreatherFilter(unittest.TestCase):
    def setUp(self): # picking this portion because it has beautifully constructed uptrend
        self.df = Pred.load_data('content/ITC.NS_historical_data.csv')
        self.df2=self.df.copy()
        start_date = pd.to_datetime('2016-02-05')
        end_date = pd.to_datetime('2017-06-18')
        self.df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
        self.ext_pts = Pred.ZZ(self.df)
        fil_ext_pts = Pred.Breather(self.ext_pts)
        # Pred.stock_utils.plotAfterBreather(self.df, ext_pts, fil_ext_pts)

    def test_empty_extreme_points(self):
        # Test when Extreme_points list is empty
        Extreme_points = []
        filtered_extreme_points = su.BREATHER_FILTER(
            Extreme_points,5,5,2,2
        )
        self.assertEqual(filtered_extreme_points, [])
    
    def test_overall_validity(self):
        pts = [(5099, 178.6666717529297, 'LOW'), (5129, 225.5666656494141, 'HIGH'), (5142, 204.0, 'LOW'), (5203, 262.0, 'HIGH'), (5209, 245.8000030517578, 'LOW'), (5226, 265.8999938964844, 'HIGH'), (5259, 233.5, 'LOW'), (5266, 259.6499938964844, 'HIGH'), (5300, 222.0, 'LOW'), (5330, 292.1499938964844, 'HIGH'), (5343, 257.8500061035156, 'LOW'), (5356, 288.8999938964844, 'HIGH'), (5370, 270.8999938964844, 'LOW'), (5382, 292.8999938964844, 'HIGH'), (5390, 271.0, 'LOW'), (5408, 319.8999938964844, 'HIGH'), (5416, 299.1499938964844, 'LOW')]

        filtered_extreme_points = su.BREATHER_FILTER(pts, 9.99, 9.99, 0.1, 0.1)

        self.assertEqual(filtered_extreme_points, 
            [(5099, 178.6666717529297, 'LOW'), (5226, 265.8999938964844, 'HIGH'), (5259, 233.5, 'LOW'), (5266, 259.6499938964844, 'HIGH'), (5300, 222.0, 'LOW'), (5330, 292.1499938964844, 'HIGH'), (5343, 257.8500061035156, 'LOW'), (5408, 319.8999938964844, 'HIGH'), (5416, 299.1499938964844, 'LOW')])

if __name__ == '__main__':
    unittest.main()
