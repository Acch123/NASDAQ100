import pandas as pd
import time
import re
import csv
import json
import requests
from datetime import datetime

def scrape_nasdaq_100():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
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


def scrape_api_nasdaq():
    """
    This is a function that scrape data from api.
    """
    url = "https://api.nasdaq.com/api/quote/list-type/nasdaq100"

    headers = {
        # Some websites will ignore uppercase for pseudo-headers like ":authority", 
        # so we typically omit them or adapt them to standard header style.
        "Accept": "application/json, text/plain, /",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://www.nasdaq.com",
        "Referer": "https://www.nasdaq.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }
    response = requests.get(url, headers=headers)
    # Check status, then parse JSON if successful
    if response.status_code == 200:
        data = response.json()
        # data should contain a dict with a "data" field listing the NASDAQ-100
        # print("Success! JSON keys:", data.keys())
        # data = data["data"]["data"]["rows"] # This is the list of the nasdaq-100
        with open("nasdaq.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        # If you want just the tickers, try something like:
        # all_symbols = [item["symbol"] for item in data["data"]["data"]]
        # print(all_symbols)
    else:
        print(f"Request failed: {response.status_code}")
        print(response.text)

    with open("nasdaq.json", "r") as file:
        json_data = json.load(file)
    # Extract headers and rows
    headers = json_data["data"]["data"]["headers"]
    rows = json_data["data"]["data"]["rows"]
    # Create a CSV file
    csv_file = "scraped_data.csv"
    # Map headers to their full names and write to CSV
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers.values())
        writer.writeheader()
        for row in rows:
            csv_row = {headers[key]: row[key] for key in headers if key in row}
            writer.writerow(csv_row)

    df = pd.read_csv(csv_file)
    df["Last Sale"] = pd.to_numeric(df["Last Sale"].str.replace('[$,]', '', regex=True))
    df.to_csv(csv_file, index=False)

    print(f"Table has been extracted and saved to {csv_file}.")
    
    date_string = json_data["data"]["date"]
    date_object = datetime.strptime(date_string, "%b %d, %Y %I:%M %p")
    date = date_object.strftime("%Y-%m-%d")
    print(f"The data is scraped on {date}")
    return date


if __name__ == "__main__":
    #scrape_nasdaq_100()
    #date = scrape_nasdaq_date()
    date = scrape_api_nasdaq()
    