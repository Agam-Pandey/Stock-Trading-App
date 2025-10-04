import requests
import os
import csv
from dotenv import load_dotenv
load_dotenv()

import os
import time
import requests

API_KEY = os.getenv("API_KEY")
limit = 1000

url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={limit}&sort=ticker&apiKey={API_KEY}'

tickers = []
request_count = 0
MAX_REQUESTS_PER_MIN = 5

def make_request(url):
    global request_count
    response = requests.get(url)
    request_count += 1

    # If we've hit the request limit, sleep before next call
    if request_count % MAX_REQUESTS_PER_MIN == 0:
        print("Rate limit reached. Sleeping for 65 seconds...")
        time.sleep(65)

    return response.json()

# First request
data = make_request(url)
for ticker in data.get('results', []):
    tickers.append(ticker)

# Paginate while next_url exists
while 'next_url' in data:
    print('Requesting next page', data['next_url'])
    data = make_request(data['next_url'] + f'&apiKey={API_KEY}')
    for ticker in data.get('results', []):
        tickers.append(ticker)

print(f"Total tickers fetched: {len(tickers)}")

if tickers:
    with open('tickers.csv', 'w', newline='') as csvfile:
        fieldnames = tickers[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(tickers)
    print("Data written to tickers.csv")
    
#Schema of the example Ticker    
example_ticker={'ticker': 'AMST', 
 'name': 'Amesite Inc.',
 'market': 'stocks',
 'locale': 'us',
 'primary_exchange': 'XNAS',
 'type': 'CS',
 'active': True,
 'currency_name': 'usd',
 'cik': '0001807166',
 'composite_figi': 'BBG00KY7FCW4',
 'share_class_figi': 'BBG00KY7FCX3',
 'last_updated_utc': '2025-10-04T06:06:02.949907152Z'}
