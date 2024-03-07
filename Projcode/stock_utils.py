import pandas as pd
import plotly.graph_objects as go
import plotly.graph_objects as go

def plotafterzigzag(df_last_3_months, extreme_points, extreme_points2):
    # Assuming df_last_3_months is your DataFrame with the last 3 months of OHLC data
    # Assuming extreme_points is the output from zig_zag(df_last_3_months), now including extreme values

    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df_last_3_months['Date'],
                                        open=df_last_3_months['Open'],
                                        high=df_last_3_months['High'],
                                        low=df_last_3_months['Low'],
                                        close=df_last_3_months['Close'],
                                        name='Candlestick')])

    # # Loop through the extreme_points to plot the high and low points using their exact values
    # for index, extreme_value, extreme_type in extreme_points:
    #     fig.add_trace(go.Scatter(x=[df_last_3_months.loc[index, 'Date']],
    #                              y=[extreme_value],
    #                              mode='markers',
    #                              marker=dict(color='Green' if extreme_type == "LOW" else 'Red', size=8),
    #                              name=f"{extreme_type} point"))

    # # Loop through the extreme_points2 to plot the high and low points using their exact values
    # for index, extreme_value, extreme_type in extreme_points2:
    #     fig.add_trace(go.Scatter(x=[df_last_3_months.loc[index, 'Date']],
    #                              y=[extreme_value],
    #                              mode='markers',
    #                              marker=dict(color='Green' if extreme_type == "LOW" else 'Red', size=8),
    #                              name=f"{extreme_type} point"))

    # For the trendline, use the dates and extreme values directly from the extreme_points
    pivot_dates = [df_last_3_months.loc[index, 'Date'] for index, _, _ in extreme_points]
    pivot_values = [extreme_value for _, extreme_value, _ in extreme_points]

    # For the trendline, use the dates and extreme values directly from the extreme_points
    pivot_dates2 = [df_last_3_months.loc[index, 'Date'] for index, _, _ in extreme_points2]
    pivot_values2 = [extreme_value for _, extreme_value, _ in extreme_points2]

    # Add a line connecting the pivot points to represent the zigzag trend
    fig.add_trace(go.Scatter(x=pivot_dates,
                            y=pivot_values,
                            mode='lines',  # This will connect the points with lines
                            line=dict(color='Yellow', width=2),
                            name='Zigzag Trend'))

    # Add a line connecting the pivot points to represent the zigzag trend
    fig.add_trace(go.Scatter(x=pivot_dates2,
                            y=pivot_values2,
                            mode='lines',  # This will connect the points with lines
                            line=dict(color='Red', width=2),
                            name='Zigzag Trend'))

    # Customize the layout
    fig.update_layout(title='Stock Price Data with Zigzag Trendlines',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()

def candle_diff(date1, date2, df):
    """
    Calculates the number of candles (rows) between two given candle dates in a DataFrame.

    Parameters:
    - date1: The date of the first candle (string or datetime).
    - date2: The date of the second candle (string or datetime).
    - df: DataFrame containing the OHLC data with a 'Date' column.

    Returns:
    - The number of candles between the two given dates, excluding non-trading days.
    """
    # Convert date1 and date2 to datetime if they are not already
    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)

    # Ensure date1 is before date2
    if date1 > date2:
        date1, date2 = date2, date1  # Swap the dates if date1 is later than date2

    # Find the indices for the given dates
    index1 = df.index[df['Date'] == date1].tolist()
    index2 = df.index[df['Date'] == date2].tolist()

    # Check if both dates exist in the DataFrame
    if not index1 or not index2:
        return None  # One or both of the dates do not exist in the DataFrame

    # Calculate the difference in indices to find the number of candles between the dates
    candle_count = index2[0] - index1[0]

    return candle_count

def get_index(candle_date, df):
    """
    Find the index of the candle with a given date in the DataFrame. Stops processing if the date is not found.

    Parameters:
    - df: DataFrame containing the OHLC data with a 'Date' column.
    - candle_date: The date of the candle to find, as a string in the same format as the DataFrame's 'Date' column.

    Returns:
    - The index of the candle with the given date. Halts execution with an assertion error if the date is not found.
    """
    # Convert the 'Date' column to datetime if it's not already
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert the input date to datetime
    candle_date = pd.to_datetime(candle_date)

    # Find the index of the row that matches the given date
    match = df.index[df['Date'] == candle_date].tolist()

    # Assert that the match list is not empty; if it is, halt execution
    assert match, "Date not found in given OHLC DataFrame. Processing halted."

    # Return the index if found
    return match[0]

def get_candle_date(df, index):
    """
    Retrieves the date of the candle for a given index from the DataFrame.

    Parameters:
    - df: DataFrame containing the OHLC data with a 'Date' column.
    - index: The index of the candle whose date you want to retrieve.

    Returns:
    - The date of the candle at the given index, or None if the index is not found.
    """
    try:
        # Access the 'Date' column of the DataFrame at the given index
        candle_date = df.loc[index, 'Date']
        return candle_date
    except KeyError:
        # Return None if the index is not found
        return None

def engulfed_candle_count(candle_index, df):
    """
    Count how many subsequent candles are engulfed by the candle at a given index.

    Parameters:
    - candle_index: The index of the candle to start the check from.
    - df: DataFrame containing the OHLC data.

    Returns:
    - The number of subsequent candles engulfed by the candle at the given index.
    """
    # Initialize the count of engulfed candles
    engulfed_candle_count = 0

    # Find the maximum index in the DataFrame
    max_index = df.index.max()

    # Start a loop to check each subsequent candle
    while True:
        # print(candle_index, engulfed_candle_count, type(candle_index))
        # Ensure we do not exceed the maximum index of the DataFrame
        if candle_index + engulfed_candle_count + 1 > max_index:
            break

        # Get the current and next candle data
        current_candle = df.loc[candle_index]
        next_candle_index = df.index[df.index > candle_index][engulfed_candle_count]  # Get the next available index
        if next_candle_index > max_index:
            break  # Break if the next index is beyond the DataFrame's range

        next_candle = df.loc[next_candle_index]

        # Check if the current candle engulfs the next candle
        if current_candle['High'] >= next_candle['High'] and current_candle['Low'] <= next_candle['Low']:
            # Increase the count as the next candle is engulfed
            engulfed_candle_count += 1
        else:
            # If the next candle is not engulfed, break the loop
            break

    # Return the count of engulfed candles
    return engulfed_candle_count

def candle_from_date(candle_date, df):
    """
    Utility function to get the candle data for a specific date from the DataFrame.

    Parameters:
    - candle_date: The date of the candle to retrieve.
    - df: DataFrame containing OHLC data with a 'Date' column.

    Returns:
    - The row from the DataFrame corresponding to the candle_date.
    """
    return df.loc[df['Date'] == pd.to_datetime(candle_date)].iloc[0]

def candle_from_extreme_point(extreme_point, df):
    """
    Retrieves a candle from the DataFrame based on the date in an extreme point dictionary.

    Parameters:
    - extreme_point: Dictionary with 'mark type', 'date', and 'value' keys.
    - df: DataFrame containing OHLC data with a 'Date' column.

    Returns:
    - The candle data corresponding to the date in the extreme_point dictionary.
    """
    # If extreme_point is None then candle would also be none
    if extreme_point is None:
        return None

    # Extract the date from the extreme_point dictionary
    extreme_point_date = pd.to_datetime(extreme_point['date']).date()

    # Use the candle_from_date utility function to get the candle data
    return candle_from_date(extreme_point_date, df)


# zigzag portion --------------------------------------------------------

def next_extreme_high_point(df, start_candle_index=None, input_candle_index=None, percent_threshold=0, move_relative_percent_threshold=0, absolute_threshold=0, pivot_high_candle_index=-1):
    """
    Finds the next extreme high point in stock data, filtering out minor movements below a specified threshold.
    Enhanced with logging for debugging purposes.
    """
    # Initialization with logging
    if start_candle_index is None:
        start_candle_index = df.index.min()
    if input_candle_index is None:
        input_candle_index = start_candle_index
    if pivot_high_candle_index == -1:
        pivot_high_candle_index = input_candle_index

    # # print(f"Starting search from index: {start_candle_index}, Input candle index: {input_candle_index}, Pivot high index: {pivot_high_candle_index}")

    pivot_high = df.loc[pivot_high_candle_index, 'High']
    # # print(f"Initial pivot high: {pivot_high} at index {pivot_high_candle_index}")

    # print("here")
    engulfed_count = engulfed_candle_count(input_candle_index, df)
    next_candle_index = input_candle_index + engulfed_count + 1

    if next_candle_index > df.index.max():
        # print("Reached the end of the DataFrame. No more candles to evaluate.")
        return (pivot_high_candle_index, pivot_high, "HIGH")

    next_candle = df.loc[next_candle_index]
    # # print(f"Evaluating next candle at index {next_candle_index} with High: {next_candle['High']}")

    if next_candle['High'] > pivot_high:
        pivot_high = next_candle['High']
        pivot_high_candle_index = next_candle_index
        # print(f"New pivot high found: {pivot_high} at index {pivot_high_candle_index}")
    else:
        move_in_high = pivot_high - next_candle['High']
        percent_high_move_threshold = pivot_high * (percent_threshold / 100)
        last_move = pivot_high - df.loc[start_candle_index, 'High']
        last_move_based_threshold = last_move * move_relative_percent_threshold /100
        high_move_abs_threshold = max(absolute_threshold, percent_high_move_threshold, last_move_based_threshold)
        # # print(f"Move in high: {move_in_high}, Last Move = {last_move}, Last Move based Threshold:{last_move_based_threshold}, Percent high move threshold: {percent_high_move_threshold}, Absolute threshold: {absolute_threshold}")

        if move_in_high >= high_move_abs_threshold:
            # print(f"Threshold met. Returning pivot high index: {pivot_high_candle_index}")
            return (pivot_high_candle_index, pivot_high, "HIGH")

    # # print("Found new pivot high  OR  Threshold not met. Either ways Continuing search...")
    return next_extreme_high_point(df, start_candle_index=start_candle_index, input_candle_index=next_candle_index, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold, absolute_threshold=absolute_threshold, pivot_high_candle_index=pivot_high_candle_index)

def next_extreme_low_point(df, start_candle_index=None, input_candle_index=None, percent_threshold=0, move_relative_percent_threshold=0, absolute_threshold=0, pivot_low_candle_index=-1):
    """
    Identifies the next extreme low point in a dataset of stock prices, filtering out minor movements.
    Debugging statements are active for detailed insights during execution.
    """
    if start_candle_index is None:
        start_candle_index = df.index.min()

    if input_candle_index is None:
        input_candle_index = start_candle_index

    if pivot_low_candle_index == -1:
        pivot_low_candle_index = input_candle_index

    pivot_low = df.loc[pivot_low_candle_index, 'Low']
    # # print(f"Starting search from index: {start_candle_index}, Input candle index: {input_candle_index}, Pivot low index: {pivot_low_candle_index}, Initial pivot low: {pivot_low}")

    engulfed_count = engulfed_candle_count(input_candle_index, df)
    next_candle_index = input_candle_index + engulfed_count + 1

    if next_candle_index > df.index.max():
        # # print(f"Reached the end of the DataFrame. No more candles to evaluate.End index of df is {df.index.max()}")
        # # print("pivot_low_candle_index is  ", pivot_low_candle_index)
        return (pivot_low_candle_index, pivot_low, "LOW")

    next_candle = df.loc[next_candle_index]
    # # print(f"Evaluating next candle at index {next_candle_index} with Low: {next_candle['Low']}")

    if next_candle_index > df.index.max():
        # print("Reached the end of the DataFrame. No more candles to evaluate.")
        return (pivot_low_candle_index, pivot_low, "LOW")

    if next_candle['Low'] < pivot_low:
        pivot_low = next_candle['Low']
        pivot_low_candle_index = next_candle_index
        # print(f"New pivot low found: {pivot_low} at index {pivot_low_candle_index}")
    else:
        move_in_low = next_candle['Low'] - pivot_low
        percent_low_move_threshold = pivot_low * (percent_threshold / 100)
        last_move = df.loc[start_candle_index, 'Low'] - pivot_low
        last_move_based_threshold = last_move * move_relative_percent_threshold /100
        low_move_abs_threshold = max(absolute_threshold, percent_low_move_threshold, last_move_based_threshold)
        # # print(f"Move in low: {move_in_low}, Last Move = {last_move}, Last Move based Threshold:{last_move_based_threshold}, Percent low move threshold: {percent_low_move_threshold}, Absolute threshold: {low_move_abs_threshold}")

        if move_in_low >= low_move_abs_threshold:  # Check for significant move away from the low
            # print(f"Threshold met. Returning pivot low index: {pivot_low_candle_index}")
            return (pivot_low_candle_index, pivot_low, "LOW")

    # # print("Found new pivot low  OR  Threshold not met. Either ways Continuing search...")
    return next_extreme_low_point(df, start_candle_index=start_candle_index, input_candle_index=next_candle_index, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold, absolute_threshold=absolute_threshold, pivot_low_candle_index=pivot_low_candle_index)

def next_extreme_candle(df, start_candle_index, input_candle_index=None, percent_threshold=0, move_relative_percent_threshold=0, absolute_threshold=0, pivot_high_candle_index=-1, pivot_low_candle_index=-1):
    """
    Identifies the next extreme point (high or low) in stock price data, filtering out minor fluctuations.

    Parameters:
    - df: DataFrame containing stock data.
    - start_candle_index: Index to start the search from.
    - input_candle_index: Current candle being considered. If None, set to start_candle_index.
    - percent_threshold: Minimum percentage movement required to consider a point significant.
    - absolute_threshold: Minimum absolute movement required to consider a point significant.
    - pivot_high_candle_index: Index of the current pivot high candle. Initialized to start_candle_index if -1.
    - pivot_low_candle_index: Index of the current pivot low candle. Initialized to start_candle_index if -1.

    Returns:
    - Index of the next extreme point that meets threshold criteria.
    """
    if start_candle_index is None:
        start_candle_index = df.index.min()

    if input_candle_index is None:
        input_candle_index = start_candle_index

    if pivot_high_candle_index == -1 and pivot_low_candle_index == -1:
        pivot_high_candle_index = pivot_low_candle_index = input_candle_index

    pivot_high = df.loc[pivot_high_candle_index, 'High']
    pivot_low = df.loc[pivot_low_candle_index, 'Low']

    engulfed_count = engulfed_candle_count(input_candle_index, df)
    next_candle_index = input_candle_index + engulfed_count + 1

    if next_candle_index >= df.index.max():
        # # print("Reached the end of the DataFrame. No further candles to evaluate. Giving most recent relevant point as default")
        if pivot_high_candle_index > pivot_low_candle_index:
              return (pivot_high_candle_index, pivot_high, "HIGH")
        elif pivot_high_candle_index < pivot_low_candle_index:
              return (pivot_low_candle_index, pivot_low, "LOW")
        else:
              return (pivot_high_candle_index, pivot_high, "HIGH")

    # # print(f"next_candle_index is {next_candle_index}")
    next_candle = df.loc[next_candle_index]

    # Adjust pivot points if the next candle sets a new extreme
    if next_candle['Low'] < pivot_low:
        pivot_low = next_candle['Low']
        pivot_low_candle_index = next_candle_index
        # # print(f"New pivot low found: {pivot_low} at index {pivot_low_candle_index}")
    else:
        move_in_low = next_candle['Low'] - pivot_low
        percent_low_move_threshold = pivot_low * (percent_threshold / 100)
        low_move_abs_threshold = max(absolute_threshold, percent_low_move_threshold)
        # Determine if the next extreme candle is a low or high point
        if move_in_low >= low_move_abs_threshold:
            if pivot_low_candle_index > start_candle_index:
                # # print(f"Pivot point is the next extreme low point and pivot_low_candle_index is : {pivot_low_candle_index}")
                return (pivot_low_candle_index, pivot_low, "LOW")
            else:
                # # print(f"Significant movement upwards from start_index identified at the candle index : {next_candle_index}..  exploring the high point now...")
                return next_extreme_high_point(df, start_candle_index=start_candle_index, input_candle_index=next_candle_index, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold, absolute_threshold=absolute_threshold, pivot_high_candle_index=-1)

    if next_candle['High'] > pivot_high:
        pivot_high = next_candle['High']
        pivot_high_candle_index = next_candle_index
        # # print(f"New pivot high found: {pivot_high} at index {pivot_high_candle_index}")
    else:
        move_in_high = pivot_high - next_candle['High']
        percent_high_move_threshold = pivot_high * (percent_threshold / 100)
        high_move_abs_threshold = max(absolute_threshold, percent_high_move_threshold)
        if move_in_high >= high_move_abs_threshold:
            if pivot_high_candle_index > start_candle_index:
                # # print(f"New pivot high found: {pivot_high} at index {pivot_high_candle_index}")
                return (pivot_high_candle_index, pivot_high, "HIGH")
            else:
                # # print(f"Significant movement downward from start_index identified at the candle index : {next_candle_index}..  exploring the low point now..")
                return next_extreme_low_point(df, start_candle_index=start_candle_index, input_candle_index=next_candle_index, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold, absolute_threshold=absolute_threshold, pivot_low_candle_index=-1)

    # Continue searching if neither threshold is met
    # # print("No significant move detected. Continuing search...")
    return next_extreme_candle(df, start_candle_index, next_candle_index, percent_threshold, move_relative_percent_threshold, absolute_threshold, pivot_high_candle_index, pivot_low_candle_index)

def zig_zag(df, percent_threshold=0,  move_relative_percent_threshold=0, absolute_threshold=0):
    """
    Generates a Zig Zag pattern by identifying a series of high and low extreme points
    in a given OHLC DataFrame.

    Parameters:
    - df: DataFrame containing OHLC data.
    - percent_threshold: The percentage movement threshold for considering an extreme point.
    - absolute_threshold: The absolute movement threshold for considering an extreme point.

    Returns:
    - A list of tuples, each containing the index of the extreme point and its type ("MAX" or "MIN").
    """

    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Initialize the list to store the extreme points
    extreme_points = []

    # Start with the first candle in the DataFrame
    start_candle_index = df.index.min()
    current_type = None  # Keep track of the current extreme type to alternate between high and low

    while True:
        # Use next_extreme_candle to find the next extreme point from the current starting point
        next_point_index, next_extreme_value, extreme_type = next_extreme_candle(df, start_candle_index, percent_threshold=percent_threshold, move_relative_percent_threshold=move_relative_percent_threshold,  absolute_threshold=absolute_threshold)

        # Debugging statement to show the progress
        # # print(f"Found extreme point at index {next_point_index} of type {extreme_type}")

        # Check if the next_point_index is None or if we've encountered a repeat
        if next_point_index == start_candle_index :
            # # print("Encountered a repeat index")
            # Repeat index happens because that point itself is the extreme point hence it points at itsel
            if next_point_index is None:
                # # print("Reached the End of dataframe")
                2==2
            break

        # Add the found extreme point to the list
        extreme_points.append((next_point_index, next_extreme_value, extreme_type))

        # Update start_candle_index for the next iteration
        start_candle_index = next_point_index

        # Check if we've reached the end of the DataFrame
        if start_candle_index == df.index.max():
            # # print("Reached the end of DataFrame.")
            break

    return extreme_points


# Breather Identification ----------------------------------------------

def Uptrend_BREATHER_IDENTIFICATION(start_point, Extreme_points, length_of_previous_trend_move, uptrend_correction_threshold=0, uptrend_retest_boundary_threshold=0):

    """
    Assess if the correction next to start_point is a small breather and can be ignored.
    """
    # # print(f"Starting Uptrend_BREATHER_IDENTIFICATION with start_point index: {start_point}")

    if Extreme_points[start_point][2] == "LOW":
        # # print("Starting point is a LOW, which is not suitable for uptrend analysis. High Point needed.")
        return ("High Point needed", 0)

    if start_point == 0:
        # # print("Start point is the first point in the series. No previous point to compute move length.")
        return ("No previous point to compute move length", 0)

    if start_point >= len(Extreme_points) - 1:
        # # print("Start point is the last point in the series. No points to assess after start_point.")
        return ("Start Point is the End Point", 0)

    start_point_value = Extreme_points[start_point][1]

    # Calculate upper and lower limits for the breather identification
    upper_limit = (1 + uptrend_retest_boundary_threshold / 100) * start_point_value
    # Lower Limit based on percentage correction
    lower_limit = start_point_value - (uptrend_correction_threshold / 100) * start_point_value
    # Lower_limit based on length of trend move
    # lower_limit = start_point_value - (uptrend_correction_threshold / 100) * length_of_previous_trend_move

    # # print(f"Upper limit: {upper_limit}, Lower limit: {lower_limit}, based on start_point_value: {start_point_value} and prev_point_value: {prev_point_value}")

    no_of_skips = 0

    for i in range(start_point + 1, len(Extreme_points)):
        next_point_value = Extreme_points[i][1]
        # # print(f"Evaluating point at index {i} with value {next_point_value}")

        if next_point_value > upper_limit:
            # # print(f"Point at index {i} exceeds the upper limit. Trend Continued.")
            return ("Trend Continued", no_of_skips)
        elif next_point_value < lower_limit:
            # # print(f"Point at index {i} falls below the lower limit. Trend Reversed.")
            return ("Trend Reversed", no_of_skips)
        else:
            no_of_skips += 1
            # # print(f"Point at index {i} is within breather thresholds. Continuing analysis...")

    # # print("Reached the end of Extreme_points without determining trend continuation or reversal.")
    return ("Breather Continued without trend reversal or continuation", 0)

def Downtrend_BREATHER_IDENTIFICATION(start_point, Extreme_points, length_of_previous_trend_move, downtrend_correction_threshold=0, downtrend_retest_boundary_threshold=0):
    """
    Assess if the correction next to start_point in a downtrend is a small breather and can be ignored.

    Parameters:
    - start_point: The index of the point within the Extreme_points list.
    - Extreme_points: List of tuples containing (index, value, type) of extreme points.
    - length_of_previous_trend_move:  length of the move preceding the start_point
    - df: DataFrame containing the OHLC data.
    - downtrend_correction_threshold: Percentage threshold above which a correction is considered significant.
    - downtrend_retest_boundary_threshold: Percentage threshold below which the downtrend is considered continued.

    Returns:
    - A tuple containing trend_status ("Continued" / "Reversed" / None / "incomplete" / "End Point") and no_of_skips.
    """
    # print(f"Starting Down_BREATHER_IDENTIFICATION with start_point index: {start_point}")

    if start_point == 0 or start_point >= len(Extreme_points) - 1:
        if start_point == 0:
            # print("No previous point to compute move length.")
            return ("No previous point to compute move length", 0)
        else:
            # print("Start point is the last point in the series. No points to assess after start_point.")
            return ("Start Point is the End Point", 0)

    if Extreme_points[start_point][2] != "LOW":
        # print("Starting point is not a LOW, which is necessary for downtrend analysis. LOW Point needed.")
        return ("LOW Point needed", 0)

    start_point_low = Extreme_points[start_point][1]

    lower_limit = (1 - downtrend_retest_boundary_threshold / 100) * start_point_low
    # Upper_limit based on percentage of the start point
    upper_limit = start_point_low + (downtrend_correction_threshold / 100) * start_point_low

    # Upper_limit based on length of trend move
    # upper_limit = start_point_low + (downtrend_correction_threshold / 100) * length_of_previous_trend_move

    # print(f"Calculated lower_limit: {lower_limit}, upper_limit: {upper_limit} based on start_point_low: {start_point_low} and length_of_trend_move: {length_of_trend_move}")

    no_of_skips = 0

    for i in range(start_point + 1, len(Extreme_points)):
        next_point_value = Extreme_points[i][1]
        # print(f"Evaluating point at index {i} with value {next_point_value}")

        if next_point_value < lower_limit:
            # print(f"Point at index {i} falls below the lower limit. Trend Continued.")
            return ("Trend Continued", no_of_skips)
        elif next_point_value > upper_limit:
            # print(f"Point at index {i} exceeds the upper limit. Trend Reversed.")
            return ("Trend Reversed", no_of_skips)
        else:
            no_of_skips += 1
            # print(f"Point at index {i} is within the breather thresholds. Continuing analysis...")

    # print("Reached the end of Extreme_points without determining trend continuation or reversal.")
    return ("Breather Continued without trend reversal or continuation", 0)

def BREATHER_FILTER(Extreme_points, uptrend_correction_threshold, downtrend_correction_threshold, uptrend_retest_boundary_threshold, downtrend_retest_boundary_threshold):
    """
    Filters out small corrections in large trends from a list of extreme points.

    Parameters:
    - Extreme_points: List of tuples containing (index, value, type) of extreme points.
    - uptrend_correction_threshold: Percentage threshold for uptrend corrections.
    - downtrend_correction_threshold: Percentage threshold for downtrend corrections.
    - uptrend_retest_boundary_threshold: Percentage threshold for retesting in uptrends.
    - downtrend_retest_boundary_threshold: Percentage threshold for retesting in downtrends.

    Returns:
    - A filtered list of extreme points.
    """
    # Validation check to ensure Extreme_points is not empty
    if not Extreme_points:
        print("Extreme_points list is empty. No points available for filtering.")
        return []

    filtered_extreme_points = [Extreme_points[0]]  # Initialize with the first point

    i = 1  # Start from the second point
    while i < len(Extreme_points):
        current_point = Extreme_points[i]
        # print(f"Evaluating point at index {i}: {current_point}")

        if current_point[2] == "HIGH":
            length_of_previous_trend_move = current_point[1] - filtered_extreme_points[-1][1]
            trend_status, no_of_skips = Uptrend_BREATHER_IDENTIFICATION(i, Extreme_points, length_of_previous_trend_move, uptrend_correction_threshold, uptrend_retest_boundary_threshold)
        elif current_point[2] == "LOW":
            length_of_previous_trend_move = filtered_extreme_points[-1][1]  -  current_point[1]
            trend_status, no_of_skips = Downtrend_BREATHER_IDENTIFICATION(i, Extreme_points, length_of_previous_trend_move, downtrend_correction_threshold, downtrend_retest_boundary_threshold)

        # print(f"Trend status: {trend_status}, No of skips: {no_of_skips}")
        a,b,c,d=0,0,0,0
        if trend_status == "Start Point is the End Point":
            filtered_extreme_points.append(current_point)
            a=1
            return filtered_extreme_points
        elif trend_status == "Trend Reversed":
            filtered_extreme_points.append(current_point)
            i += no_of_skips + 1  # Move to the next extreme point for evaluation
            b=1
        elif trend_status == "Trend Continued":
            i += no_of_skips + 1  # Skip minor correction points
            c=1
        elif trend_status == "Breather Continued without trend reversal or continuation":
            # Include all points starting from current_point till the end
            filtered_extreme_points.extend(Extreme_points[i:])
            d=1000
            break
    # print(a+b+c+d)
    return filtered_extreme_points

def plotAfterBreather(df, extreme_points, filtered_extreme_points):
    # Assuming df_last_3_months is your DataFrame with the last 3 months of OHLC data
    # Assuming Extreme_points and filtered_extreme_points are already defined
    df_last_3_months = df
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df_last_3_months['Date'],
                                        open=df_last_3_months['Open'],
                                        high=df_last_3_months['High'],
                                        low=df_last_3_months['Low'],
                                        close=df_last_3_months['Close'],
                                        name='Candlestick')])

    # Function to extract date and value for plotting
    def extract_date_value(points, df):
        # Corrected function to ensure 'idx' is defined in both comprehensions
        dates = [df.loc[idx, 'Date'] for idx, value, point_type in points if idx in df.index]
        values = [value for idx, value, point_type in points if idx in df.index]
        return dates, values

    # Original Extreme Points (with trend lines)
    dates, values = extract_date_value(extreme_points, df_last_3_months)
    fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers',
                            line=dict(color='Blue', width=2),
                            marker=dict(color='LightSkyBlue', size=1),
                            name='Original Trend'))

    # Filtered Extreme Points (with trend lines)
    filtered_dates, filtered_values = extract_date_value(filtered_extreme_points, df_last_3_months)
    fig.add_trace(go.Scatter(x=filtered_dates, y=filtered_values, mode='lines+markers',
                            line=dict(color='DarkGreen', width=2),
                            marker=dict(color='Green', size=1),
                            name='Filtered Trend'))

    # Customize the layout
    fig.update_layout(title='Stock Price Data with Trends',
                    xaxis_title='Date',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=False)

    # Show the plot
    fig.show()
