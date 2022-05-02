from .skill_manager import SkillManager
from config import building_item_id
from blueTu import BlueTu, BuildingOprate
from building import Building, Belt
from index import IndexGroup
import math


@SkillManager.register(
    "传送带生成",{
        "传送带等级": "level",
        "关键坐标数据": "pos_data",
        }
)
def belt_gen(bt1:BlueTu, pos_data, level=3):
    """用于生成传送带
    pos_data = [
        [0, 0, 0,
         0, 0.05, 2.5,
         0, 0.06, 5 
        ],  # 一条从(0,0,0)到(0, 0.06, 5)的传送带
        [
         1, 0.06, 5,
         1, 0.05, 2.5,
         1, 0, 0
        ]  # 一条从(1, 0.06, 5)到(1,0,0)的传送带
    ]
    
    """
    index_group = IndexGroup()
    belts = BuildingOprate([])  # 传送带数据
    # 分条生成传送带
    for i, yiT_belt in enumerate(pos_data): # 获取每条传送带数据
        # 分节点处理传送带

        # 第一个节点
        pre_index = index_group.make_index() # 上一个索引
        pre_point = yiT_belt[:3] # 第一个节点
        print(f"第{i}条传送带,节点数:{len(yiT_belt)/3}")
        print("第一个点:", pre_point)
        pre_belt = Belt(index=pre_index, **dict(zip('xyz', yiT_belt[:3])), level=level) # 第一个传送带
        belts.selected_buildings.add(pre_belt)

        # 对每两节点间的传送带进行处理
        for point_n3 in range(3, len(yiT_belt), 3): #  获取每条传送带的节点
            # 计算两个节点间的距离
            point = yiT_belt[point_n3: point_n3+3]
            # 计算差值
            x= (point[0] - pre_point[0])
            y= (point[1] - pre_point[1])
            z= (point[2] - pre_point[2])
            dir = math.dist(point, pre_point) # 距离
            point_num = int(dir) +  (1 if dir - int(dir) > 0.2 else 0) # 两节点间需要的传送带数
            # 计算增量
            try:
                bias_x, bias_y, bias_z  = x / dir, y / dir, z / dir
            except:
                print(f"当前节点序号:{point_n3/3}")
                print(f"节点1:{pre_point}")
                print(f"节点2:{point}")
                raise "生成出错"

            # 生成每两节点间的传送带
            for n_belt in range(1, point_num): # 获取节点间的第n个传送带
                index = index_group.make_index()
                belt = Belt(index=index, 
                x=pre_point[0]+bias_x*n_belt,
                y=pre_point[1]+bias_y*n_belt,
                z=pre_point[2]+bias_z*n_belt,
                level=level
                )
                belts.selected_buildings.add(belt)
                # print([round(belt.x, 2), round(belt.y, 2), round(belt.z, 2)])
                

                # 更新上一个传送带
                pre_index = index
                pre_belt.link_to(belt) # 从上一个传送带连接到这个传送带
                pre_belt = belt
            
            # 节点间的传送带生成完毕, 生成一条传送带的中间节点
            if point_n3 + 3 != len(yiT_belt):
                # 生成节点传送带
                index = index_group.make_index()
                belt = Belt(index=index, x=point[0],y=point[1],z=point[2],level=level)
                belts.selected_buildings.add(belt)
                # print([round(belt.x, 2), round(belt.y, 2), round(belt.z, 2)])

                # 更新上一个传送带
                pre_index = index
                pre_belt.link_to(belt) # 从上一个传送带连接到这个传送带
                pre_belt = belt
                
            # 更新上一个节点
            pre_point = point
        
        # 一条传送带生成结束， 开始连接交叉点
        # 判断是否存在交叉点
        closest_belt = None
        for b in belts.selected_buildings:
            if abs(b.z - point[2]) < 0.1 and \
                abs(b.y - point[1]) < 0.1 and \
                abs(b.x - point[0]) < 0.1:
                closest_belt = b
                break
        # 如果存在交叉点， 连接， 不存在则生成新的传送带
        if closest_belt:
            pre_belt.link_to(closest_belt) # 从上一个传送带连接到这个传送带
        else:
            # 生成节点传送带
            index = index_group.make_index()
            belt = Belt(index=index, x=point[0],y=point[1],z=point[2],level=level)
            belts.selected_buildings.add(belt)
            # print([round(belt.x, 2), round(belt.y, 2), round(belt.z, 2)])

            # 更新上一个传送带
            pre_belt.link_to(belt) # 从上一个传送带连接到这个传送带
            

                
    
    # 将传送带添加到蓝图中
    bt1.data.add_buildings(belts)
    
            
            
                
            

