from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import re
import csv
from datetime import datetime

def scrape_nasdaq_100():
    """
    Scrape the data on 'div' tag,
    save all the text in a file, 
    and filter out the table by regrex into a csv file.
    """
    print("Scraping data...")
    # Set up WebDriver
    service = Service("/opt/homebrew/bin/chromedriver")
    driver = webdriver.Chrome(service=service)
    # Open the website
    url = "https://www.nasdaq.com/market-activity/quotes/nasdaq-ndx-index"
    driver.get(url)
    # Wait for JavaScript to load
    time.sleep(5)

    # Get the page source
    #page_source = driver.page_source
    elements = driver.find_elements(By.TAG_NAME, "div")  # Or any other tag, e.g., "span", "a", etc.

    # Save the results in a txt file
    output_file = "scraped_data.txt"
    with open(output_file, "w", encoding="utf-8") as file:
        for i, div in enumerate(elements):
            try:
                # Get text content from the <div>
                content = div.text.strip()
                # Write to file if content exists
                if content:
                    file.write(f"Element {i + 1}:\n{content}\n{'-' * 30}\n")
            except Exception as e:
                file.write(f"Error scraping Element {i + 1}: {e}\n{'-' * 30}\n")


    # Define the file paths
    input_file = "scraped_data.txt"
    output_file = "scraped_data.csv"
    # Read the input file
    with open(input_file, "r") as file:
        data = file.read()

    # Regular expression to extract table rows
    regex = r"([A-Z]{1,5})\s+(.+?)\s+([\d,]+)\s+\$([\d,]+\.\d+)\s+(\$[\d,]+\.\d+|UNCH)\s+(UNCH|[+-]?\d+\.\d{2}%)"
    matches = re.findall(regex, data)
    matches = matches[:101]

    # Extract headers from the data manually
    headers = ["Symbol", "Name", "Market Cap", "Last Sale", "Net Change", "Percentage Change"]

    # Save the extracted data to a CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(matches)

    df = pd.read_csv(output_file)
    df["Last Sale"] = pd.to_numeric(df["Last Sale"].str.replace('[$,]', '', regex=True))
    df.to_csv(output_file, index=False)

    print(f"Table has been extracted and saved to {output_file}")


def scrape_nasdaq_date():
    """
    Reads a CSV file, searches for dates in the format 'Nov 24, 2024',
    and returns them as a string in 'YYYY-MM-DD' format.
    """
    with open("scraped_data.txt", "r") as file:
        data = file.read()

    # Define the regex pattern for the date format, e.g. 'Nov 24, 2024'
    date_pattern = r"\b([A-Za-z]{3})\s(\d{1,2}),\s(\d{4})\b"
    match = re.search(date_pattern, data)

    if match:
        month_abbr, day, year = match.groups()
        # Convert the matched date to 'YYYY-MM-DD' format
        date_obj = datetime.strptime(f"{month_abbr} {day} {year}", "%b %d %Y")
        date = date_obj.strftime("%Y-%m-%d")
        print(f"The data is scraped on {date}.")
        return date
    
    return None


if __name__ == "__main__":
    scrape_nasdaq_100()
    date = scrape_nasdaq_date()
    