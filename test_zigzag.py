import pandas as pd
import unittest
from Projcode import stock_utils as su
from Projcode import Pred

# Define the test case class
class TestZigZagFunction(unittest.TestCase):
    # Setup test data
    def setUp(self):
        self.df = pd.DataFrame({
            'Date': pd.date_range(start='2022-01-01', periods=10, freq='D'),
            'Open': [100, 105, 110, 108, 112, 115, 114, 118, 120, 122],
            'High': [110, 115, 120, 118, 122, 125, 124, 128, 130, 132],
            'Low': [98, 103, 108, 106, 110, 113, 112, 116, 118, 120],
            'Close': [105, 110, 115, 113, 118, 120, 119, 123, 125, 128],
            'Adj Close': [105, 110, 115, 113, 118, 120, 119, 123, 125, 128],
            'Volume': [1000, 1100, 1200, 1150, 1250, 1300, 1200, 1350, 1400, 1500]
        })
        # su.plotAfterBreather(self.df, su.zig_zag(self.df), su.zig_zag(self.df))


    def test_zig_zag(self):
        result = su.zig_zag(self.df)
        expected_result = [(2, 120, 'HIGH'),
                            (3, 106, 'LOW'),
                            (5, 125, 'HIGH'),
                            (6, 112, 'LOW'),
                            (9, 132, 'HIGH')]
        self.assertEqual(result, expected_result)
    
    def test_zig_zag_to_test_another_pattern(self):
        df2 = pd.DataFrame({
            'Date': pd.date_range(start='2022-01-01', periods=10, freq='D'),
            'Open': [100, 105, 110, 108, 112, 115, 114, 118, 120, 122],
            'High': [110, 115, 120, 118, 122, 125, 124, 128, 130, 132],
            'Low': [98, 103, 108, 106, 110, 113, 112, 116, 118, 120],
            'Close': [105, 110, 115, 113, 118, 120, 119, 123, 125, 128],
            'Adj Close': [105, 110, 115, 113, 118, 120, 119, 123, 125, 128],
            'Volume': [1000, 1100, 1200, 1150, 1250, 1300, 1200, 1350, 1400, 1500]
        })
        df2.drop(df2.index[:2], inplace=True)
        result = su.zig_zag(df2, 0, 0, 2)
        # su.plotAfterBreather(df2, result, result)

        expected_result = [(3, 106, 'LOW'), (9, 132, 'HIGH')]
        self.assertEqual(result, expected_result)

    def test_zig_zag_with_percent_threshold(self):
        result = su.zig_zag(self.df, 1)
        expected_result = [(2, 120, 'HIGH'), (3, 106, 'LOW'), (9, 132, 'HIGH')]
        self.assertEqual(result, expected_result)

    def test_zig_zag_with_random_thresholds(self):
        result = su.zig_zag(self.df, 1, 0.5, 3)
        expected_result = [(9, 132, 'HIGH')]
        self.assertEqual(result, expected_result)
    
    # Test for empty DataFrame
    @unittest.skip("")
    def test_empty_dataframe(self):
        empty_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
        result = su.zig_zag(empty_df)
        self.assertEqual(result, [])

    # Test for DataFrame with single row
    def test_single_row_dataframe(self):
        single_row_df = pd.DataFrame({
            'Date': [pd.Timestamp('2022-01-01')],
            'Open': [100],
            'High': [110],
            'Low': [98],
            'Close': [105],
            'Adj Close': [105],
            'Volume': [1000]
        })
        result = su.zig_zag(single_row_df)
        self.assertEqual(result, [])

    # Test for DataFrame with all same values
    def test_all_same_values_dataframe(self):
        all_same_df = pd.DataFrame({
            'Date': pd.date_range(start='2022-01-01', periods=10, freq='D'),
            'Open': [100] * 10,
            'High': [110] * 10,
            'Low': [90] * 10,
            'Close': [105] * 10,
            'Adj Close': [105] * 10,
            'Volume': [1000] * 10
        })
        result = su.zig_zag(all_same_df)
        self.assertEqual(result, [])

    # Test for DataFrame with alternating values
    def test_alternating_values_dataframe(self):
        result = su.zig_zag(self.df)
        expected_result = [(2, 120, 'HIGH'),
                            (3, 106, 'LOW'),
                            (5, 125, 'HIGH'),
                            (6, 112, 'LOW'),
                            (9, 132, 'HIGH')]
        self.assertEqual(result, expected_result)

# Run the tests
if __name__ == '__main__':
    unittest.main()
