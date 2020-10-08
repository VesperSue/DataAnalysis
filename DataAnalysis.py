import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy as np
import pandas as pd
import json
import math
import os
import linecache

BEST_FEEDBACK = 60


def get_distance(x0, y0, x1, y1):
    distance = math.sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))
    return distance


def get_coordinate_distance(x0, x1):
    return x1-x0



file_path = "/Users/Galaxy/Desktop/smartedge/gesture/5/5-50.json"
# /Users/Galaxy/Desktop/smartedge/gesture_2/1



#
with open(file_path, 'r') as f:
    line = json.load(f)
    print(line)
    print(type(line))
    number_down = []
    number_up = []
    for i in range(len(line)):
        if line[i]['name'] == "ACTION_DOWN":
            number_down.append(i)
        if line[i]['name'] == "ACTION_UP":
            number_up.append(i)

        # print(len(number_down))
        # print(len(number_up))
        # print(number_down)

    data = [[] for i in range(len(number_up))]
    for i in range(len(number_up)):
        for j in range(number_down[i], number_up[i]+1):
            data[i].append(line[j])

        # dataDict = {}
        # dataDict = data
        # print(dataDict[0])



    # 前60个像素点,最后一个move的位置
    last_move_x = []
    last_move_y = []
    last_location = []
    # 前60个像素点，最后一个move的时间
    last_time = []
    for i in range(len(number_down)):
        for j in range(len(data[i])):
            dst = get_distance(data[i][0]['x'],  data[i][0]['y'], data[i][j]['x'], data[i][j]['y'])
            if dst > BEST_FEEDBACK:
                last_move_x.append(data[i][j-1]['x'])
                last_move_y.append(data[i][j-1]['y'])
                last_time.append(data[i][j-1]['time'])
                ldst = get_distance(data[i][0]['x'],  data[i][0]['y'], data[i][j-1]['x'], data[i][j-1]['y'])
                break
            else:
                pass
            if j == len(data[i])-1:
                last_time.append(0)
                last_move_y.append(0)
                last_move_x.append(0)
    # print("lastmovex", last_move_x)
    # print("lastmovey ", last_move_y)
    # print("last_time ", last_time)

    # 画出第一次move和down🐶之间的时间散点图
    time = []
    time_third_move = []
    sequence = [0]*(len(number_down))
    # print(data[0])
    # print(line[number_down[0]+1]['time'])
    for i in range(len(number_down)):
        time.append(line[number_down[i]+1]['time'])
        time_third_move.append(line[number_down[i]+3]['time'])
    # print(time)
    # plt.scatter(sequence, time, alpha=0.5)


    # 画出每次手势的持续时间手势次序的关系折线图
    time_last = []
    sequence_number = []
    for i in range(len(number_up)):
        time_last.append(line[number_up[i]]['time'])
        sequence_number.append(i)
    # print(sequence_number)
    # plt.xlabel("x: sequence")
    # plt.ylabel('y: last time/ms')
    # plt.plot(sequence_number,time_last)
    # plt.show()

    # 画出第一落点的密度图
    first_down_x = []
    first_down_y = []
    first_location = []
    for i in range(len(number_down)):
        first_down_x.append(line[number_down[i]]['x'])
        first_down_y.append(line[number_down[i]]['y'])
        first_location.append([first_down_x[i], first_down_y[i]])
    # plt.scatter(first_down_x, first_down_y)
    # plt.show()

    # xy方向的第三个move瞬时速度
    v_third_move_x = []
    v_third_move_y = []
    a_third_move_x = []
    a_third_move_y = []
    for i in range(len(number_down)):
        if len(data[i]) < 4:
            v_third_move_x.append(0)
            v_third_move_y.append(0)
            a_third_move_x.append(0)
            a_third_move_y.append(0)
        else:
            current_distance_x = get_coordinate_distance(data[i][0]['x'], data[i][3]['x'])
            current_distance_y = get_coordinate_distance(data[i][0]['y'], data[i][3]['y'])
            current_time = data[i][3]['time'] - data[i][2]['time']
            if current_time == 0:
                v_third_move_x.append(0)
                v_third_move_y.append(0)
                a_third_move_x.append(0)
                a_third_move_y.append(0)
            else:
                v_x = current_distance_x / current_time
                v_y = current_distance_y / current_time

                v_third_move_x.append(v_x)
                v_third_move_y.append(v_y)
                a_x = v_x / current_time
                a_y = v_y / current_time
                a_third_move_x.append(a_x)
                a_third_move_y.append(a_y)
    # print("v_third_move_x", v_third_move_x)

    # for i in range(len(number_up)):
    #     print(len(data[i]))

    # # 第一次写入文件
    # dataset = {'f_first_move_time': time,
    #            'f_third_move_time': time_third_move,
    #            'f_first_down_x': first_down_x,
    #            'f_first_down_y': first_down_y,
    #            'f_v_third_move_x': v_third_move_x,
    #            'f_v_third_move_y': v_third_move_y,
    #            'f_a_third_move_x': a_third_move_x,
    #            'f_a_third_move_y': a_third_move_y,
    #            'f_last_time': last_time,
    #            'f_last_move_x': last_move_x,
    #            'f_last_move_y': last_move_y,
    #            'label': [1 for i in range(len(time))]}
    # df = pd.DataFrame(dataset)
    # df.to_csv(r'/Users/Galaxy/Desktop/smartedge/test.csv', header=True, index=True, mode='w')
    # print(df.info())
    # print("write over!")

    # 写入文件 没有header
    # dataset = {'f_first_move_time': time,
    #            'f_third_move_time': time_third_move,
    #            'f_first_down_x': first_down_x,
    #            'f_first_down_y': first_down_y,
    #            'f_v_third_move_x': v_third_move_x,
    #            'f_v_third_move_y': v_third_move_y,
    #            'f_a_third_move_x': a_third_move_x,
    #            'f_a_third_move_y': a_third_move_y,
    #            'f_last_time': last_time,
    #            'f_last_move_x': last_move_x,
    #            'f_last_move_y': last_move_y,
    #            'label': [1 for i in range(len(time))]}
    # df = pd.DataFrame(dataset)
# with open('/Users/Galaxy/Desktop/smartedge/test.csv', 'a') as fdata:
#     print(fdata.tell())
#     print(fdata.tell())
#     fdata.seek(0, 2)
#     print(fdata.tell())
#     fdata.write('\n')
#     print(fdata.tell())
#     df.to_csv(fdata, header=False, index=True, mode='a')
#     # print(df.info())
#     # print("write over!")
#     dataset.clear()




