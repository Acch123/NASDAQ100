import pandas as pd
from datetime import datetime

def compare_nasdaq_files(date1, date2):
    """
    This function will take two dates as input,
    and compare the NASDAQ 100 of these two dates from nasdaq_100.csv,
    and report the result
    """
    try:
        # Load the CSV files
        df = pd.read_csv("nasdaq_100.csv")
        
        # Check if the specified dates are valid columns
        if date1 not in df.columns or date2 not in df.columns:
            print(f"Error: One or both dates ({date1}, {date2}) are not columns in the CSV file.")
            return
        
        # Extract the stock symbols
        stocks1 = set(df[date1].dropna())
        stocks2 = set(df[date2].dropna())
        
        # Compare the stocks
        added_stocks = stocks2 - stocks1
        removed_stocks = stocks1 - stocks2
        unchanged_stocks = stocks1 & stocks2

        with open("execution_log.txt", "a") as log:
            log.write(f"\nScript executed at {datetime.now()}\n")
            if bool(added_stocks) & bool(removed_stocks):
                log.write(f"Stocks added to NASDAQ 100 between {date1} and {date2}: ")
                log.write(f"{added_stocks}")
                log.write(f"\nStocks removed from NASDAQ 100 between {date1} and {date2}: ")
                log.write(f"{removed_stocks}\n")
                #log.write(f"\nStocks that remained in NASDAQ 100 between {date1} and {date2}:")
                #log.write(unchanged_stocks if unchanged_stocks else "None")
            else:
                log.write(f"All stocks have remained the same in NASDAQ 100 between {date1} and {date2}\n")
        # Display results
        if bool(added_stocks) & bool(removed_stocks):
            print(f"\nStocks added to NASDAQ 100 between {date1} and {date2}: ")
            print(added_stocks)
            print(f"\nStocks removed from NASDAQ 100 between {date1} and {date2}: ")
            print(removed_stocks)
            #print(f"\nStocks that remained in NASDAQ 100 between {date1} and {date2}:")
            #print(unchanged_stocks if unchanged_stocks else "None")
        else:
            print(f"\nAll stocks have remained the same in NASDAQ 100 between {date1} and {date2}")
    
    except FileNotFoundError as e:
        print(f"Error: {e}. Please ensure the file exists and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    # Ask for user input for the two dates
    date1 = input("Enter the first date (YYYY-MM-DD): ")
    date2 = input("Enter the second date (YYYY-MM-DD): ")
    if date1 > date2:
        print(f"Note that the first date should be earlier than the second date, or result might be reversed.")
    # Compare the NASDAQ 100 CSV files
    compare_nasdaq_files(date1, date2)


