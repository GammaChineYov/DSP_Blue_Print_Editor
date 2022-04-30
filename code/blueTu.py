import os
import sys
import json
import time
from urllib import parse
from index import IndexGroup
from building import Building


dspbp_path = os.path.split(__file__)[0]
def dspbp_decode(source, target):
    """ 解码蓝图txt文件 -> json文件
    source: 解码前文件路径
    target: 解码后另存文件路径"""
    source = os.path.abspath(source)
    target = os.path.abspath(target)
    cmd = f'start /d "{dspbp_path}" dspbp.exe -i "{source}" -o "{target}" dump'
    os.system(cmd)

def dspbp_encode(source, target):
    """ 编码蓝图json文件 -> txt文件
    source: 编码前文件路径
    target: 编码后另存文件路径"""
    source = os.path.abspath(source)
    target = os.path.abspath(target)
    cmd = f'start /d "{dspbp_path}" dspbp.exe -o "{target}" -i "{source}" undump'
    print(cmd)
    os.system(cmd)

class BuildingOprate:
    """ 建筑操作类:
    """
    def __init__(self, data) -> None:
        "剪切板， 要进行操作的建筑列表"
        self.selected_buildings = set(data)

    def search_param(self, value, key=None):
        """ 根据参数值查找data["param"]中的参数所在位置
        return: dict, {建筑index: 参数位置}
        """
        out = {}
        for building in self.selected_buildings:
            for k, val_list in building.param.items():
                if key and k != key:
                    continue

                if type(val_list) is list and value in val_list:
                    out[building.index] = val_list.index(value)
                    
        return out
    
    def set_param(self, key, value, index, item_id=None):
        """
        根据item_id , 设定对应的参数值
        key: 键,
        value: 值，
        index: 列表中的位置
        item_id: 建筑数据中的item_id
        """
        for building in self.selected_buildings: 
            if item_id and building.item_id == item_id:
                building.set_param(key=key, value=value, index=index)
    
    def bias_pos(self, x=0, y=0, z=0):
        """ 偏移建筑位置，
        新位置=旧位置+偏移量"""
        for building in self.selected_buildings:
            building.x += x
            building.y += y
            building.z += z
            building.x2 += x
            building.y2 += y
            building.z2 += z    

    def set_pos(self, x=None, y=None, z=None):
        """ 设置建筑位置"""
        for building in self.selected_buildings:
            if x is not None:
                building.x = x
                building.x2 = x
            if y is not None: 
                building.y = y
                building.y2 = y
            if z is not None :
                building.z = z
                building.z2 = z
    
    def __add__(self, other):
        """实现选中项的并集操作, 返回新的BuildingOprate"""
        if type(other) is BuildingOprate:
            return BuildingOprate(self.selected_buildings | other.selected_buildings)
    
    def __sub__(self, other):
        """实现选中项的并集操作, 返回新的BuildingOprate"""
        if type(other) is BuildingOprate:
            return BuildingOprate(self.selected_buildings - other.selected_buildings)
        elif type(other) is Building:
            return BuildingOprate(self.selected_buildings - set((other,)))
    

    def _select(self, item_id=None):
        """ 
        根据条件选择特定的建筑
        item_id: 单个数字
        return: 选中的建筑组成的BuildingOprate
        """
        select = set()
        for building in self.selected_buildings:
            if item_id and building.item_id == item_id:
                select.add(building)
        return select
    
    def select(self, item_id=None):
        """ 
        根据条件选择特定的建筑
        item_id: 单个数字或 元组
        return: 选中的建筑组成的BuildingOprate
        """
        res = set()
        if item_id:
            if type(item_id) is int:
                res |= self._select(item_id=item_id)
            else:
                for ii in item_id:
                    res |= self._select(item_id=ii)
        return BuildingOprate(res)
    
    def _unselect(self, item_id=None):
        """
        根据条件排除特定的建筑
        return: 选中的建筑组成的BuildingOprate
        """
        select = set()
        for building in self.selected_buildings:
            if item_id and building.item_id == item_id:
                continue
            select.add(building)
        return select
    
    def unselect(self, item_id=None):
        """ 
        根据条件排除特定的建筑
        item_id: 单个数字或 元组
        return: 选中的建筑组成的BuildingOprate
        """
        res = BuildingOprate(self.selected_buildings)
        if item_id:
            if type(item_id) is int:
                res -= self._unselect(item_id=item_id)
            else:
                for ii in item_id:
                    res -= self._select(item_id=ii)
        return res
    
    def set(self, key, value):
        """ 所有选择的建筑设定某个参数的值 """
        for building in self.selected_buildings:
            building.__setattr__(key, value)

    def get(self, key):
        """ 获取选择的建筑的某个参数
        返回:{
            建筑对象: 值
        }
        """
        data = {}
        for building in self.selected_buildings:
            data[building] = building.__getattribute__(key)
        return data
    
    def select_belt(self, level=(2001, 2002, 2003)):
        """ 选择传送带
        level: int 1,2,3传送带等级, 若输入此项则选择特定等级的传送带"""
        if type(level) is int:
            level = 2000 + level
        return self.select(item_id=level)  # 传送带

    def select_sort(self, level=(2011, 2012, 2013)):
        """ 选择分拣器
        level: int 1,2,3传送带等级, 若输入此项则选择特定等级的传送带"""
        if type(level) is int:
            level = 2010 + level
        return self.select(item_id=level)  # 分拣器
    
    def is_empty(self):
        """ 是否没有选到建筑"""
        return len(self.selected_buildings) == 0

    def set_be_all_bottom(self, bottom_building:Building, only_item_id=None):
        """设置某个建筑为所有的基底, 用于突破蓝图的建造高度限制"""
        belts = self.select_belt()
        sorts = self.select_sort()
        up_buildings = self -belts - sorts - bottom_building

        # 特别操作, 只对某种建筑进行操作
        item_id = only_item_id
        if not item_id is None:
            if type(item_id) is int:
                up_buildings = up_buildings.select(item_id=item_id) 
            else:
                _temp = BuildingOprate([])
                for i_id in item_id:
                    _temp += up_buildings.select(item_id=i_id)
                up_buildings = _temp

        fx_index = bottom_building.index
        up_buildings.set("in_index", fx_index)
        up_buildings.set("out_to_slot", 14)
        up_buildings.set("in_from_slot", 15)
        up_buildings.set("out_from_slot", 15)
        up_buildings.set("in_to_slot", 14)

        
    def four_xiang_be_bottom(self, item_id=None):
        """
        将四项分流器作为堆叠基底进行堆叠, 排除传送带和钩子
        item_id: int或list\tuple, 如果输入此项,则只对对应item_id的进行操作
        """
        four_xiangs = self.select(item_id=2020) # 四项分流器
        belts = self.select_belt()
        sorts = self.select_sort()
        up_buildings = self -belts - sorts - four_xiangs
        if not item_id is None:
            if type(item_id) is int:
                up_buildings = up_buildings.select(item_id=item_id) 
            else:
                _temp = BuildingOprate([])
                for i_id in item_id:
                    _temp += up_buildings.select(item_id=i_id)
                up_buildings = _temp

        fx_index = four_xiangs.get('index').popitem()[1]
        up_buildings.set("in_index", fx_index)
        up_buildings.set("out_to_slot", 14)
        up_buildings.set("in_from_slot", 15)
        up_buildings.set("out_from_slot", 15)
        up_buildings.set("in_to_slot", 14)
    
    def scall(self, x_scale=1.0, y_scale=1.0, z_scale=1.0, origin=(0,0,0)):
        """ 对蓝图进行缩放
        x_scale,y_scale,z_scale: 各坐标轴缩放比例
        origin: (x, y, z), 缩放的原点， 默认为蓝图原点 
        """
        ox = origin[0]
        oy = origin[1]
        oz = origin[2]
        # 遍历所有选择的建筑
        for building in self.selected_buildings:
            building:Building
            building.x = ox + (building.x - ox) * x_scale
            building.y = oy + (building.y - oy) * y_scale
            building.z = oz + (building.z - oz) * z_scale

            building.x2 = ox + (building.x2 - ox) * x_scale
            building.y2 = oy + (building.y2 - oy) * y_scale
            building.z2 = oz + (building.z2 - oz) * z_scale

    def copy(self):
        """ 复制建筑群"""
        data = []
        for item in self.selected_buildings:
            data.append(item.copy())
        return BuildingOprate(data)
    

class BlueTuData(BuildingOprate):
    """
    蓝图数据类
    """
    
    def __init__(self, data):
        """ 
        data: 蓝图数据
        """
        header = data['header']

        # 头部数据
        self.version = header['version']
        self.cursor_offset_x = header['cursor_offset_x']
        self.cursor_offset_y = header['cursor_offset_y']
        self.cursor_target_area = header['cursor_target_area']
        self.dragbox_size_x = header['dragbox_size_x']
        self.dragbox_size_y = header['dragbox_size_y']
        self.primary_area_index = header['primary_area_index']
        self.area_count = header['area_count']

        # 蓝图区域数据
        areas = data['areas']
        self.areas = areas
        # self.index = areas['index']
        # self.parent_index = areas['parent_index']
        # self.tropic_anchor = areas['tropic_anchor']
        # self.area_segments = areas['area_segments']
        # self.anchor_local_offset_x = areas['anchor_local_offset_x']
        # self.anchor_local_offset_y = areas['anchor_local_offset_y']
        # self.width = areas['width']
        # self.height = areas['height']


        # 建筑列表
        self.buildings = []
        self.index_group = IndexGroup()
        for item in data['buildings']:
            # 生成建筑实例
            item_obj = Building(item)
            self.buildings.append(item_obj)
        # 生成索引
        index_dict = {item_obj.index: self.index_group.make_index(item_obj.index) for item_obj in self.buildings}
        index_dict[4294967295] = 4294967295
        for item_obj in self.buildings:
            item_obj.index = index_dict[item_obj.index]
            item_obj.in_index = index_dict[item_obj.in_index]
            item_obj.out_index = index_dict[item_obj.out_index]
        self.buildings = tuple(self.buildings)
        super().__init__(self.buildings)
    
    @property
    def buildings_count(self):
        # 建筑数量
        return len(self.buildings)
    
    def to_json(self):
        # 将蓝图数据打包成json格式
        buildings = []
        for item_obj in self.buildings:
            item_json = item_obj.to_json()
            item_json["header"]['index'] = self.index_group.get_value(item_obj.index)
            item_json["header"]['input_object_index'] = self.index_group.get_value(item_obj.in_index)
            item_json["header"]['output_object_index'] = self.index_group.get_value(item_obj.out_index)
            buildings.append(item_json)


        json_data = {
                "header": {
                    "version": self.version,
                    "cursor_offset_x": self.cursor_offset_x,
                    "cursor_offset_y": self.cursor_offset_y,
                    "cursor_target_area": self.cursor_target_area,
                    "dragbox_size_x": self.dragbox_size_x,
                    "dragbox_size_y": self.dragbox_size_y,
                    "primary_area_index": self.primary_area_index,
                    "area_count": self.area_count
                },
                "areas": self.areas,
                # [
                #     {
                #         "index": self.index,
                #         "parent_index": self.parent_index,
                #         "tropic_anchor": self.tropic_anchor,
                #         "area_segments": self.area_segments,
                #         "anchor_local_offset_x": self.anchor_local_offset_x,
                #         "anchor_local_offset_y": self.anchor_local_offset_y,
                #         "width": self.width,
                #         "height": self.height
                #     }
                # ],
                "building_count": self.buildings_count,
                "buildings": buildings
            }

        return json_data
    
    
    def add_buildings(self, building_oprate):
        """ 将两个建筑群组合到一起, building_oprate的索引信息将被修改
        building_oprate: BuilidngOprate, 被组合的建筑群"""
        # building_oprate的索引列表
        source_index_list = [building.index for building in building_oprate.selected_buildings]
        source_index_list = sorted(source_index_list, key=lambda index: index.value)
        # 新生成的索引列表
        target_index_list = self.index_group.make_indexs(num=len(building_oprate.selected_buildings))
        index_map_dict = dict(zip(source_index_list, target_index_list))
        index_map_dict.update({4294967295:4294967295})
        buildings = []
        for building in sorted(building_oprate.selected_buildings, key=lambda b: b.index.value):
            building: Building
            building.index = index_map_dict[building.index]
            building.in_index = index_map_dict[building.in_index]
            building.out_index = index_map_dict[building.out_index]
            
            # building.in_index = index_map_dict.get(building.in_index, 4294967295)
            # building.out_index = index_map_dict.get(building.out_index, 4294967295)
            buildings.append(building)
        self.buildings += tuple(buildings)
        self.selected_buildings = set(self.buildings)
        




class BlueTu():
    """
    蓝图操作类
    """
    json_tempfile_dir="json_temp"

    def __init__(self, filepath=None, json_data=None):
        """
        filepath: 蓝图的文件路径
        json_data: 蓝图的json格式的dict数据
        初始化
        """
        if filepath:
            print(filepath)
            if os.path.splitext(filepath)[-1] == '.txt':
                json_data = self.load_blue_by_txt(filepath)
            else: 
                json_data = json.load(open(filepath, 'r', encoding='utf-8'))

        # 简介
        self.short_desc = self.desc_decode(json_data.get('short_desc', ''))
        # 游戏版本
        self.game_version = json_data['game_version']
        self.layout = json_data['layout']
        self.icons = json_data['icons']
        self.timestamp = json_data['timestamp']
        self.data = BlueTuData(json_data['data'])
        

    @staticmethod
    def desc_encode(desc):
        """ 将蓝图简介编码成蓝图文件所需格式"""
        return parse.quote(desc)
    
    @staticmethod
    def desc_decode(desc):
        """ 将蓝图简介解码成正常文本"""
        return parse.unquote(desc)

    @classmethod
    def json_temp_filepath(cls, filepath):
        filepath = os.path.join(os.path.split(filepath)[0], cls.json_tempfile_dir, os.path.split(filepath)[1])
        return os.path.splitext(filepath)[0] + '.json'

    @classmethod
    def load_blue_by_txt(cls, filepath="./test.txt", json_save_dir=None, sleep=0.5):
        """
        加载蓝图文件成json格式
        filepath: 文件加载路径
        json_filepath: json文件保存路径
        sleep: 解码等待时间
        """
        # 读取，解码成字典
        if json_save_dir is None:
            json_filepath = cls.json_temp_filepath(filepath)
        else:
            json_filepath = os.path.join(json_save_dir, os.path.split(os.path.splitext(json_filepath)[0] + '.json')[1])
        dspbp_decode(source=filepath, target=json_filepath)
        time.sleep(sleep)   # 需要一些延时等待文件解码
        if os.path.isfile(json_filepath):
            with open(json_filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            return json_data
    
    
    def to_json(self, filepath=None):
        """ 
        filepath: 文件路径
        将蓝图导出成json格式"""
        json_data = {
            "layout": self.layout,
            "icons": self.icons,
            "timestamp": self.timestamp,
            "game_version": self.game_version,
            "short_desc": self.desc_encode(self.short_desc),
            "data": self.data.to_json()
        }
        
        # 打包成json格式文件
        if filepath:
            filepath = os.path.splitext(filepath)[0] + '.json'
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(json_data, f)
            
        
        return json_data
    
    def to_txt(self, filepath, json_save_dir=None):
        """
        将文件重新编码为txt格式
        filepath: 文件路径
        """
        if json_save_dir is None:
            json_filepath = self.json_temp_filepath(filepath)
        else:
            json_filepath = os.path.join(json_save_dir, os.path.split(os.path.splitext(json_filepath)[0] + '.json')[1])

        self.to_json(filepath=json_filepath)
        filepath = os.path.splitext(filepath)[0] + '.txt'
        dspbp_encode(source=json_filepath, target=filepath)
    

