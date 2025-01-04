import pandas as pd
from nasdaq_100_generate import update_nasdaq_index
from nasdaq_100_compare import compare_nasdaq_files
from nasdaq_100_scrape import scrape_nasdaq_100, scrape_nasdaq_date, scrape_api_nasdaq
from sma_estimate import latest_sma_with_differences

def process_nasdaq_100(new_date):
    """
    This function process the NASDAQ 100 table of the day into the csv file,
    and compare the difference of the latest two dates.
    """
    # Step 1: Generate the Nasdaq 100 data for the new date
    print(f"\nProcessing data for {new_date}...")
    update_nasdaq_index(new_date)
    
    # Step 2: Read the updated nasdaq_100.csv file to get the latest two dates
    try:
        df = pd.read_csv("nasdaq_100.csv")
        
        # Get the last two column headers (dates)
        date_columns = sorted(df.columns, reverse=True)
        if len(date_columns) < 2:
            print("Not enough data for comparison. Add more dates first.")
            return
        
        # Latest two dates
        latest_date = date_columns[0]
        second_latest_date = date_columns[1]
        print(f"Comparing the latest two dates: {second_latest_date}, {latest_date}...")
        
        # Step 3: Compare the Nasdaq 100 for the latest two dates
        compare_nasdaq_files(second_latest_date, latest_date)
    except FileNotFoundError:
        print("Error: 'nasdaq_100.csv' file not found. Please ensure it's created by the generator.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # 1. Scrape the data and the date from internet
    #scrape_nasdaq_100()
    #date = scrape_nasdaq_date()
    date = scrape_api_nasdaq()
    if date is None:
        print(f"The date of the data cannot be found, Please try again.")
    else:
        #2. Update the csv file, and do the comparison
        process_nasdaq_100(date)
    result_df = latest_sma_with_differences('nasdaq_stock.csv')
