from blueTu import BlueTu


class SkillManager:
    """
    仙术管理器， 所有的仙术都放在这里
    使用方法: SkillManager.run(蓝图实例, "仙术名称", 参数字典)
    或者直接从SkillManager.skill_dict中获取仙术函数直接调用
    """
    skill_dict = {}
    skill_param_map = {}
    @classmethod
    def register(cls, skill_name, skill_param_map):
        """ 装饰器， 用于注册仙术到管理器
        skill_name: 仙术名称
        skill_param_map: 仙术功能 与 函数参数的映射
        参考:
        "御空":{
        "偏移高度": "h",
        "堆叠次数": "loop_num", 
        "保留底层建筑": "keep_bottom",
        "基底": "bottom_building_name" # 基底建筑名称
        }
        """
        def decorator(func):
            cls.skill_dict[skill_name] = func
            cls.skill_param_map[skill_name] = skill_param_map
            return func
        return decorator
    
    @classmethod
    def run(cls, bt1:BlueTu, skill_name, param_dict):
        """ 施展仙术
        bt1: 蓝图实例
        skill_name: 仙术名称
        param_dict: 参数字典
        """
        map = cls.skill_param_map[skill_name]
        param = {map[key]: value for key, value in param_dict.items()}
        cls.skill_dict[skill_name](bt1, **param)
