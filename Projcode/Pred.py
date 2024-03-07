import pandas as pd
import numpy as np
from Projcode import stock_utils

def load_data(file_path):
    df = pd.read_csv(file_path)

    # Convert the 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Adding moving averages to the DataFrame with min_periods=1
    df['MA200'] = df['Close'].rolling(window=200, min_periods=1).mean()
    df['MA150'] = df['Close'].rolling(window=150, min_periods=1).mean()
    df['MA50'] = df['Close'].rolling(window=50, min_periods=1).mean()

    # Display the first few rows to ensure it's loaded correctly
    # print(df.head())

    def filterData(df):
        pd.set_option('display.max_rows', None)

        # Get the last date in the dataset
        last_date = df['Date'].max()

        # Calculate the date 3 months prior to the last date
        three_months_ago = last_date - pd.DateOffset(months=150)

        # Filter the DataFrame for the last 3 months
        df_last_3_months = df[df['Date'] > three_months_ago]
        df_last_3_months = df_last_3_months[:-1]

        return df_last_3_months

    # df = filterData(df)

    return df

def ZZ(df):
    # extreme_points = stock_utils.zig_zag(df, percent_threshold=5, move_relative_percent_threshold=0, absolute_threshold=0)
    extreme_points = stock_utils.zig_zag(df, percent_threshold=5, move_relative_percent_threshold=10, absolute_threshold=0)
    return extreme_points

def Breather(extreme_points):
    # uptrend_correction_threshold = 9.99
    # downtrend_correction_threshold = 9.99
    # filtered_extreme_points = stock_utils.BREATHER_FILTER(extreme_points, uptrend_correction_threshold=uptrend_correction_threshold,downtrend_correction_threshold=downtrend_correction_threshold, uptrend_retest_boundary_threshold=0.1, downtrend_retest_boundary_threshold=0.1)
    
    uptrend_correction_threshold = 9.99
    downtrend_correction_threshold = 9.99
    filtered_extreme_points = stock_utils.BREATHER_FILTER(extreme_points, uptrend_correction_threshold=uptrend_correction_threshold,downtrend_correction_threshold=downtrend_correction_threshold, uptrend_retest_boundary_threshold=0.1, downtrend_retest_boundary_threshold=0.1)
    return filtered_extreme_points