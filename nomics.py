import json

import pandas as pd
from datetime import date, timedelta
import urllib.request


API_key = "9881bfae39e5ffb6b94740a0fe09bed7"


# import urllib.request
# url = "https://api.nomics.com/v1/currencies/ticker?key=" + API_key + "&ids=BTC,ETH,XRP&interval=1Y,30d&convert=EUR&per-page=100&page=1"
# print(urllib.request.urlopen(url).read())

# import urllib.request
# url = "https://api.nomics.com/v1/volume/history?key=" + API_key + "&start=2018-04-14T00%3A00%3A00Z&end=2018-05-14T00%3A00%3A00Z&convert=EUR"
# print(urllib.request.urlopen(url).read())

# sdate = date(2021, 1, 1)   # start date
# edate = date(2021, 6, 8)   # end date
#
# delta = edate - sdate       # as timedelta
#
# for i in range(delta.days + 1):
#     day = sdate + timedelta(days=i)
#     print(day)
ticker = 'BTC'
currency_unit = 'ZAR'
start_date = date(2021, 1, 1)
end_date = date(2021,6, 5)
delta = end_date - start_date      # as timedelta

final_crypto_data = [{'currency': ticker, 'timestamps': [], 'prices': []}]

for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    print(day)

    url = "https://api.nomics.com/v1/currencies/sparkline?key=" + API_key + "&ids=" + ticker + "&start=" + str(day) + "T00%3A00%3A00Z&end=" + str(day) + "T00%3A00%3A00Z&convert=" + str(currency_unit)
    api_data = json.loads(urllib.request.urlopen(url).read().decode("utf-8"))

    date = api_data[0]['timestamps'][0]
    prices = api_data[0]['prices'][0]
    print(date)
    print(prices)
    final_crypto_data[0]['timestamps'].append(date)
    final_crypto_data[0]['prices'].append(prices)

print(final_crypto_data)



    # print("date: " + str(date))
    # print("prices: " + str(prices))


# print(len(api_data[0]['timestamps']))
# print(api_data[0])
# wakeword_data = {'Date' : api_data[0]['timestamps']}
# # date = []
# col = ['Date']
# for i in api_data:
#     currency = i['currency']
#     timestamp = i['timestamps']
#     prices = i['prices']
#
#     wakeword_data[currency] = prices
#
#     col.append(currency)
#
# # print(col)
# # print(wakeword_data)
#
# df = pd.DataFrame (wakeword_data, columns = col)
#
# print (df)
# # df.to_csv('test.csv')
# # print(api_data[0]['prices'])
