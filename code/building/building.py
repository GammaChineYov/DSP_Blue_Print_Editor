from index import Index
class Building():
    """
    建筑类
    """

    def __init__(self, data) -> None:
        self._out_index = None
        # 参数
        self.param = data.get('param', {})

        # 头部数据
        header = data['header']
        self.index = header['index']
        self.area_index = header['area_index']
        self.x = header['local_offset_x']
        self.y = header['local_offset_y']
        self.z = header['local_offset_z']
        self.x2 = header['local_offset_x2']
        self.y2 = header['local_offset_y2']
        self.z2 = header['local_offset_z2']
        self.yaw = header['yaw']
        self.yaw2 = header['yaw2']

        self.item_id = header['item_id']
        self.model_index = header['model_index']

        self.out_index = header['output_object_index']
        self.in_index = header['input_object_index']

        self.out_to_slot = header['output_to_slot']
        self.in_from_slot = header['input_from_slot']

        self.out_from_slot = header['output_from_slot']
        self.in_to_slot = header['input_to_slot']

        self.output_offset = header['output_offset']
        self.input_offset = header['input_offset']

        # 配方id
        self.recipe_id = header['recipe_id']

        # 过滤ID
        self.filter_id = header['filter_id']


    @property
    def out_index(self):
        return self._out_index
    
    @out_index.setter
    def out_index(self, value):
        if type(value) is Index:
            value.as_out_num += 1
        self._out_index = value

    @property
    def parameter_count(self):
        count = 0
        for value in self.param.values():
            if type(value) is list:
                count += len(value)
        return count
    
    def set_param(self, key, value, index):
        """
        设置param的某个参数, 有这个key时才可以设置
        key: 键,
        value: 值，
        index: 列表中的位置
        """
        if key in self.param:
            self.param[key][index] = value

    def to_json(self):
        # 将建筑数据打包成json格式的dict
        data = {
            "header": {
                "index": self.index,
                "area_index": self.area_index,
                "local_offset_x": self.x,
                "local_offset_y": self.y,
                "local_offset_z": self.z,
                "local_offset_x2": self.x2,
                "local_offset_y2": self.y2,
                "local_offset_z2": self.z2,
                "yaw": self.yaw,
                "yaw2": self.yaw2,
                "item_id": self.item_id,
                "model_index": self.model_index,
                "output_object_index": self.out_index,
                "input_object_index": self.in_index,

                "output_to_slot": self.out_to_slot,
                "input_from_slot": self.in_from_slot,

                "output_from_slot": self.out_from_slot,
                "input_to_slot": self.in_to_slot,

                "output_offset": self.output_offset,
                "input_offset": self.input_offset,

                "recipe_id": self.recipe_id,
                "filter_id": self.filter_id,
                "parameter_count": self.parameter_count
            },
            "param": self.param

        }
        return data
    
    def copy(self):
        """复制自身"""
        return Building(self.to_json())
    
    def link_to(self, building):
        """ 将建筑连接到另一个建筑， 传送带到另一个传送带,"""
        self.out_index = building.index
        self.out_to_slot = building.index.as_out_num
        
    
    def link_from(self, building):
        """ 将建筑从另一个建筑连接到自身, 垂直建造时连接低层建筑"""
        self.in_index = building.index
        
        

        
    