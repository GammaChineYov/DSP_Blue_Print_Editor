from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu,BuildingOprate
from building import Building


@SkillManager.register(
    "半层进爪", {
        "爪子高度": "height"
    }
)
def change_sort_height(bt1, height):
    """ 调整分拣器高度
    1.连接传送带那一端抬升
    2.无连接那一端抬升"""
    all_b:BuildingOprate = bt1.data
    sort_b = all_b.select_sort()
    belt_indexs = set(all_b.select_belt().get("index").values())
    for building in sort_b.selected_buildings:
        building: Building
        if building.in_index in belt_indexs:
            building.z =height 
            building.z2 =0 
        else:
            building.z2 =height 
            building.z =0 
