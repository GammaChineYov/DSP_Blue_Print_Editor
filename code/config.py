import json

class Config(dict):
    config_filename = "0_点我改配置.json"
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        # 加载配置文件
        self.load_config()
    
    def load_config(self,):
        """
        加载配置文件
        """
        with open(self.config_filename, 'r', encoding='utf-8') as f:
            self.update(json.load(f))
    
    @property
    def cmd_list(self):
        """仙术指令列表"""
        return self["你要施展的仙术"]

config = Config()



building_item_id ={
    "四项分流器": 2020,
    "大矿机": 2316,
    "一级传送带": 2001,
    "二级传送带": 2002,
    "三级传送带": 2003,
    "一级分拣器": 2011,
    "二级分拣器": 2012,
    "三级分拣器": 2013,
    "太阳能板":2205,

}
    