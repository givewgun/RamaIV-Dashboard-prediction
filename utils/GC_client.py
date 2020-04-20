import os 
import pandas
import datetime
from google.cloud import bigquery

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"""C:\Users\givew\Documents\senior\predict-server\gcloud_credential.json"""
client = bigquery.Client()



def fetch_data(time, cur_date, prev_date):
    y,m,d = cur_date.split("/")
    cur_date = "".join(cur_date.split("/"))
    prev_date = "".join(prev_date.split("/"))
    query = """
            DECLARE cur_time TIME DEFAULT TIME "{}";
            DECLARE cur_date DATE DEFAULT DATE({},{},{});

            select FORMAT_TIMESTAMP("%R", TIMESTAMP_SECONDS(300 * DIV(UNIX_SECONDS(TIMESTAMP(datetime)), 300))) as time, 
            wayids as wayids, lon3 as lon3, AVG(speed) as `speed_mps` 
            from (
            select DATETIME(datetime, "Asia/Bangkok") as datetime, wayids as wayids,  ROUND(projectedlng,3) as lon3, speed 
            from (select * from saved.combined{} UNION ALL select * from saved.combined{}) 
            where DATE(datetime, "Asia/Bangkok") = cur_date AND (TIME(datetime, "Asia/Bangkok") BETWEEN TIME_SUB(cur_time, INTERVAL 30 MINUTE) AND cur_time)
            )
            GROUP BY wayids, lon3, FORMAT_TIMESTAMP("%R", TIMESTAMP_SECONDS(300 * DIV(UNIX_SECONDS(TIMESTAMP(datetime)), 300)));
            """.format(time, y, m, d, cur_date, prev_date)
    project_id = 'taxi-272612'
    df = client.query(query, project=project_id).to_dataframe()
    print("FINISH FETCHING")
    # df.to_csv('test.csv')
    return df
    



##query for single day
# DECLARE cur_time TIME DEFAULT TIME "{}";
# select FORMAT_TIMESTAMP("%T", TIMESTAMP_SECONDS(300 * DIV(UNIX_SECONDS(TIMESTAMP(DATETIME(datetime, "Asia/Bangkok"))) + 150, 300))) as time, wayids as wayids, ROUND(projectedlng,3) as lon3, AVG(speed) as `speed_kph` 
# from saved.combined20190819
# where time between TIME_SUB(cur_time, INTERVAL 40 MINUTE) and cur_time 
# GROUP BY wayids, ROUND(projectedlng,3) ,FORMAT_TIMESTAMP("%T", TIMESTAMP_SECONDS(300 * DIV(UNIX_SECONDS(TIMESTAMP(DATETIME(datetime, "Asia/Bangkok"))) + 150, 300)));
