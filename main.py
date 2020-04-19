import datetime
import tensorflow as tf 
from utils import GC_client as gc, data_formatter as fmt
import pandas as pd
import numpy as np

model = tf.keras.models.load_model("model.hdf5")

def predict():
    begin_time, cur_time, cur_date, prev_date = fmt.get_format_date()
    print(begin_time, cur_time, cur_date, prev_date)
    df = gc.fetch_data(cur_time, cur_date, prev_date)
    # df = pd.read_csv('test.csv')
    inp = fmt.format_input(df, begin_time, cur_time)
    # print(inp)
    # print(inp.shape)
    pred = model.predict(inp)
    print(pred)



predict()
# x_test = np.load('test_work.npy')
# x_temp = np.asarray([x_test])
# y_tmp = model.predict(x_temp)
# print(y_tmp)