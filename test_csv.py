import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import pandas as pd
import json
import math


# 写入文件
data_set = {
    'f_first_move_time': ['la' for i in range(50)],
    'f_third_move_time': ['la' for i in range(50)],
    'f_first_down_x': ['la' for i in range(50)],
    'f_first_down_y': ['la' for i in range(50)],
    'f_v_third_move_x': ['la' for i in range(50)],
    'f_v_third_move_y': ['la' for i in range(50)],
    'f_a_third_move_x': ['la' for i in range(50)],
    'f_a_third_move_y': ['la' for i in range(50)],
    'f_last_time': ['la' for i in range(50)],
    'f_last_move_x': ['la' for i in range(50)],
    'f_last_move_y': ['la' for i in range(50)],
    'label': ['la' for i in range(50)]}
df = pd.DataFrame(data_set)
df.index = range(len(df))
with open('/Users/Galaxy/Desktop/smartedge/practise.csv', 'a') as fdata:
    print(fdata.tell())
    fdata.write('\n')
    print(fdata.tell())
    fdata.seek(1)
    print(fdata.tell())
    fdata.seek(0, 2)
    df.to_csv(r'/Users/Galaxy/Desktop/smartedge/practise.csv', header=False, index=False, mode='a')
# print
#
# print(df.info())
# print("write over!")
