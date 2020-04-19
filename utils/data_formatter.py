import os 
import pandas as pd
import datetime
from calendar import monthrange
import json
import numpy as np
from sklearn.preprocessing import StandardScaler

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
east_w = []
east_seg = []
east_seg_id = {}
west_w = []
west_seg = []
west_seg_id = {}
rama_iv_way = []

def load_segment():
    global east_w, east_seg, east_seg_id, west_w, west_seg, west_seg_id, rama_iv_way
    print(THIS_FOLDER)
    ways_json_f = os.path.join(THIS_FOLDER, 'mapping', 'segment.json')
    with open(ways_json_f) as json_file:
        ways_json = json_file.read()
        ways_json = json.loads(ways_json)
    east_w = ways_json['east']['way_id']
    east_w = [str(w) for w in east_w]
    east_seg = ways_json['east']['segment']
    west_w = ways_json['west']['way_id']
    west_w = [str(w) for w in west_w]
    west_seg = ways_json['west']['segment']
    rama_iv_way = east_w + west_w

    lon_seg_f =  os.path.join(THIS_FOLDER, 'mapping', 'lon_to_seg_map.json')
    with open(lon_seg_f) as json_file:
        lon_seg = json_file.read()
        lon_seg = json.loads(lon_seg)
    east_seg_id = lon_seg['east_seg_id']
    west_seg_id = lon_seg['west_seg_id']
    east_seg_id = { float(key):value for key,value in east_seg_id.items()}
    west_seg_id = { float(key):value for key,value in west_seg_id.items()}

load_segment()

def get_format_date():
    now = datetime.datetime.now()
    # now = datetime.datetime(2019, 8, 30, 17, 0, 59, 342380)
    cur_date = now.date()
    rounded_time = datetime.datetime.fromtimestamp(now.timestamp() // 60 * 60) #every 5 minutes (rounded floor)
    begin_time = rounded_time - datetime.timedelta(minutes=30)
    #mockup has only aug 2019 data
    cur_date = datetime.date(2019, 8, cur_date.day)
    #delete line 13-15 if real data has more than one month (full data)
    if cur_date.day == 1:
        prev_date = datetime.date(2019, 8, 31)
    else:
        prev_date = cur_date - datetime.timedelta(days=1)
    
    return begin_time.strftime("%H:%M:%S"), rounded_time.strftime("%H:%M:%S"), cur_date.strftime("%Y/%m/%d"), prev_date.strftime("%Y/%m/%d")

def normalize_matrix(x):
    scaler = StandardScaler()
    return scaler.fit_transform(x)


def find_time_col(begin_time, cur_time, x):
    time_begin = begin_time
    time_end = cur_time
    time_step = '5min'
    full_min_diff = ((pd.to_datetime(time_end) - pd.to_datetime(time_begin)).total_seconds() / 60)
    min_diff = ((pd.to_datetime(time_end) - pd.to_datetime(x)).total_seconds() / 60)
    index = (full_min_diff - min_diff) / int(time_step[:-3])
    # print(index)
    return int(index)

def format_input(df, begin_time, cur_time):
    #filter the way in geojsonfirst
    print(df.dtypes)
    df = df[df['wayids'].isin(rama_iv_way)].reset_index().drop(['index'], axis = 1)
    print(df.shape)
    #apply segment w or e 
    df['direction'] = 'w'
    df.loc[df['wayids'].isin(east_w), 'direction'] = 'e'

    #find segment
    df['segment'] = df.apply(lambda row: east_seg_id[round(row['lon3'],3)] if row['direction'] == 'e'\
                             else west_seg_id[round(row['lon3'],3)] + max(east_seg_id.values())+1, axis = 1)

    print(df.head())
    #find average speed per time
    df = df.groupby(['segment','time'])
    df = df.mean()['speed_mps'].reset_index()
    print(df.head())

    #create way_idx - time_step avg matrix
    avg_speed_mtx = np.full((max(east_seg_id.values())+1 + max(west_seg_id.values())+1, find_time_col(begin_time, cur_time, cur_time)), np.nan)
    print()
    for r in df.itertuples():
        col = find_time_col(begin_time, cur_time, str(r[2]))
        if col < avg_speed_mtx.shape[1]:
            avg_speed_mtx[r[1], find_time_col(begin_time, cur_time, str(r[2]))] = r[3]

    #normalize input
    avg_speed_mtx = normalize_matrix(avg_speed_mtx)
    print(avg_speed_mtx.shape)
    
    #fill nan with 0
    avg_speed_mtx = np.nan_to_num(avg_speed_mtx)
    np.savetxt('inp.csv', avg_speed_mtx, delimiter=',')

    avg_speed_mtx= np.reshape(avg_speed_mtx, avg_speed_mtx.shape + (1,))
    avg_speed_mtx = np.asarray([avg_speed_mtx])
    print(avg_speed_mtx)


    return avg_speed_mtx
