import pandas as pd
import csv
import requests
import json

def update_nasdaq_index(date):
    """
    Update the NASDAQ index by reading from 'scraped_data.csv', extracting the stock symbols,
    and directly updating 'nasdaq_100.csv'; also extracting stock symbols and sales data into
    'nasdaq_stock.csv'.
    """
    scraped_file = "scraped_data.csv"
    scraped_df = pd.read_csv(scraped_file)

    stock_file = "nasdaq_stock.csv"
    try:
        # Extract the 'Symbol' column and rename 'Last Sale' to the given date
        new_df = scraped_df[['Symbol', 'Last Sale']].rename(columns={'Last Sale': date})
        # If the base file exists, merge the new data
        try:
            stock_df = pd.read_csv(stock_file)

            # Ensure the base file has 'Symbol' as its first column
            if stock_df.columns[0] != 'Symbol':
                raise ValueError("The base file does not have 'Symbol' as the first column.")
            # Merge the new column into the base DataFrame using 'Symbol' as the key
            updated_df = pd.merge(stock_df, new_df, how="outer", on="Symbol")
            updated_df = updated_df.rename(columns={updated_df.columns[-1]: date})
        except FileNotFoundError:
            # If the base file doesn't exist, the new DataFrame becomes the base
            updated_df = new_df
        # Save the updated DataFrame back to the base file
        updated_df.to_csv(stock_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
        print(f"Successfully updated {stock_file} with data for {date}")
    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure {scraped_file} exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


    base_file = "nasdaq_100.csv"
    try:
        # Extract the 'Symbol' column and rename it to the given date
        new_df = scraped_df[['Symbol']].rename(columns={'Symbol': date})
        # If the base file exists, merge the new data
        try:
            base_df = pd.read_csv(base_file)
            updated_df = pd.concat([base_df, new_df], axis=1)
        except FileNotFoundError:
            # If base file doesn't exist, the new DataFrame becomes the base
            updated_df = new_df
        # Save the updated DataFrame back to the base file
        updated_df.to_csv(base_file, index=False, quoting=csv.QUOTE_NONNUMERIC)
        print(f"Successfully updated {base_file} with data for {date}")
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure {scraped_file} exists.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    date = input("Enter the date of the data (YYYY-MM-DD): ")
    update_nasdaq_index(date)