import requests
import json
from pandas import json_normalize
from datetime import datetime

# importing libraries
import matplotlib.pyplot as plt

def Reverse(lst):
   new_lst = lst[::-1]
   return new_lst

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=NVDA&apikey=YTMVZXBN56T8IAM7'
r = requests.get(url)
data = r.json()

values = data['Time Series (Daily)']
list = []
dates = []
for key in values:
    list.append(values[str(key)]['4. close'])
    dates.append(key)

print(list)
print(dates)

n_list = []
n_dates = []
for i in range(30):
    n_list.append(list[i])
    n_dates.append(dates[i])

n_list = Reverse(n_list)
n_dates = Reverse(n_dates)


plt.plot_date(n_dates, n_list,'g')
plt.show()

