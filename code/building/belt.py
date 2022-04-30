from .building import Building

class Belt(Building):
    """ 传送带类"""

    def __init__(self, level=3, index=0, x=0, y=0, z=0, out_index=4294967295, in_index=4294967295) -> None:
        data = {
                "header": {
                    "index": index,
                    "area_index": 0,
                    "local_offset_x": x,
                    "local_offset_y": y,
                    "local_offset_z": z,
                    "local_offset_x2": x,
                    "local_offset_y2": y,
                    "local_offset_z2": z,
                    "yaw": 0,
                    "yaw2": 0,
                    "item_id": 2000 + level,
                    "model_index": 37,
                    "output_object_index": out_index,
                    "input_object_index": in_index,
                    "output_to_slot": 1,
                    "input_from_slot": 0,
                    "output_from_slot": 0,
                    "input_to_slot": 1,
                    "output_offset": 0,
                    "input_offset": 0,
                    "recipe_id": 0,
                    "filter_id": 0,
                    "parameter_count": 0
                },
                "param": {
                    "Belt": None
                }
            }
        super().__init__(data)