import random
from datetime import date, timedelta
from tqdm import tqdm
import pandas as pd
import os

def get_all_files(directory):
    """
    Gets a list of all files (excluding directories) within a directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list: A list of filenames within the directory.
    """
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except FileNotFoundError:
        print(f"Error: Directory '{directory}' not found.")
        return []

def generateStockData(days, incr):

    def get_next_day(current_date, incrr, incrby=1):
        current_date_obj = date.fromisoformat(current_date)  # Convert to date object

        if incrr==True: next_day = current_date_obj + timedelta(days=incrby)  # Add one day
        else: next_day = current_date_obj - timedelta(days=incrby)

        return next_day.strftime("%Y-%m-%d")  # Format as YYYY-MM-DD string
    def generate_price(base_price, volatility):
        """Generates a random price with volatility."""
        change = random.uniform(-volatility, volatility) * base_price
        return base_price + change
    def generate_split_factor(split_probability, split_ratio):
        """Generates a random split factor if a split occurs."""
        if random.random() < split_probability:
            return split_ratio
        else:
            return 1
    def generate_dividend_yield(dividend_yield_probability, dividend_yield_range):
        """Generates a random dividend yield if a dividend is paid."""
        if random.random() < dividend_yield_probability:
            return random.uniform(*dividend_yield_range)  # Uniform distribution within the range
        else:
            return 0
    def generate_stock_data(
        days=10,  # Number of data points (days)
        base_price=100,  # Base price
        volatility=0.1,  # Price volatility
        split_probability=0.1,  # Probability of a stock split
        split_ratio=2,  # Ratio of a stock split (e.g., 2:1)
        dividend_yield_probability=0.1,  # Probability of a dividend payment
        dividend_yield_range=(0.01, 0.05),  # Range for random dividend yield
        incr=True
    ):
        """
        Generates simulated stock data for a specified number of days.

        Args:
            days (int, optional): The number of data points (days) to generate. Defaults to 10.
            base_price (float, optional): The initial base price of the stock. Defaults to 100.
            volatility (float, optional): The level of price volatility. Defaults to 0.1.
            split_probability (float, optional): The probability of a stock split. Defaults to 0.1.
            split_ratio (int, optional): The ratio of a stock split (e.g., 2:1). Defaults to 2.
            dividend_yield_probability (float, optional): The probability of a dividend payment. Defaults to 0.05.
            dividend_yield_range (tuple, optional): The range for random dividend yield. Defaults to (0.01, 0.05).

        Returns:
            list: A list of dictionaries containing simulated stock data for each day.

        Disclaimer: The generated data does not represent or reflect the actual performance of any real-world security or financial instrument. It is solely intended for educational demonstrations and should not be used for any other purpose.
        """

        data = []
        # current_date="2023-01-01"
        current_date = get_next_day(current_date="2023-01-01", incrr=(incr==False), incrby=days)  # Replace with your desired start date (YYYY-MM-DD format)

        for i in range(days):
            # Generate random "open", "high", "low", and "close" prices, accounting for volatility
            open_price = generate_price(base_price, volatility)
            high_price = max(open_price, generate_price(open_price, volatility))
            low_price = min(open_price, generate_price(open_price, volatility))
            close_price = generate_price(open_price, volatility)

            # Calculate split factor
            split_factor = generate_split_factor(split_probability, split_ratio)

            # Calculate dividend yield
            dividend_yield = generate_dividend_yield(dividend_yield_probability, dividend_yield_range)

            # Adjust closing price for splits and dividends
            adjusted_close_price = close_price / split_factor * (1 - dividend_yield)

            # Simulate random volume
            volume = random.randint(1000, 10000)

            # Append data as a dictionary to the list
            data.append({
                "Date": current_date,
                "Open": open_price,
                "High": high_price,
                "Low": low_price,
                "Close": close_price,
                "Adj Close": adjusted_close_price,
                "Volume": volume,
                # "Split Factor": split_factor,
                # "Dividend Yield": dividend_yield,
            })

            # Update base price for the next day (optional)
            base_price = close_price  # This can be modified to implement different price change scenarios

            # Increment date for the next day's data (modify date format as needed)
            
            year, month, day = map(int, current_date.split('-'))
            current_date = get_next_day(current_date, incr)

        return data  # Return the generated data as a list of dictionaries

    # Example usage (optional):
    stock_data = generate_stock_data(days=days, incr=incr)  # Generate data for 20 days
    stock_data = pd.DataFrame(stock_data)
    return stock_data

def generateStocks(n=4):
    dirs = []
    tcdir = "content/SyntheticTC"
    f = get_all_files(tcdir)+["0.csv"]
    maxfilename = max([int(name.split('.')[0]) for name in f])
    
    for _ in tqdm(range(n)):
        df=generateStockData(days=590, incr=random.choice([True, False]))

        maxfilename+=1
        df.to_csv(f"{tcdir}/{str(maxfilename)}.csv", index=False)

generateStocks()