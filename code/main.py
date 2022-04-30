import os
os.chdir(r"C:\Users\Administrator\Documents\Dyson Sphere Program\Blueprint\仙术")
from this import d
import time
from blueTu import BlueTu
from magic_skill.skill_manager import SkillManager
from config import config


class BlueTuChange:
    """批量蓝图修改类"""
    file_dir = "./"

    def __init__(self) -> None:
        """加载蓝图"""
        # 获取需要改变的文件
        self.all_blueTu = {}
        # 查找蓝图
        file_list = self.find_blueTu()

        # 解码蓝图
        for filepath in file_list:
            BlueTu.load_blue_by_txt(filepath, sleep=0)
        time.sleep(0.5)

        # 加载蓝图
        for filepath in file_list:
            # 加载蓝图
            js_filepath = BlueTu.json_temp_filepath(filepath)
            bt1 = BlueTu(js_filepath)
            bt1.short_desc += "_仙术"
            
            self.all_blueTu[filepath] = bt1
        

    @classmethod
    def find_blueTu(cls, find_source=True):
        """ 查找蓝图文件
        find_source: True,查找非仙术蓝图。 False,查找仙术蓝图，判断标准: 文件名中带 _仙术
        """
        file_dir = cls.file_dir
        file_list = []
        for filename in os.listdir(file_dir):
            filepath = os.path.join(file_dir, filename)
            # 排除文件夹
            if not os.path.isfile(filepath):
                continue
            # 排除非蓝图文件
            back_Zhui = os.path.splitext(filename)[-1]
            if back_Zhui != ".txt":
                continue
            
            # 排除配置文件
            # if filename == config_filename:
            #     continue

            # 查找生成的仙术蓝图
            if "_仙术" in filename and not find_source:
                file_list.append(filepath)

            # 查找源蓝图
            elif not "_仙术" in filename and find_source:
                file_list.append(filepath)
        return file_list

    def save_all(self):
        """ 保存所有的蓝图"""
        # 输出仙术蓝图
        for filepath, bt1 in self.all_blueTu.items():
            save_filepath = os.path.splitext(filepath)[0] + "_仙术.txt" # 输出的文件路径
            bt1.to_txt(filepath=save_filepath)
            print(f"\n{filepath}\t=>\t{save_filepath}\n")

    @staticmethod
    def change_all_blueTu(func):
        """ 最后进行的操作"""
        
        def wrapper(self, *args, **kwargs):
            for bt1 in self.all_blueTu.values():
                func(self, bt1, *args, **kwargs)
            return 

        return wrapper
    
    
    def run(self):
        """ 执行蓝图修改操作并保存"""
        # 获取蓝图操作指令
        cmd_list = config.cmd_list

        # 执行蓝图修改操作
        for cmd in cmd_list:
            if type(cmd) is dict:
                config.update(cmd)
                continue
            for bt in self.all_blueTu.values():
                SkillManager.run(bt, cmd, config[cmd])
        # 保存蓝图
        self.save_all()



if __name__ == "__main__":
    # 加载蓝图
    bc = BlueTuChange()

    # 执行修改操作
    bc.run()

    print("恭喜你成功施展了仙术")
