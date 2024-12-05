import pandas as pd

def latest_sma_with_differences(file_path):
    """
    Calculate the SMA for the latest available dates and check differences between SMAs.

    Parameters:
        file_path (str): Path to the CSV file containing stock data.
        sma_periods (list): List of integers indicating the SMA periods (e.g., [10, 20, 50]).

    Returns:
        pd.DataFrame: A DataFrame with SMAs for each symbol and their latest dates, plus differences.
    """
    
            

    sma_periods = [10, 20, 50]
    allowed_diff = 3
    try:
        # Load data
        stock_df = pd.read_csv(file_path)
        stock_df.set_index('Symbol', inplace=True)
        stock_df = stock_df.apply(pd.to_numeric, errors='coerce')

        # Prepare a dictionary to store SMA calculations
        sma_results = {}

        # Iterate over rows (each stock)
        for symbol, row in stock_df.iterrows():
            # Drop NaN values to compute SMAs
            valid_data = row.dropna()

            # Calculate SMAs only if there are enough data points
            if len(valid_data) >= min(sma_periods):
                latest_sma = {}
                for period in sma_periods:
                    if len(valid_data) >= period:
                        sma = valid_data.tail(period).mean()
                        latest_sma[f"SMA{period}"] = sma
                    else:
                        latest_sma[f"SMA{period}"] = None  # Not enough data for this SMA
                with open("execution_log.txt", "a") as log:
                    # Check differences between SMAs
                    if f"SMA10" in latest_sma and f"SMA20" in latest_sma:
                        sma10, sma20 = latest_sma["SMA10"], latest_sma["SMA20"]
                        if sma10 and sma20:
                            diff_10_20 = abs(sma20 - sma10) / sma10 * 100
                            latest_sma["Diff_10_20 (%)"] = diff_10_20
                            if diff_10_20 < allowed_diff:
                                print(f"Warning: Difference between SMA10 and SMA20 for {symbol} is less than {allowed_diff}%.")
                                log.write(f"Warning: Difference between SMA10 and SMA20 for {symbol} is less than {allowed_diff}%.")
                    
                    if f"SMA20" in latest_sma and f"SMA50" in latest_sma:
                        sma20, sma50 = latest_sma["SMA20"], latest_sma["SMA50"]
                        if sma20 and sma50:
                            diff_20_50 = abs(sma50 - sma20) / sma20 * 100
                            latest_sma["Diff_20_50 (%)"] = diff_20_50
                            if diff_20_50 < allowed_diff:
                                print(f"Warning: Difference between SMA20 and SMA50 for {symbol} is less than {allowed_diff}%.")
                                log.write(f"Warning: Difference between SMA20 and SMA50 for {symbol} is less than {allowed_diff}%.")

                sma_results[symbol] = latest_sma

        # Convert the results into a DataFrame for better readability
        sma_df = pd.DataFrame.from_dict(sma_results, orient='index')

        return sma_df

    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    result_df = latest_sma_with_differences('nasdaq_stock.csv')
    if result_df is not None:
        print(result_df)