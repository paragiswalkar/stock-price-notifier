import tkinter as tk
from tkinter import messagebox
import requests
import threading
import time
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import datetime
import requests.exceptions

# Replace with your Alpha Vantage API key
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

def get_live_data(stock_code):
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_code}&interval=1min&apikey={API_KEY}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"API Error: Status code {response.status_code}")
        
        data = response.json()
        time_series = data.get("Time Series (1min)")
        if not time_series:
            raise ValueError("Invalid response from Alpha Vantage API")
        
        latest_time = sorted(time_series.keys())[0]
        latest_data = time_series[latest_time]
        return float(latest_data["4. close"])
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to connect to Alpha Vantage API. Please check your internet connection.\nError: {str(e)}")
        return None
    
    except ValueError as e:
        messagebox.showerror("API Error", f"Error fetching data from Alpha Vantage API.\n{str(e)}")
        return None

def check_low_price(current_price, threshold):
    return current_price < threshold

def show_stock_data():
    stock_code = stock_code_entry.get()
    threshold_text = threshold_entry.get()
    
    if not stock_code or not threshold_text:
        messagebox.showerror("Input Error", "Please enter both stock code and price threshold.")
        return
    
    try:
        threshold = float(threshold_text)
        current_price = get_live_data(stock_code)
        
        if current_price is None:
            return  # Stop execution if there was an API error
        
        stock_info.set(f"Data for {stock_code} loaded. Checking price...")
        
        is_low = check_low_price(current_price, threshold)
        
        if is_low:
            messagebox.showinfo("Notification", f"The current price of {stock_code} is {current_price}, which is below the threshold of {threshold}.")
        else:
            messagebox.showinfo("Notification", f"The current price of {stock_code} is {current_price}, which is above the threshold of {threshold}.")
        
        update_candlestick_chart(stock_code)
    
    except ValueError:
        messagebox.showerror("Input Error", "Invalid price threshold. Please enter a valid number.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {stock_code}. Please try again.\nError: {str(e)}")
    
def check_price_periodically():
    stock_code = stock_code_entry.get()
    threshold_text = threshold_entry.get()
    
    if not stock_code or not threshold_text:
        print("Error: Stock code or threshold is missing.")
        return

    try:
        threshold = float(threshold_text)
    except ValueError:
        print("Error: Invalid price threshold.")
        return

    while True:
        try:
            current_price = get_live_data(stock_code)
            
            if current_price is None:
                continue  # Retry if there was an API error
            
            is_low = check_low_price(current_price, threshold)

            if is_low:
                print(f"Notification: The current price of {stock_code} is {current_price}, which is below the threshold of {threshold}.")
            else:
                print(f"The current price of {stock_code} is {current_price}, which is above the threshold of {threshold}.")
        
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
        
        # Wait for a specified period before checking again (e.g., 60 seconds)
        time.sleep(60)

def start_automation():
    thread = threading.Thread(target=check_price_periodically, daemon=True)
    thread.start()

def fetch_candlestick_data(stock_code, interval='1min'):
    try:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_code}&interval={interval}&apikey={API_KEY}'
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"API Error: Status code {response.status_code}")
        
        data = response.json()
        
        timestamps = list(data[f'Time Series ({interval})'].keys())
        timestamps.sort()
        prices = [float(data[f'Time Series ({interval})'][t]['4. close']) for t in timestamps]
        
        timestamps = [datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S') for t in timestamps]
        
        return timestamps, prices
    
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to connect to Alpha Vantage API. Please check your internet connection.\nError: {str(e)}")
        return None, None
    
    except ValueError as e:
        messagebox.showerror("API Error", f"Error fetching data from Alpha Vantage API.\n{str(e)}")
        return None, None

def update_candlestick_chart(stock_code):
    try:
        timestamps, prices = fetch_candlestick_data(stock_code)
        
        if timestamps is None or prices is None:
            return  # Stop execution if there was an API error
        
        fig, ax = mpf.plot(timestamps, prices, type='candle', volume=True, returnfig=True)
        ax.set_title(f'Candlestick Chart for {stock_code}')
        
        canvas = FigureCanvasTkAgg(fig, master=app)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {stock_code}. Please try again.\nError: {str(e)}")

# Create Tkinter application
app = tk.Tk()
app.title("NSE Stock Price Notifier")

# Create GUI elements
tk.Label(app, text="Stock Code:").pack()
stock_code_entry = tk.Entry(app)
stock_code_entry.pack()

tk.Label(app, text="Price Threshold:").pack()
threshold_entry = tk.Entry(app)
threshold_entry.pack()

stock_info = tk.StringVar()
tk.Label(app, textvariable=stock_info).pack()

tk.Button(app, text="Check Stock Price", command=show_stock_data).pack()
tk.Button(app, text="Start Automation", command=start_automation).pack()

# Start Tkinter main loop
app.mainloop()
