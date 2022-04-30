from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building


@SkillManager.register(
    "设置增产方案", {
        "加速": "speed"
    }
)
def set_increase_scheme(bt1:BlueTu, speed=True):
    """
    修改蓝图中所有的增产方案
    speed: 设置为加速方案
    """
    all_b = bt1.data
    op_b = all_b - all_b.select_sort()
    for building in op_b.selected_buildings:
        building: Building
        if "Unknown" in building.param and len(building.param["Unknown"])>0:
            building.param["Unknown"][0] = int(speed)