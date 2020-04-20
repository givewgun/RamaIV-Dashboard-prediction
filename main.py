import datetime
import tensorflow as tf 
from utils import GC_client as gc, data_formatter as fmt
import pandas as pd
import numpy as np
import json
import os
from flask import Flask, jsonify, request

# load model
model = tf.keras.models.load_model("model.hdf5")

# app
app = Flask(__name__)

@app.route("/")
def hello():
    print("DDDDDD")
    return 'Hello World!'

@app.route('/predict',methods=['POST'])
def predict():
    req_body = request.get_json()
    print(req_body)
    cur_datetime = req_body['datetime']
    begin_time, cur_time, cur_date, prev_date = fmt.get_format_date(cur_datetime)
    print(begin_time, cur_time, cur_date, prev_date)
    
    df = gc.fetch_data(cur_time, cur_date, prev_date)
    # df = pd.read_csv('test.csv')
    out = fmt.format_input(df, begin_time, cur_time)
    print("finished formatting input")
    # print(inp)
    # print(inp.shape)
    pred = model.predict(out)
    print("finished prediction")
    # print(pred)
    pred = fmt.format_output(pred, cur_time)
    print("finished formatting output")
    # print(pred)
    return json.dumps({'df' : df.to_json(orient='split', date_format='iso')})
    
@app.route('/testpost',methods=['POST'])
def test_post():
    req_body = request.json
    print(req_body)
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


# predict()
# x_test = np.load('test_work.npy')
# x_temp = np.asarray([x_test])
# y_tmp = model.predict(x_temp)
# print(y_tmp)