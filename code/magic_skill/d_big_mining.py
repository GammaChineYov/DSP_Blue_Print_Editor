from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu
from building import Building


def find_near(target, func, start=0, end=10000, err=0.01):
    """ 二分法查找func中的target
    start, end: x的查找范围 """
    x1 = start
    x2 = end
    while True:
        m = (x1 + x2) /2
        y = func(m)
        if abs(y - target) < err:
            # print(f"目标功率: {target} \n匹配功率: {y} \n倍率设置: {m}\n")
            break
        if y > target:
            x2 = m
        else:
            x1 = m
    return m


@SkillManager.register(
    "调整大矿机采矿速度", {
        "目标功率": "power_value"
    }
)
def change_DaKuangJi_speed(bt1:BlueTu, power_value=None, speed=None):
    """ 
    修改大矿机采矿速率
    power_value: 根据采矿功率设定采矿速率, 0 -1000
    speed: 直接设定采矿速率
    """
    item_id = 2316
    index = 329
    coef = [2.76806866e+00, 2.38376640e-03, 0.168]
    comp = lambda p: coef[0]*p*p + coef[1]*p + coef[2]
    value = speed if speed else find_near(power_value, func=comp)
    bt1.data.set_param(key="Unknown", value=int(value*10000), index=index, item_id=item_id)
