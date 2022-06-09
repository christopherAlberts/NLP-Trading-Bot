
from datetime import datetime
import requests
import pandas as pd

# CLEAN Altcoin Data
response = requests.get('https://api.altcointrader.co.za/v3/live-stats')
full_response = response.json()
num_of_currency = len(full_response)
num_of_info = len(full_response[next(iter((full_response.items())))[0]])

data = []
for i in range(num_of_currency):

        data.append({'Date': datetime.now(),
                # 'Coin': [altcoin_handler(list(altcoin_config.keys())[i], list(altcoin_config.keys())[j])]
                'Coin': list(full_response.keys())[i],
                'Price': full_response[list(full_response.keys())[i]]['Price'],
                'High': full_response[list(full_response.keys())[i]]['High'],
                'Low': full_response[list(full_response.keys())[i]]['Low'],
                'Buy': full_response[list(full_response.keys())[i]]['Buy'],
                'Sell': full_response[list(full_response.keys())[i]]['Sell'],
                'Volume': full_response[list(full_response.keys())[i]]['Volume'],
                # 'Fluctuation(%)': 100 * (float(full_response[list(full_response.keys())[i]]['High']) - float(full_response[list(full_response.keys())[i]]['Low'])) / float(full_response[list(full_response.keys())[i]]['High']),
                'Fluctuation(%)': 'null'
                })

df = pd.DataFrame (data, columns = ['Date', 'Coin', 'Price', 'High', 'Low', 'Buy', 'Sell', 'Volume', 'Fluctuation(%)'])

print (df)
df.to_csv('test.csv')

