import requests
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation

# CoinGecko API endpoint for Bitcoin price
bitcoin_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
show_last_n_prices = 10
update_interval_sec = 10

# Create lists to store timestamps and prices
timestamps = []
prices = []

# Create the figure and axis
fig, ax = plt.subplots()

# Initialize an empty line plot
line, = ax.plot([], [], label='Bitcoin Price (USD)')

# Set up the axis labels and legend
ax.set_xlabel('Time')
ax.set_ylabel('Price (USD)')
ax.set_title('Live Bitcoin Price')
ax.legend()

# Function to fetch and update Bitcoin price data
def update(frame):
    response = requests.get(bitcoin_api_url)
    data = response.json()
    print(data)
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    price = data['bitcoin']['usd']
    
    timestamps.append(timestamp)
    prices.append(price)
    
    # Update the line plot data
    line.set_data(timestamps, prices)
    
    # Adjust the x-axis limits for better visualization
    if len(timestamps) > show_last_n_prices:
        ax.set_xlim(timestamps[-1 * show_last_n_prices], timestamps[-1])
    else:
        ax.set_xlim(timestamps[0], timestamps[-1])

    # Adjust the y-axis limits to show the price range within the last n data points
    min_price = min(prices[-1 * show_last_n_prices:])
    max_price = max(prices[-1 * show_last_n_prices:])
    price_range = max_price - min_price
    ax.set_ylim(min_price - 0.1 * price_range, max_price + 0.1 * price_range)

    return line,

# Create an animation
ani = FuncAnimation(fig, update, frames=None, interval=update_interval_sec*1000)

plt.tight_layout()
plt.xticks(rotation=45)
plt.grid()
plt.show()