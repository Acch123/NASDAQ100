import pandas as pd

def latest_sma_with_differences(file_path, stock_file="sma_warned_stocks.csv", sma_periods=[10, 20, 50], allowed_diff=2):
    """
    Calculate the SMA for the latest available dates and check differences between SMAs.

    Parameters:
        file_path (str): Path to the CSV file containing stock data.
        stock_file (str): Path to the file storing stocks with sma_diff < allowed_diff.
        sma_periods (list): List of integers indicating the SMA periods (e.g., [10, 20, 50]).
        allowed_diff (float): Maximum allowed difference (%) between SMAs.

    Returns:
        pd.DataFrame: A DataFrame with SMAs for each symbol and their latest dates, plus differences.
    """
    try:
        # Load data
        stock_df = pd.read_csv(file_path)
        stock_df.set_index('Symbol', inplace=True)
        stock_df = stock_df.apply(pd.to_numeric, errors='coerce')

        # Load existing stocks with sma_diff < allowed_diff
        try:
            tracked_stocks_df = pd.read_csv(stock_file)
            tracked_stocks = set(tracked_stocks_df['Symbol'])
        except FileNotFoundError:
            tracked_stocks = set()

        new_tracked_stocks = set()

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
                    # Loop through SMA periods to calculate differences
                    for i in range(len(sma_periods) - 1):
                        sma_current = f"SMA{sma_periods[i]}"
                        sma_next = f"SMA{sma_periods[i + 1]}"
                        
                        if sma_current in latest_sma and sma_next in latest_sma:
                            sma_val_current, sma_val_next = latest_sma[sma_current], latest_sma[sma_next]
                            if sma_val_current and sma_val_next:
                                diff = abs(sma_val_next - sma_val_current) / sma_val_current * 100
                                latest_sma[f"Diff_{sma_periods[i]}_{sma_periods[i + 1]} (%)"] = diff
                                
                                if diff < allowed_diff:
                                    new_tracked_stocks.add(symbol)
                                    if symbol not in tracked_stocks:
                                        log.write(
                                            f"Warning: Difference between {sma_current} and {sma_next} for {symbol} is less than {allowed_diff}%.\n"
                                        )
                                elif symbol in tracked_stocks:
                                    log.write(
                                        f"Info: {symbol} no longer stays within the \u00B1{allowed_diff}% region. Removed from tracking.\n"
                                    )

                sma_results[symbol] = latest_sma

        # Save new tracked stocks to the stock file
        tracked_stocks_df = pd.DataFrame({"Symbol": list(new_tracked_stocks)})
        tracked_stocks_df.to_csv(stock_file, index=False)

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