import requests
import json
import datetime
import pandas as pd

# url = 'http://localhost:5000/predict'
# now = datetime.datetime.now()
# now = now.strftime("%Y/%m/%d %H:%M:%S")

# payload = {
#     'datetime' : now
# }

# # r = requests.get(url)
# r = requests.post(url, json = payload) 
# r = r.json()

# with open('response.json', 'w') as outfile:
#     json.dump(r, outfile)

with open('response.json') as infile:
    data = json.load(infile)

df = pd.read_json(data['df'], orient='split')

print(df.dtypes)