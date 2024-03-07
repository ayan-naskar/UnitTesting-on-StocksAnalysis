import unittest
import pandas as pd
from Projcode import stock_utils as su
from Projcode import Pred

class TestNextExtremeCandle(unittest.TestCase):
    def setUp(self):
        # Define a test DataFrame with stock data
        # data = {
        #     'Date': pd.date_range(start='2022-01-01', periods=10, freq='D'),
        #     'Open': [100, 105, 110, 108, 112, 115, 114, 118, 120, 122],
        #     'High': [110, 115, 120, 118, 122, 125, 124, 128, 130, 132],
        #     'Low': [98, 103, 108, 106, 110, 113, 112, 116, 118, 120],
        #     'Close': [105, 110, 115, 113, 118, 120, 119, 123, 125, 128],
        #     'Adj Close': [102, 108, 113, 110, 115, 118, 117, 121, 123, 126],
        #     'Volume': [100000, 120000, 150000, 130000, 140000, 160000, 155000, 170000, 180000, 190000]
        # }
        # self.df = pd.DataFrame(data)
        self.df = Pred.load_data('content/ITC.NS_historical_data.csv')
        last_date = self.df['Date'].max()
        three_months_ago = last_date - pd.DateOffset(months=1)
        self.df = self.df[self.df['Date'] > three_months_ago]
    
    def test_next_extreme_is_last_data(self):
        start_index = su.get_index('2024-02-05', self.df)
        threshold = 2
        result = su.next_extreme_candle(self.df, start_index, percent_threshold=threshold)
        self.assertEqual(result, (7059, 429.5, 'LOW'))

    def test_next_extreme_candle_high_threshold(self):
        # Test with a high threshold where extreme point is not reached
        start_index = su.get_index('2024-01-30', self.df)
        threshold = 10
        result = su.next_extreme_candle(self.df, start_index, percent_threshold=threshold)
        self.assertEqual(result, (7059, 429.5, 'LOW'))

    def test_next_extreme_candle_low_threshold(self):
        # Test with a low threshold where extreme point is not reached
        start_index = su.get_index('2024-01-19', self.df)
        threshold = 0.0001
        result = su.next_extreme_candle(self.df, start_index, percent_threshold=threshold)
        self.assertEqual(result, (7050, 473.75, 'HIGH'))

    def test_next_extreme_candle_absolute_threshold(self):
        # Test with an absolute threshold where extreme point is reached
        start_index = su.get_index('2024-01-18', self.df)
        threshold = 10
        absolute_threshold = 20
        result = su.next_extreme_candle(self.df, start_index, percent_threshold=threshold, absolute_threshold=absolute_threshold)
        self.assertEqual(result, (7059, 429.5, 'LOW'))

    @unittest.skip("")
    def test_next_extreme_candle_negative_move_threshold(self):
        # Test with a negative move relative threshold
        start_index = su.get_index('2024-01-18', self.df)
        threshold = 5
        move_relative_threshold = -2
        result = su.next_extreme_candle(self.df, start_index, percent_threshold=threshold, move_relative_percent_threshold=move_relative_threshold)
        self.assertEqual(result, None)

    def test_next_extreme_candle_end_of_dataframe(self):
        # Test when the end of DataFrame is reached
        start_index = su.get_index('2024-02-08', self.df)
        result = su.next_extreme_candle(self.df, start_index)
        self.assertEqual(result, (7061, 429.1000061035156, 'HIGH'))

    @unittest.skip("")
    def test_next_extreme_candle_invalid_start_index(self):
        # Test with an invalid start index
        start_index = -1
        with self.assertRaises(IndexError):
            su.next_extreme_candle(self.df, start_index)

if __name__ == '__main__':
    unittest.main()
