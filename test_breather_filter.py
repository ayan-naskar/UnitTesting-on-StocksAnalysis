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
        # print(self.df2.iloc[5129]["Low"]==pts[0][1])
        # print(self.df2.iloc[5129]['Low'],"==",pts[0][1])
        # for x,y,z in pts:
        #     if y!=self.df2.iloc[x]['Low'] and y!=self.df2.iloc[x]['High']:
        #         print(x)
        self.assertEqual(filtered_extreme_points, 
            [(5099, 178.6666717529297, 'LOW'), (5226, 265.8999938964844, 'HIGH'), (5259, 233.5, 'LOW'), (5266, 259.6499938964844, 'HIGH'), (5300, 222.0, 'LOW'), (5330, 292.1499938964844, 'HIGH'), (5343, 257.8500061035156, 'LOW'), (5408, 319.8999938964844, 'HIGH'), (5416, 299.1499938964844, 'LOW')])


    def test_overall_validity_for_very_small_values(self):
        # Causing problems due to precission
        # Can be eleminated by analysing the data and then scaling it

        pts = [(5099, 178.6666717529297, 'LOW'), (5129, 225.5666656494141, 'HIGH'), (5142, 204.0, 'LOW'), (5203, 262.0, 'HIGH'), (5209, 245.8000030517578, 'LOW'), (5226, 265.8999938964844, 'HIGH'), (5259, 233.5, 'LOW'), (5266, 259.6499938964844, 'HIGH'), (5300, 222.0, 'LOW'), (5330, 292.1499938964844, 'HIGH'), (5343, 257.8500061035156, 'LOW'), (5356, 288.8999938964844, 'HIGH'), (5370, 270.8999938964844, 'LOW'), (5382, 292.8999938964844, 'HIGH'), (5390, 271.0, 'LOW'), (5408, 319.8999938964844, 'HIGH'), (5416, 299.1499938964844, 'LOW')]
        # print(len(pts), len(set(i[1]*10//1 for i in pts)))
        def changeIt(pts):
            for i in range(len(pts)):
                pts[i]=(pts[i][0],(pts[i][1]*10//1)/100000000+0.2389, pts[i][2])
                # print(pts[i][1])
            return pts

        pts=changeIt(pts)
        expected_pts=[(5099, 178.6666717529297, 'LOW'), (5226, 265.8999938964844, 'HIGH'), (5259, 233.5, 'LOW'), (5266, 259.6499938964844, 'HIGH'), (5300, 222.0, 'LOW'), (5330, 292.1499938964844, 'HIGH'), (5343, 257.8500061035156, 'LOW'), (5408, 319.8999938964844, 'HIGH'), (5416, 299.1499938964844, 'LOW')]
        expected_pts=changeIt(expected_pts)
        
        # print(sorted(list(set(i[1]//1 for i in pts))))
        # print(sorted([i[1]//1 for i in pts]))


        filtered_extreme_points = su.BREATHER_FILTER(pts, 9.99, 9.99, 0.1, 0.1)
        # print(self.df2.iloc[5129]["Low"]==pts[0][1])
        # print(self.df2.iloc[5129]['Low'],"==",pts[0][1])
        # for x,y,z in pts:
        #     if y!=self.df2.iloc[x]['Low'] and y!=self.df2.iloc[x]['High']:
        #         print(x)
        self.assertEqual(filtered_extreme_points, expected_pts)


if __name__ == '__main__':
    unittest.main()
