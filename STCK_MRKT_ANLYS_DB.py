import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Initialize the main window
root = tk.Tk()
root.title("Stock Market Analysis Dashboard")

# Create frames
top_frame = ttk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

bottom_frame = ttk.Frame(root)
bottom_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create labels, entry, and button widgets
symbol_label = ttk.Label(top_frame, text="Enter Stock Symbols (comma-separated):")
symbol_entry = ttk.Entry(top_frame, width=30)
analyze_button = ttk.Button(top_frame, text="Analyze", command=lambda: analyze_stock(symbol_entry.get(), start_date_cal.get(), end_date_cal.get()))

# Pack widgets
symbol_label.pack(side=tk.LEFT, padx=10, pady=10)
symbol_entry.pack(side=tk.LEFT, padx=10, pady=10)
analyze_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create widgets for date range selection
date_range_label = ttk.Label(top_frame, text="Select Date Range:")
start_date_label = ttk.Label(top_frame, text="Start Date:")
end_date_label = ttk.Label(top_frame, text="End Date:")

start_date_cal = DateEntry(top_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
end_date_cal = DateEntry(top_frame, width=12, background='darkblue', foreground='white', borderwidth=2)

# Pack additional widgets for date range selection
date_range_label.pack(side=tk.LEFT, padx=10, pady=10)
start_date_label.pack(side=tk.LEFT, padx=10, pady=10)
start_date_cal.pack(side=tk.LEFT, padx=10, pady=10)
end_date_label.pack(side=tk.LEFT, padx=10, pady=10)
end_date_cal.pack(side=tk.LEFT, padx=10, pady=10)

# Create section boxes for performance metrics
percentage_change_frame = ttk.Frame(top_frame, padding=(12, 6))
daily_return_frame = ttk.Frame(top_frame, padding=(12, 6))
average_volume_frame = ttk.Frame(top_frame, padding=(12, 6))

percentage_change_frame.pack(side=tk.LEFT, padx=10, pady=10)
daily_return_frame.pack(side=tk.LEFT, padx=10, pady=10)
average_volume_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Create labels for performance metrics
percentage_change_label = ttk.Label(percentage_change_frame, text="Percentage Change:")
daily_return_label = ttk.Label(daily_return_frame, text="Daily Return:")
average_volume_label = ttk.Label(average_volume_frame, text="Average Volume:")

# Pack performance metrics labels
percentage_change_label.pack(side=tk.LEFT)
daily_return_label.pack(side=tk.LEFT)
average_volume_label.pack(side=tk.LEFT)

# Create a canvas for plotting
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=bottom_frame)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Function to analyze stock and update the plot with date range and performance metrics
def analyze_stock(symbols, start_date, end_date):
    try:
        symbols_list = [symbol.strip() for symbol in symbols.split(',')]

        start_date = datetime.strptime(start_date, '%m/%d/%y').strftime('%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%m/%d/%y').strftime('%Y-%m-%d')

        data_frames = [yf.download(symbol, start=start_date, end=end_date) for symbol in symbols_list]
        data = pd.concat([df['Close'] for df in data_frames], axis=1)

        ax.clear()
        data.plot(ax=ax)
        ax.set_title(f"Stock Price Analysis for {', '.join(symbols_list)}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Closing Price in USD")
        ax.legend(symbols_list)
        canvas.draw()

        # Calculate and display performance metrics
        for i, symbol in enumerate(symbols_list):
            percentage_change = ((data_frames[i]['Close'].iloc[-1] - data_frames[i]['Close'].iloc[0]) / data_frames[i]['Close'].iloc[0]) * 100
            daily_return = data_frames[i]['Close'].pct_change().mean() * 100
            average_volume = data_frames[i]['Volume'].mean()

            # Display metrics in the labels with visual symbols
            percentage_change_label.config(text=f"Percentage Change ({symbol}): {percentage_change:.2f}%" + (" ↗" if percentage_change > 0 else " ↘"))
            daily_return_label.config(text=f"Daily Return ({symbol}): {daily_return:.2f}%" + (" ↗" if daily_return > 0 else " ↘"))
            average_volume_label.config(text=f"Average Volume ({symbol}): {average_volume:.2f}" + (" ↗" if average_volume > 0 else " ↘"))

    except Exception as e:
        print(f"Failed download for {symbols}: {e}")

# Run the main loop
root.mainloop()
