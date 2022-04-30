from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building


@SkillManager.register(
    "御空", {
        "偏移高度": "h",
        "堆叠次数": "loop_num", 
        "保留底层建筑": "keep_bottom",
        "基底": "bottom_building_name" # 基底建筑名称
    }
)
def change_height(bt1:BlueTu, h, loop_num=1, keep_bottom=False, bottom_building_name=("一级传送带", "四项分流器")):
    """ 改变所有建筑的高度(除了四项分流器), 会带后缀_仙术, 排除带_仙术的文件
    "偏移高度": "h",
    "堆叠次数": "loop_num", 
    "保留底层建筑": "keep_bottom",
    "基底": "bottom_building_name" # 基底建筑名称
    """
    
    all_b = bt1.data
    # 获取并排除基底
    bottom_building:Building = sorted((all_b-all_b.select_sort()).selected_buildings, key=lambda b: abs(b.z))[0]
    oprate_buildings = all_b
    for name in bottom_building_name:
        item_id = building_item_id[name]
        _bottom_building = all_b.select(item_id=item_id) 
        if not _bottom_building.is_empty():
            bottom_building = tuple(_bottom_building.selected_buildings)[0]
            oprate_buildings = all_b - bottom_building
            break
    
        
    
    #调整所有建筑高度
    # 如果保留底层, copy次数+1, 提前进行复制
    if keep_bottom:
        oprate_buildings = oprate_buildings.copy()

    # 重复的复制建筑群并堆叠
    for n in range(loop_num):
        # 先判断是否保留底层
        # 第一次循环，如果保留底层则复制，不保留则跳过
        if n == 0: 
            if keep_bottom:
                oprate_buildings = oprate_buildings.copy()
        else:
            oprate_buildings = oprate_buildings.copy()

        # 偏移高度
        oprate_buildings.bias_pos(z=h)
        # 追加到原来的蓝图
        # 第一次如果不保留底层则不追加
        if n==0 and not keep_bottom:
            continue
        all_b.add_buildings(oprate_buildings)

    # 设置基底
    all_b.set_be_all_bottom(bottom_building=bottom_building)  # 设置所有建筑的堆叠基底， 运行此项可突破高度上限至42M

    # 设置基底高度
    bottom_building.z = 0
    bottom_building.z2 = 0
    # all_b.select_belt().set_pos(z=0)