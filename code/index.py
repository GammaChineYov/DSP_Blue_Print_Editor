class IndexGroup():
    def __init__(self):
        # 索引字典 索引值: 索引实例
        self.index_dict = {}

    @property
    def max_index(self):
        if self.index_dict:
            return max(self.index_dict.keys())
        else:
            return -1

    def make_index(self, index=None):
        # 生成index实例
        if index is None:
            index = Index(self.max_index+1)
            self.index_dict[index.value] = index
            return index
                
        elif type(index) is not Index:
            # 不是-1 并且没有生成过实例
            if index == 4294967295:
                pass
            elif  index not in self.index_dict:
                index = Index(index)
                self.index_dict[index.value] = index
                return index
            else:
                return self.index_dict[index]
        return index
    
    def make_indexs(self,num):
        # 生成多个索引
        index_list = []
        for i in range(num):
            index_obj = Index(self.max_index+1)
            self.index_dict[index_obj.value] = index_obj
            index_list.append(index_obj)
        return index_list

    def get_value(self, index):
        # 获取索引的值
        if type(index) is Index:
            return index.value
        return index
    
class Index():
    def __init__(self, index) -> None:
        self.value = index
        self.as_out_num = 0 # 作为输出点的次数