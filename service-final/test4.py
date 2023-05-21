import requests
import json
import pandas as pd
from matplotlib import pyplot as plt
import time
import numpy as np

from sklearn.preprocessing import StandardScaler
import joblib

time_point = 0
current_value = 0
count = 0
data1 = []


def judge_time(values):
    global count
    global time_point
    global data1
    # if time_point != values[0].get('update_at', ''):
    #     time_point = values[0].get('update_at', '')
    #
    #     # current_value = values[0].get('current_value', '')
    #     current_gm = values[0].get('current_value', '')
    #     current_hum = values[1].get('current_value', '')
    #     current_temp = values[2].get('current_value', '')
    #     current_wind = values[3].get('current_value', '')
    #     data1.append({'gm': current_gm, 'hum': current_hum, 'temp': current_temp, 'wind': current_wind})
    #
    #     count += 1
    #
    #     print(count)
    time_point = values[0].get('update_at', '')

    current_gm = values[0].get('current_value', '')
    current_hum = values[1].get('current_value', '')
    current_temp = values[2].get('current_value', '')
    current_wind = values[3].get('current_value', '')
    data1.append({'gm': current_gm, 'hum': current_hum, 'temp': current_temp, 'wind': current_wind})

    count += 1

    print(count)

    return data1


def send(send_cmd):
    headers_send = {'api-key': 'jE6UQFJ3fJ64YkU5yGj7zu0XBV8='}
    payload_send = {'': send_cmd}
    url_point_send = 'http://api.heclouds.com/cmds?device_id=1068071955'

    Point = requests.post(url_point_send, headers=headers_send, data=payload_send)
    # print(Point.text)

    t_send = str(Point.text)
    print(t_send)
    jtemp_send = json.loads(t_send)
    print(jtemp_send)


# 写一个求平均数的函数
def average(data_input):
    sum_temp = 0
    for i in range(len(data_input)):
        sum_temp += data_input[i]
    return sum_temp / len(data_input)


if __name__ == '__main__':
    data_value = []
    pingjun = 0
    flag = 0
    ccc = 0
    while True:
        headers = {'api-key': 'jE6UQFJ3fJ64YkU5yGj7zu0XBV8='}
        url_point = 'http://api.heclouds.com/devices/1068071955/datastreams?datastream_ids=gm,hum,temp,wind'
        Point = requests.get(url_point, headers=headers)

        t = str(Point.text)
        Jtemp = json.loads(t)
        data = Jtemp['data']
        # print(data)
        data_value = judge_time(data)

        if count == 10:
            ccc += 1
            mm = StandardScaler()
            mm1 = joblib.load('scalar01.joblib')
            df1 = pd.DataFrame(data1)
            print(df1)
            df1 = df1.iloc[:, :].values

            x_test = mm.fit_transform(df1)
            # 加载模型
            svr_load = joblib.load('LL_SVR1.joblib')  # LL_SVR.joblib是标签标准化的，LL_SVR1.joblib是没标准化的
            # 预测
            y_pred = svr_load.predict(x_test)
            print(y_pred)
            # y123456 = mm1.inverse_transform(y_pred.reshape(-1,1))
            # print(y123456)
            pingjun = average(y_pred)
            print(y_pred.reshape(-1, 1))
            print('pingjun=', pingjun)
            if (pingjun >= 7) and (flag != 3):
                if flag == 4:
                    send('d.')
                    flag = 3
                else:
                    send('c.')
            if ccc == 10:
                flag = 4
            if ccc == 20:
                flag = 5
            count = 0
            data1 = []
