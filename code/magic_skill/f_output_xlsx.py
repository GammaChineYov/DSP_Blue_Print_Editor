from email.encoders import encode_noop
from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building
import csv
import os 


@SkillManager.register(
    "EXCEL导出", {
        "输出文件夹": "file_dir",
    }
)
def change_height(bt1:BlueTu, file_dir):
    """ 将所有建筑信息导出到excel用于分析
    """
    json_data = bt1.data.to_json()['buildings']
    
    header = list(json_data[0]['header'].keys()) + ['param']
    data = [list(v['header'].values()) + [str(v['param'])] for v in json_data ]
    filepath = os.path.join(file_dir, bt1.short_desc.strip("_仙术") + '.csv')
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        c = csv.writer(f)
        c.writerow(header)
        c.writerows(data)
    print(" csv 导出完成")
    exit()
    
    