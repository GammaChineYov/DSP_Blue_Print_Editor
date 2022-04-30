from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building


@SkillManager.register(
    "翻转传送带xz轴", {
    }
)
def belt_trans_xz(bt1:BlueTu):
    """翻转传送带XZ轴,让它竖起来"""
    belts = bt1.data.select_belt()
    for building in belts.selected_buildings:
        building.x,building.z =building.z, building.x
        building.x2,building.z2 =building.z2, building.x2