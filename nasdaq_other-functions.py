"""
These programs should be used based on needs
"""

import pandas as pd
import matplotlib.pyplot as plt

def rearrange_nasdaq_columns():
    """
    Rearrange the columns of naasdaq_100.csv in date orders
    """
    base_file = "nasdaq_100.csv"

    try:
        # Load the base file
        df = pd.read_csv(base_file)

        # Sort the columns (dates as headers)
        sorted_columns = sorted(df.columns)

        # Reorder the DataFrame
        sorted_df = df[sorted_columns]

        # Save the updated file
        sorted_df.to_csv(base_file, index=False)
        print(f"Columns rearranged successfully in {base_file}!")
    except FileNotFoundError:
        print(f"Error: {base_file} not found. Ensure the file exists in the current directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def delete_nasdaq_columns(columns_list):
    """
    Delete the input column(s) from naasdaq_100.csv
    """
    file = "nasdaq_100.csv"
    df = pd.read_csv(file)
    # Drop the specified columns
    df = df.drop(columns=columns_list)
    df.to_csv(file, index=False)
    print(f"Columns deleted: {columns_list}")


def plot_stock_with_sma(file_path, stock_symbol, sma_periods=[10, 20, 50]):
    """
    Plot stock data along with SMA lines.

    Parameters:
        file_path (str): Path to the CSV file containing stock data.
        stock_symbol (str): The symbol of the stock to plot (e.g., 'AAPL').
        sma_periods (list): List of integers indicating the SMA periods (e.g., [10, 20, 50]).
    """
    try:
        # Load the stock data
        stock_df = pd.read_csv(file_path)
        stock_df.set_index('Symbol', inplace=True)

        # Get data for the specific stock
        if stock_symbol not in stock_df.index:
            print(f"Error: Stock symbol '{stock_symbol}' not found in the dataset.")
            return

        stock_data = stock_df.loc[stock_symbol].dropna()
        dates = stock_data.index[-len(stock_data):]  # Extract dates for x-axis
        dates = pd.to_datetime(dates, format = '%Y-%m-%d')

        # Plot the stock data
        plt.figure(figsize=(12, 6))
        plt.plot(dates, stock_data.values, label=f"{stock_symbol} Price", linewidth=2)

        # Calculate and plot SMAs
        for period in sma_periods:
            if len(stock_data) >= period:
                sma = stock_data.rolling(window=period).mean()
                plt.plot(dates, sma, label=f"SMA{period}", linestyle='--')

        # Customize the plot
        plt.title(f"{stock_symbol} Stock Price with SMAs")
        plt.xlabel("Dates")
        plt.ylabel("Price")
        plt.legend()
        plt.grid()
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    #rearrange_nasdaq_columns()
    #delete_nasdaq_columns(["2024-11-23","2024-11-24"])
    plot_stock_with_sma("nasdaq_stock.csv", "AAPL", sma_periods=[10, 20, 50])

