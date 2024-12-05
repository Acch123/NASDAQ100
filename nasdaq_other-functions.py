"""
These programs should be used based on needs
"""

import pandas as pd

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


if __name__ == "__main__":
    #rearrange_nasdaq_columns()
    # Choose the columns to drop
    delete_nasdaq_columns(["2024-11-23","2024-11-24"])

