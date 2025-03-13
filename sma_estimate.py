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

        # Load existing tracked stocks
        try:
            tracked_stocks_df = pd.read_csv(stock_file)
        except FileNotFoundError:
            tracked_stocks_df = pd.DataFrame()

        log_messages = []  # Collect log messages
        new_tracked_stocks = {}

        # Prepare a dictionary to store SMA calculations
        sma_results = {}

        # Iterate over rows (each stock)
        for symbol, row in stock_df.iterrows():
            valid_data = row.dropna()

            if len(valid_data) >= min(sma_periods):
                latest_sma = {}
                for period in sma_periods:
                    latest_sma[f"SMA{period}"] = valid_data.tail(period).mean() if len(valid_data) >= period else None

                for i in range(len(sma_periods) - 1):
                    sma_current = f"SMA{sma_periods[i]}"
                    sma_next = f"SMA{sma_periods[i + 1]}"
                    comparing_sma = f"{sma_periods[i]}-{sma_periods[i + 1]}"

                    # Initialize tracked stocks for this comparison if not already done
                    if comparing_sma not in new_tracked_stocks:
                        new_tracked_stocks[comparing_sma] = set()

                    # Calculate and compare differences
                    if sma_current in latest_sma and sma_next in latest_sma:
                        sma_val_current, sma_val_next = latest_sma[sma_current], latest_sma[sma_next]
                        if sma_val_current and sma_val_next:
                            diff = abs(sma_val_next - sma_val_current) / sma_val_current * 100
                            latest_sma[f"Diff_{sma_periods[i]}_{sma_periods[i + 1]} (%)"] = diff

                            # Handle warnings and tracking
                            tracked_stocks = (
                                set(tracked_stocks_df[comparing_sma].dropna())
                                if comparing_sma in tracked_stocks_df.columns
                                else set()
                            )
                            if diff < allowed_diff:
                                new_tracked_stocks[comparing_sma].add(symbol)
                                if symbol not in tracked_stocks:
                                    log_messages.append(
                                        f"Warning: Difference between {sma_current} and {sma_next} for {symbol} is less than {allowed_diff}%."
                                    )
                            elif symbol in tracked_stocks:
                                log_messages.append(
                                    f"Info: {symbol} no longer stays within \u00B1{allowed_diff}%. Removed from tracking."
                                )

                sma_results[symbol] = latest_sma

        # Update the tracking file
        max_length = max(len(values) for values in new_tracked_stocks.values())
        aligned_tracked_stocks = {
            key: list(values) + [""] * (max_length - len(values))  # Pad shorter lists with empty strings
            for key, values in new_tracked_stocks.items()
        }
        final_tracked_stocks = pd.DataFrame(aligned_tracked_stocks)
        final_tracked_stocks.to_csv(stock_file, index=False)

        # Write log messages
        with open("execution_log.txt", "a") as log:
            log.write("\n".join(log_messages) + "\n")

        # Convert results to DataFrame
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