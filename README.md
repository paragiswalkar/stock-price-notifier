# Stock Price Notifier

## Overview

The Stock Price Notifier is a Python application that allows users to monitor real-time stock prices, set price thresholds for notifications, and visualize historical data using candlestick charts. It uses Tkinter for the graphical user interface (GUI), Alpha Vantage API for fetching stock data, and Matplotlib/mplfinance for chart visualization.

## Features

- **Live Stock Price Monitoring:** Fetches real-time stock prices from Alpha Vantage API.
- **Threshold Notifications:** Notifies users when stock prices cross specified thresholds.
- **Candlestick Chart Visualization:** Displays historical stock data using interactive candlestick charts.

## Requirements

- Python 3.6 or higher
- Tkinter (included in Python standard library)
- Matplotlib (for plotting graphs)
- mplfinance (for candlestick chart visualization)
- Requests (for making HTTP requests)
- Alpha Vantage API key (free API key available at [Alpha Vantage](https://www.alphavantage.co/support/#api-key))

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your/repository.git
   cd stock-price-notifier
   ```
   
## Install dependencies
```bash
pip install -r requirements.txt
```

## Set up Alpha Vantage API key:
1. Sign up for a free API key at Alpha Vantage.
2. Replace API_KEY variable in main.py with your API key.

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. Using the application:
   - Enter the stock code (e.g., AAPL, GOOGL) and set a price threshold.
   - Click Check Stock Price to fetch the current price and receive notifications based on the threshold.
   - Click Start Automation to monitor prices periodically.
   - Candlestick charts below the buttons visualize historical stock data.
