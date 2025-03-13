# NASDAQ100 Stock Data Scraper & SMA Tracker

## 📌 Project Overview
This project scrapes NASDAQ 100 stock data, saves it to a CSV file, calculates Simple Moving Averages (SMA), and logs warnings if the differences between SMA values fall below a threshold. It automates data retrieval using API calls and can run on Windows/Mac via Task Scheduler.

## 🚀 Features
- Scrapes NASDAQ 100 stock data from the Nasdaq API
- Cleans and stores data in CSV format
- Computes SMA 10, 20, 50-day averages(customisable) for stock prices
- Logs warnings when SMA differences fall below the threshold
- Supports automated execution via Task Scheduler on Windows/Mac

## 📥 Installation & Setup
### 1️⃣ Prerequisites
- Python 3.8+
- `pip install` dependencies:
  ```bash
  pip install requests pandas matplotlib
  ```

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/Acch123/NASDAQ100.git
cd NASDAQ100
```

### 3️⃣ Running the Script Manually
```bash
python nasdaq_100_process.py
```


## 📊 Usage & Limitation
- You can add on functions based on the scraped data, e.g. plotting, and analysis
- Take a glimpse of scraping data methods
- Library such as 'yfinance' can scrape data with one day delay but the frequency is guaranteed. While this project can scrape real-time data but with less frequency (Scraping too often will result in API call fail).

## 🛠 Configuration
- Modify `allowed_diff` in `latest_sma_with_differences()` to adjust SMA margin for warning.
- Customize `sma_periods=[10, 20, 50]` in `sma_estimate.py` to adjust SMA threshold.
- Experience different scraping method in `nasdaq_100_scrape.py`. This project is using API as default, but you can scrape through selenium as well.

## 📄 License
This project is open-source under the MIT License.

## 🤝 Contributing
Pull requests and suggestions are welcome! Fork the repo and submit a PR.

---
💡 **Maintainer:** Angus Chan (chinghongchan.angus@gmail.com)

