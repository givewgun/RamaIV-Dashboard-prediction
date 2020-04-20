import requests
import json
import datetime
import pandas as pd
pd.set_option("display.max_rows", None, "display.max_columns", None)

# url = 'https://ramaivpredict-s66niuzd5q-de.a.run.app/predict'
# now = datetime.datetime.now()
# now = now.strftime("%Y/%m/%d %H:%M:%S")

# payload = {
#     'datetime' : now
# }

# # r = requests.get(url)
# r = requests.post(url, json = payload) 
# r = r.json()

# df = pd.read_json(r['df'], orient='split')
# with open('response.json', 'w') as outfile:
#     json.dump(r, outfile)

with open('response.json') as infile:
    data = json.load(infile)

df = pd.read_json(data['df'], orient='split')

print(df)
print(df.dtypes)