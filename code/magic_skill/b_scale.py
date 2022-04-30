from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building


@SkillManager.register(
    "缩地", {
        "纬度缩放比例": "x_scale",
        "经度缩放比例": "y_scale",
        "缩放传送带": "scale_belt"
    }
)
def change_scale(bt1, x_scale=1, y_scale=1, scale_belt=False):
    """缩放蓝图尺寸, 排除传送带"""
    all_b:BuildingOprate = bt1.data
    if scale_belt:
        op_b = all_b
    else:
        op_b = all_b - all_b.select_belt()
    op_b.scall(x_scale=x_scale, y_scale=y_scale)