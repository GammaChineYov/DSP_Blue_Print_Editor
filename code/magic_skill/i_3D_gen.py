from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building
import re 
from .g_belt_gen import belt_gen
import math


g0_list = []
def g0_campare(point):
    """ 比对曾经的g0指令位置,重合则返回更高的位置"""
    for index, p in enumerate(g0_list):
        if math.dist(p, point) < 0.75:
            point = list(point)
            point[2] -= 0.25
            break
    g0_list.append(tuple(point))
    return point
        


@SkillManager.register(
    "3D打印文件转传送带", {
        "文件路径": "filepath",
        "X轴缩放": "x_scale",
        "Y轴缩放": "y_scale",
        "Z轴缩放": "z_scale",
        "X轴偏移": "x_bias",
        "Y轴偏移": "y_bias",
        "Z轴偏移": "z_bias",
        "Z轴生成区间": "z_select",
        "追加坐标": "append_point",
        "回到起点": "back_start_point"
    }
)
def gcode2point(bt1:BlueTu, filepath, x_scale=1, y_scale=1, z_scale=1, 
x_bias=0, y_bias=0, z_bias=0, z_select=(-10, 1000), 
append_point=tuple(),back_start_point=True):
    """ 将gcode文件的路径转换成传送带路径"""
    z_min, z_max = z_select
    # 读取文件并转换成坐标点
    point = [0, 0, 0]
    point_list = []
    # G0 F600 X113.853 Y111.25 Z1.4
    re_X = re.compile("X([-\d\.]+)")
    re_Y = re.compile("Y([-\d\.]+)")
    re_Z = re.compile("Z([-\d\.]+)")
    jump_g10 = False
    last_Z = 0
    last_cmd = "" # 上一条指令
    last_point = (0, 0, 0)
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            # 跳过 G10 G11区间
            if "G10" in line:
                jump_g10 = True
                continue
            if "G11" in line:
                jump_g10 = False
                continue
            if jump_g10:
                Z = re_Z.search(line)
                if Z:
                    Z = (float(Z.group(1)) - z_bias) * z_scale
                    point[2] = Z
                    continue

            # 正常生成点
            if "G0 " in line or "G1 " in line:
                X, Y, Z = re_X.search(line), re_Y.search(line), re_Z.search(line)
                X = (float(X.group(1)) - x_bias) * x_scale if X else point[0]
                Y = (float(Y.group(1)) - y_bias) * y_scale if Y else point[1]
                Z = (float(Z.group(1)) - z_bias) * z_scale if Z else point[2]
                # if "G0" in line:

                point[0] = X
                point[1] = Y
                point[2] = Z

                # input()
                # 距离过短则跳过
                dist = math.dist(point, last_point)
                if abs(last_point[2] - point[2]) < 0.1 and dist < 0.4:
                    # print(f"跳过:")
                    # print(f"{last_point}")
                    # print(f"{point}:距离:{dist}")
                    continue
                
                # G0指令抬升
                cmd = "G0" if "G0 " in line else "G1"
                # if cmd == "G0":
                if last_Z > Z and len(point_list) > 1:
                    # 上次高度 > 此次高度， 下降
                    p = list(point_list.pop(-1))
                    p[2] += -0.25
                    point_list.append(tuple(p))
                    p = list(point)
                    p[2] += -0.25
                    # p = g0_campare(p)
                    point_list.append(tuple(p))
                # elif (cmd == "G1" and last_cmd == "G0") and len(point_list)>1:
                elif last_Z < Z and len(point_list)>1:
                    # 上次高度 < 此次高度， 升高
                    # 将上一个点抬升0.25
                    p = list(point_list.pop(-1))
                    p[2] += +0.25
                    point_list.append(tuple(p))
                    # 当前点抬升0.25
                    p = list(point)
                    p[2] += 0.25
                    point_list.append(tuple(p))

                else:
                    point_list.append(tuple(point))
                
                last_point = tuple(point)
                last_cmd = cmd
                last_Z = 0


    point_list = point_list[1:-1]
    x_mean = sum([p[0] for p in point_list]) / len(point_list)
    y_mean = sum([p[1] for p in point_list]) / len(point_list)
    z_mean = sum([p[2] for p in point_list]) / len(point_list)
    # [print(i, p) for i, p in enumerate(point_list)]
    print(f"xyz均值:x:{x_mean}, y:{y_mean}, z:{z_mean}")
    print("Z轴坐标集: ",set([p[2] for p in point_list]))

    posdata = [[]]
    [posdata[0].extend((p[0]-x_mean, p[1]-y_mean, p[2])) for p in point_list if z_min < p[2] < z_max]
    posdata[0].extend(append_point)
    if back_start_point:
        sp = list(posdata[0][:3])
        sp[2] = posdata[0][-1]
        posdata[0].extend(tuple(sp))
        sp[2] = posdata[0][2]
        posdata[0].extend(tuple(sp))
    print("坐标长度:", len(point_list))
    print("post_data长度:", len(posdata[0])/3)
    print(f"第一个坐标是: {posdata[0][:3]}")
    print(f"最后一个坐标: {posdata[0][-3:]}")

    belt_gen(bt1=bt1, pos_data=posdata)

