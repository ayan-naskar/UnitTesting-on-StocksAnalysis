import unittest
import numpy as np
import pandas as pd
from Projcode import Pred
from tqdm import tqdm
from Projcode import stock_utils as su

class Test_utils(unittest.TestCase):
    def setUp(self):
        self.csv_files = ['content/ITC.NS_historical_data.csv']
        # self.csv_files = ['content/SyntheticTC/1.csv','content/SyntheticTC/2.csv','content/SyntheticTC/3.csv','content/SyntheticTC/4.csv']
    
    # def test_Predcode(self):
    #     # Iterate over each CSV file
    #     for file_path in tqdm(self.csv_files):
    #         df = Pred.load_data(file_path)
            
    #         ext_pts = Pred.ZZ(df)
    #         fil_ext_pts = Pred.Breather(ext_pts)
    #         # Pred.stock_utils.plotAfterBreather(df, ext_pts, fil_ext_pts)
    #         # self.assertTrue(np.allclose(np.mean(y_pred), np.mean(y), atol=1))
    
    def test_candle_diff(self):
        # Assuming that candle_diff calculates number of candles by (start, end]
        # Since, the original function calculates differences by (end-start) and not (end-start+1)
        date = [
            {
                "start": "2022-01-03",
                "end": "2022-01-06",
                "expected": 3
            },
            {
                "start": "2022-01-06",
                "end": "2022-01-03",
                "expected": 3
            },
            # {
            #     "start": "2022-01-06",
            #     "end": "2022-01-08",
            #     "expected": 1
            # },
            # {
            #     "start": "2022-01-08",
            #     "end": "2022-01-06",
            #     "expected": 1
            # },
            # {
            #     "start": "2022-01-07",
            #     "end": "2022-01-10",
            #     "expected": 1
            # },
            # {
            #     "start": "2022-01-10",
            #     "end": "2022-01-07",
            #     "expected": 1
            # },
            # {
            #     "start": "2022-01-07",
            #     "end": "2022-01-09",
            #     "expected": 0
            # },
            # {
            #     "start": "2022-01-09",
            #     "end": "2022-01-07",
            #     "expected": 0
            # },
            # {
            #     "start": "2022-01-02",
            #     "end": "2022-01-04",
            #     "expected": 2
            # },
            # {
            #     "start": "2022-01-04",
            #     "end": "2022-01-02",
            #     "expected": 2
            # }
        ]
        df = Pred.load_data(self.csv_files[0])
        for entry in date:
            out = su.candle_diff(entry["start"], entry["end"], df)
            self.assertEqual(out, entry["expected"])
    
    def test_get_index(self):
        date = [
            {"date": "2022-01-03", "expected": 6541},
            # {"date": "fkuybkl", "expected": None}
        ]
        df = Pred.load_data(self.csv_files[0])
        for d in date:
            out = su.get_index(d["date"], df)
            self.assertEqual(out, d["expected"])
    
    def test_engulfed_candle_count(self):
        df = Pred.load_data(self.csv_files[0])
        print(df.index.min())
        inp =  [
            {
                "candle_index": su.get_index('2024-01-30',df),
                "df": df,
                "expected": 3
            },
            {
                "candle_index": 7019,
                "df": df,
                "expected": 4
            },
            {
                "candle_index": 0,
                "df": df,
                "expected": 0
            },
            {
                "candle_index": 3000000,
                "df": df,
                "expected": 0
            },
            # {
            #     "candle_index": -100,
            #     "df": df,
            #     "expected": 0
            # },
            # {
            #     "candle_index": -1,
            #     "df": df,
            #     "expected": 0
            # },
            # {
            #     "candle_index": 5,
            #     "df": None,
            #     "expected": 0
            # }
        ]
        for inpt in inp:
            out = su.engulfed_candle_count(inpt["candle_index"], inpt["df"])
            self.assertEqual(out, inpt["expected"])
    
    def test_no_extreme_high(self):
        # Failing dataframe
        data = {
            'Date': ['2023-11-20', '2023-11-21', '2023-11-22', '2023-11-23', '2023-11-24', '2023-11-25'],
            'Open': [98, 100, 99, 98.5, 101, 102.5],
            'High': [102, 103, 101, 100.5, 105, 104],
            'Low': [95, 98, 97, 96.5, 99, 101],
            'Close': [100, 101, 99, 98, 103, 102],
            'Adj Close': [100, 101, 99, 98, 103, 102],
            'Volume': [10000, 12000, 8000, 9000, 15000, 11000]
        }
        df = pd.DataFrame(data)

        # Set start and pivot high indices
        start_candle_index = df.index[0]
        pivot_high_candle_index = df.index[0]  # Initial high point

        # Test case with high thresholds (no new extreme high)
        percent_threshold = 10
        move_relative_percent_threshold = 5
        absolute_threshold = 1

        result = su.next_extreme_high_point(df, start_candle_index, pivot_high_candle_index, percent_threshold, move_relative_percent_threshold, absolute_threshold)

        # Expected output (may vary depending on specific implementation)
        expected_result = (4, 105.0, 'HIGH')

        self.assertEqual(result, expected_result)

    def test_extreme_close_thresholds(self):
        data = {
            'Date': pd.date_range(start='2024-01-01', periods=10),
            'Open': [11, 11.5, 14.2, 13, 14.5, 17, 18, 18.5, 21, 20.5],
            'High': [10, 12, 15, 14, 16, 18, 20, 19, 22, 21],
            'Low': [9, 11, 13.8, 12, 14, 16.5, 17.5, 17.8, 20, 20],
            'Close': [9.5, 12, 14.5, 13.5, 15.5, 17.8, 19, 18.7, 21.5, 20.8],
            'Adj Close': [9.2, 11.8, 14.2, 13.3, 15.2, 17.5, 19.1, 18.8, 21.3, 20.5],
            'Volume': [10000, 12000, 15000, 14000, 16000, 18000, 20000, 19000, 22000, 21000]
        }
        df = pd.DataFrame(data)

        percent_threshold = 0.5
        move_relative_percent_threshold = 0.4
        absolute_threshold = 0.6

        # Call the function with the test case
        result = su.next_extreme_high_point(df, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold, absolute_threshold=absolute_threshold)

        # Assert the result
        self.assertEqual(result, (2, 15, 'HIGH'))

    def test_next_extreme_low_point(self):
        data = {
            'Date': pd.date_range(start='2024-01-01', periods=10),
            'Open': [9, 10, 13, 12, 14, 15, 16, 17, 19, 18],
            'High': [10, 12, 15, 14, 16, 18, 20, 19, 22, 21],
            'Low': [100, 90, 85, 82, 80, 78, 77, 75, 70, 68],
            'Close': [9.5, 10.5, 14, 13, 15, 17, 18, 18, 20, 19],
            'Adj Close': [9.2, 10.2, 13.8, 12.8, 14.5, 16.5, 17.8, 17.8, 19.8, 18.5],
            'Volume': [10000, 12000, 15000, 14000, 16000, 18000, 20000, 19000, 22000, 21000]
        }
        df = pd.DataFrame(data)
        
        result = su.next_extreme_low_point(df, percent_threshold=0.1, move_relative_percent_threshold=0.1, absolute_threshold=2)
        # In this case, the function should still return the same result as in the other test cases,
        # because the thresholds are close but not exactly equal
        self.assertEqual(result, (9, 68, 'LOW'))

if __name__ == '__main__':
    unittest.main()