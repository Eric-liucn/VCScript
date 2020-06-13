import pyhocon
from os import path
import os


class decorate(object):

    def __init__(self):
        self.color_1 = 1
        self.color_2 = 2
        self.slot_list = input("需要玻璃装饰充填的Slot序号(英文','分隔):\n ").split(',')
        self.conf_data = {}

    def gen(self):
        for slot in self.slot_list:
            data = {
                "Slot{}".format(int(slot)): [
                    {
                        "Item": {
                            "Count": 1,
                            "ItemType": "minecraft:stained_glass_pane",
                            "UnsafeDamage": int(self.color_1),
                            "DisplayName": ""
                        },
                        "Requirements": "tick % 40 <= 20"
                    },
                    {
                        "Item": {
                            "Count": 1,
                            "ItemType": "minecraft:stained_glass_pane",
                            "UnsafeDamage": int(self.color_2),
                            "DisplayName": ""
                        },
                        "Requirements": "tick % 40 > 20"
                    }
                ]
            }
            key = "Slot{}".format(int(slot))
            self.conf_data[key] = data.get(key)


if __name__ == "__main__":
    de = decorate()
    de.gen()
    if not path.exists(path.join(os.getcwd(), "gen_decorate")):
        os.mkdir(path.join(os.getcwd(), "gen_decorate"))
    with open(path.join(os.getcwd(), "gen_decorate", 'decorate.conf'), 'w+', encoding='utf-8') as file:
        conf = pyhocon.ConfigFactory.from_dict(de.conf_data)
        file.write(pyhocon.HOCONConverter.to_hocon(conf))
