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

    def test_downtrend_reversed(self):
        extreme_points=Pred.ZZ(self.df2)
        length_of_previous_trend_move = extreme_points[60 - 1][1] - extreme_points[60][1]
        downtrend_correction_threshold = 10  # Example threshold value
        downtrend_retest_boundary_threshold = 0  # Example threshold value
       

        result = su.Downtrend_BREATHER_IDENTIFICATION(60, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, downtrend_correction_threshold= downtrend_correction_threshold, downtrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
        self.assertEqual(result, ('Trend Reversed', 0))

    def test_downtrend_continued(self):
        extreme_points=Pred.ZZ(self.df2)
        length_of_previous_trend_move = extreme_points[98 - 1][1] - extreme_points[98][1]
        downtrend_correction_threshold = 10  # Example threshold value
        downtrend_retest_boundary_threshold = 0  # Example threshold value
       

        result = su.Downtrend_BREATHER_IDENTIFICATION(98, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, downtrend_correction_threshold= downtrend_correction_threshold, downtrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
        self.assertEqual(result, ('Trend Continued', 1))

    def test_downtrend_no_previous_point(self):
        # Test when there is no previous point to compute move length
        start_point = 0
        extreme_points = [
            (0, 100, "MAX"),
            (1, 90, "MIN"),
            (2, 80, "MAX"),
            (3, 75, "MIN"),
            (4, 70, "MAX"),
            (5, 65, "MIN")
        ]
        length_of_previous_trend_move = 20
        downtrend_correction_threshold = 5
        downtrend_retest_boundary_threshold = 2

        result = su.Downtrend_BREATHER_IDENTIFICATION(
            start_point,
            extreme_points,
            length_of_previous_trend_move,
            downtrend_correction_threshold,
            downtrend_retest_boundary_threshold
        )
        self.assertEqual(result, ("No previous point to compute move length", 0))

    def test_start_point_is_end_point(self):
        # Test when there is no previous point to compute move length
        start_point = 5
        extreme_points = [
            (0, 100, "MAX"),
            (1, 90, "MIN"),
            (2, 80, "MAX"),
            (3, 75, "MIN"),
            (4, 70, "MAX"),
            (5, 65, "MIN")
        ]
        length_of_previous_trend_move = 20
        downtrend_correction_threshold = 5
        downtrend_retest_boundary_threshold = 2

        result = su.Downtrend_BREATHER_IDENTIFICATION(
            start_point,
            extreme_points,
            length_of_previous_trend_move,
            downtrend_correction_threshold,
            downtrend_retest_boundary_threshold
        )
        self.assertEqual(result, ("Start Point is the End Point", 0))

    def test_downtrend_low_point_needed(self):
        # Test when the starting point is not a LOW
        start_point = 2  # Index of the first MAX point
        extreme_points = [
            (0, 100, "MAX"),
            (1, 90, "MIN"),
            (2, 80, "MAX"),
            (3, 75, "MIN"),
            (4, 70, "MAX"),
            (5, 65, "MIN")
        ]
        length_of_previous_trend_move = 20
        downtrend_correction_threshold = 5
        downtrend_retest_boundary_threshold = 2

        result = su.Downtrend_BREATHER_IDENTIFICATION(
            start_point,
            extreme_points,
            length_of_previous_trend_move,
            downtrend_correction_threshold,
            downtrend_retest_boundary_threshold
        )
        self.assertEqual(result, ("LOW Point needed", 0))

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
    #         r=su.Downtrend_BREATHER_IDENTIFICATION(index, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, downtrend_correction_threshold= downtrend_correction_threshold, downtrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
    #         if r[0]=="Breather Continued without trend reversal or continuation":
    #             print(index)
    #             break
    #         if r[0]=="Trend Continued":
    #             print(index)
    #             break

    #     # result = su.Downtrend_BREATHER_IDENTIFICATION(start_point, extreme_points, length_of_previous_trend_move=length_of_previous_trend_move, downtrend_correction_threshold= downtrend_correction_threshold, downtrend_retest_boundary_threshold = downtrend_retest_boundary_threshold)
    #     # self.assertEqual(result, ("Breather Continued without trend reversal or continuation", 0))


# Run the tests
if __name__ == '__main__':
    unittest.main()
