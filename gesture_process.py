import json
import numpy as np
import pandas as pd
import math
BEST_FEEDBACK = 60


def get_distance(x0, y0, x1, y1):
    distance = math.sqrt((x1-x0)*(x1-x0)+(y1-y0)*(y1-y0))
    return distance


def get_coordinate_distance(x0, x1):
    return x1-x0


file_path = '/Users/Galaxy/Desktop/smartedge/gesture_2/data_raw.json'
with open(file_path, 'r') as f:
    line = json.load(f)
    print(len(line))
    js_line = []
    # js_line = json.loads(line[0])
    for i in range(len(line)):
        js_line.append(json.loads(line[i]))
        print(len(js_line))
    js_data = sum(js_line, [])
    print(len(js_data))
    print(js_data[0:2])
    number_down = []
    number_up = []

    for i in range(len(js_data)):
        if js_data[i]['name'] == "ACTION_DOWN":
            number_down.append(i)
        if js_data[i]['name'] == "ACTION_UP":
            number_up.append(i)

    print('down:', len(number_down))
    print('up', len(number_up))

    data = [[] for i in range(len(number_up))]
    for i in range(len(number_up)):
        for j in range(number_down[i], number_up[i]+1):
            data[i].append(js_data[j])

    # 前60个像素点,最后一个move的位置
    last_move_x = []
    last_move_y = []
    last_location = []
    # 前60个像素点，最后一个move的时间
    last_time = []
    for i in range(len(number_up)):
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

    # 画出第一次move和down🐶之间的时间散点图
    time = []
    time_third_move = []
    sequence = [0]*(len(number_up))
    for i in range(len(number_up)):
        time.append(js_data[number_down[i]+1]['time'])
        time_third_move.append(js_data[number_down[i]+3]['time'])

    # 画出每次手势的持续时间手势次序的关系折线图
    time_last = []
    sequence_number = []
    for i in range(len(number_up)):
        time_last.append(js_data[number_up[i]]['time'])
        sequence_number.append(i)

    # 画出第一落点的密度图
    first_down_x = []
    first_down_y = []
    first_location = []
    for i in range(len(number_up)):
        first_down_x.append(js_data[number_down[i]]['x'])
        first_down_y.append(js_data[number_down[i]]['y'])
        first_location.append([first_down_x[i], first_down_y[i]])

    # xy方向的第三个move瞬时速度
    v_third_move_x = []
    v_third_move_y = []
    a_third_move_x = []
    a_third_move_y = []
    for i in range(len(number_up)):
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

# 写入文件 没有header
    dataset = {'f_first_move_time': time,
               'f_third_move_time': time_third_move,
               'f_first_down_x': first_down_x,
               'f_first_down_y': first_down_y,
               'f_v_third_move_x': v_third_move_x,
               'f_v_third_move_y': v_third_move_y,
               'f_a_third_move_x': a_third_move_x,
               'f_a_third_move_y': a_third_move_y,
               'f_last_time': last_time,
               'f_last_move_x': last_move_x,
               'f_last_move_y': last_move_y,
               'label': [31 for i in range(len(time))]}
    df = pd.DataFrame(dataset)
with open('/Users/Galaxy/Desktop/smartedge/test2.csv', 'a') as fdata:
    df.to_csv(fdata, header=False, index=False, mode='a')
    print(df.info())
    print("write over!")
    dataset.clear()

