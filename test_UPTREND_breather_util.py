import unittest
from Projcode import stock_utils as su
from Projcode import Pred
import pandas as pd

class TestUptrendBreatherIdentification(unittest.TestCase):
    def setUp(self): # picking this portion because it has beautifully constructed uptrend
        self.df = Pred.load_data('content/ITC.NS_historical_data.csv')
        self.df2=self.df.copy()
        start_date = pd.to_datetime('2016-02-05')
        end_date = pd.to_datetime('2017-06-18')
        self.df = self.df[(self.df['Date'] >= start_date) & (self.df['Date'] <= end_date)]
        self.ext_pts = Pred.ZZ(self.df)
        fil_ext_pts = Pred.Breather(self.ext_pts)
        # Pred.stock_utils.plotAfterBreather(self.df, ext_pts, fil_ext_pts)

    def test_high_point_needed(self):
        Extreme_points = [(0, 100, 'LOW'), (1, 110, 'HIGH'), (2, 105, 'LOW')]
        result = su.Uptrend_BREATHER_IDENTIFICATION(0, Extreme_points, 10)
        self.assertEqual(result, ("High Point needed", 0))

    def test_no_previous_point(self):
        Extreme_points = [(0, 100, 'HIGH'), (1, 90, 'LOW'), (2, 95, 'HIGH')]
        result = su.Uptrend_BREATHER_IDENTIFICATION(0, Extreme_points, 10, uptrend_correction_threshold=5, uptrend_retest_boundary_threshold=2)
        self.assertEqual(result, ("No previous point to compute move length", 0))
        

    def test_start_point_end_point(self):
        Extreme_points = [(0, 100, 'HIGH'), (1, 90, 'LOW'), (2, 95, 'HIGH')]
        result = su.Uptrend_BREATHER_IDENTIFICATION(2, Extreme_points, 10)
        self.assertEqual(result, ("Start Point is the End Point", 0))

    # @unittest.skip("Couldnt Find testcase")
    def test_trend_reversed(self):
        extreme_points=Pred.ZZ(self.df2)
        length_of_previous_trend_move = extreme_points[33 - 1][1] - extreme_points[33][1]
        uptrend_correction_threshold = 10  # Example threshold value
        uptrend_retest_boundary_threshold = 0  # Example threshold value
       

        result = su.Uptrend_BREATHER_IDENTIFICATION(33, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, uptrend_correction_threshold= uptrend_correction_threshold, uptrend_retest_boundary_threshold = uptrend_retest_boundary_threshold)
        self.assertEqual(result, ('Trend Reversed', 0))
        

    def test_breather_continued_without_rev_or_cont(self):
        given_date = '2023-07-24'
        df_index = su.get_index(given_date, self.df2)
        extreme_points=Pred.ZZ(self.df2)
        # print(extreme_points)
        start_point = None
        for i, (index, value, point_type) in enumerate(extreme_points):
            if index == df_index:
                start_point = i
                break
        length_of_previous_trend_move = extreme_points[start_point][1] - extreme_points[start_point - 1][1]
        uptrend_correction_threshold = 40  # Example threshold value
        uptrend_retest_boundary_threshold = 0  # Example threshold value

        result = su.Uptrend_BREATHER_IDENTIFICATION(start_point, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move,  uptrend_correction_threshold= uptrend_correction_threshold, uptrend_retest_boundary_threshold = uptrend_retest_boundary_threshold)
        self.assertEqual(result, ("Breather Continued without trend reversal or continuation", 0))

    def test_breather_continued(self):
        extreme_points=Pred.ZZ(self.df2)
        length_of_previous_trend_move = extreme_points[153 - 1][1] - extreme_points[153][1]
        uptrend_correction_threshold = 10  # Example threshold value
        uptrend_retest_boundary_threshold = 0  # Example threshold value
       

        result = su.Uptrend_BREATHER_IDENTIFICATION(153, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, uptrend_correction_threshold= uptrend_correction_threshold, uptrend_retest_boundary_threshold = uptrend_retest_boundary_threshold)
        self.assertEqual(result, ('Trend Continued', 1))

    @unittest.skip("There are no testcase(Atleast I couldnt Find)")
    def test_breather_continued_without_rev_or_cont(self):
        pass

    # def test_breather_continued_without_rev_or_cont(self):
    #     given_date = '2024-01-10'
    #     # df_index = su.get_index(given_date, self.df2)
    #     # print(df_index)
    #     # df_index=6751
    #     extreme_points=Pred.ZZ(self.df2)
    #     # print(extreme_points)
    #     start_point = None

    #     # length_of_previous_trend_move = extreme_points[start_point - 1][1] - extreme_points[start_point][1]
    #     downtrend_correction_threshold = 10  # Example threshold value
    #     downtrend_retest_boundary_threshold = 0  # Example threshold value
    #     k=1
    #     for i, (index, value, point_type) in enumerate(extreme_points):
    #         # if index == df_index:
    #             # start_point = i
    #             # break
    #         if k==1:
    #             k=0
    #             continue
    #         length_of_previous_trend_move = extreme_points[i - 1][1] - extreme_points[i][1]
    #         r=su.Uptrend_BREATHER_IDENTIFICATION(index, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, uptrend_correction_threshold= downtrend_correction_threshold, uptrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
    #         # if r[0]=="Breather Continued without trend reversal or continuation":
    #         #     print(index)
    #         #     break
    #         # if r[0]=="Trend Reversed":
    #         #     print("?",index,"?")
    #         #     break

    #     # result = su.Downtrend_BREATHER_IDENTIFICATION(start_point, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, downtrend_correction_threshold= downtrend_correction_threshold, downtrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
    #     # self.assertEqual(result, ("Breather Continued without trend reversal or continuation", 0))


# Run the tests
if __name__ == '__main__':
    unittest.main()
