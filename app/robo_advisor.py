from dotenv import load_dotenv
import json
import csv
import os
import datetime
from IPython import embed

import requests

def to_usd(my_price):
    return"${0:,.2f}".format(my_price)

load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

# see: https://www.alphavantage.co/support/#api-key
api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
#print("API KEY: " + api_key) # TODO: remove or comment-out this line after you have verified the environment variable is getting read properly

valid_characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

while True:
        user_input = input("Please print name of stock")
        if all(char in valid_characters for char in user_input):
            break
        print("invalid stock choice, please enter another symbol")
#
# INFO OUTPUTS
#


request_url = "http://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&apikey=demo"

response = requests.get(request_url)

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

TSD = parsed_response["Time Series (Daily)"]
dates = list(TSD.keys())
latest_day = dates[0] #Assummes that latest day is first in list

latest_close = TSD[latest_day]["4. close"] #price for the close

#get highest closing price from each day and take the max of that

high_prices = []
low_prices = []

for date in dates:
    high_price = TSD[date]["2. high"]
    low_price = TSD[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))

latest_high = max(high_prices)
latest_low = min(low_prices)

#CF must continue
#averagelows = no.mean(high_prices)
#averagehighs = np.mean(low_prices)



#csv_file_path = "prices.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")

csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]


with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader()
    for date in dates:
        daily_prices = TSD[date]
        writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
        })
        
current_time = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")

print("-----------------")
print(f"STOCK SYMBOL: {symbol}")
print("RUN AT: " + (str(current_time))) 
print("-----------------")
print(f"LATEST DAY OF AVAILABLE DATA: {last_refreshed}") #fix
print(f"LATEST DAILY CLOSING PRICE: {to_usd(float(latest_close))}") #fix
print("RECENT AVERAGE HIGH CLOSING PRICE: {to_usd(float(latest_high))}")
print("RECENT AVERAGE LOW CLOSING PRICE: {to_usd(float(latest_low))}")
print("-----------------")
print("RECOMMENDATION: Buy!")
print("RECOMMENDATION REASON: Because the latest closing price is within threshold XYZ etc., etc. and this fits within your risk tolerance etc., etc.")
print("-----------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-----------------")
print("HAPPY INVESTING")
print("-----------------")

