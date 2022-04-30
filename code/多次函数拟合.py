import numpy as np

data = np.array([
    0.1, 0.195,
    0.2, 0.278,
    0.5, 0.861,
    1,2.94,
    1.1, 3.52, 
    1.2, 4.15,
    1.3, 4.85,
    1.5, 6.4, 
    1.8, 9.14,
    # 2, 11.2,
    # 2.1, 12.3,
    # 2.5, 17.4,
    # 2.7, 20.3,
    # 2.9, 23.4,
    # 10, 277,
    # 20, 1100
])
x = data[::2]
y = data[1::2]
coef = np.polyfit(x, y, 2)
print("参数: ", coef)
coef = [2.76806866e+00, 2.38376640e-03, 0.168]
x = list(x)
x += [10, 20, 30, 100, 150, 200, 250, 300 ]
y_fit = np.polyval(coef, x)
y_fit = np.round(y_fit, 2)
# [print(x[i], i<len(y) and y[i], y_fit[i]) for i in range(len(x))]
target = 144 * 1000
err = 0.1
x1 = 0
x2 = 10000
while True:
    m = (x1 + x2) /2
    y_fit = np.polyval(coef, [m])
    if abs(y_fit[0] - target) < err:
        print(f"目标功率: {target} \n匹配功率: {y_fit[0]} \n倍率设置: {m}\n")
        break
    if y_fit[0] > target:
        x2 = m
    else:
        x1 = m
        

