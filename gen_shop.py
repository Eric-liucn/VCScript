import pyhocon
import os
from os import path


def is_valid_item_id(item_str: str):
    strings = item_str.split(":")
    if not len(strings) == 4:
        return False
    if not strings[2].isdigit():
        return False
    if not strings[3].isdigit() or int(strings[3]) < 0:
        return False
    return True


def is_valid_transaction_number(num: str):
    if not num.isdigit() or num == '' or num is None or int(num) <= 1 or int(num) > 64:
        return False
    else:
        return True


class shop(object):

    def __init__(self):
        self.file_name = input("请输入改商店菜单的文件名称：\n")
        while self.file_name == '' or self.file_name is None:
            self.file_name = input("商店菜单文件名称有误，请重新输入\n")
        self.shop_title = input("商店菜单标题：\n")
        while self.shop_title == '' or self.shop_title is None:
            self.shop_title = input("商店菜单标题有误，请重新输入\n")
        self.this_page = input("该商店页码：\n")
        while not self.this_page.isdigit() or self.this_page is None:
            self.this_page = input("商店页码输入有误，请重新输入\n")
        self.total_page = input("该商店的总页数：\n")
        while not self.total_page.isdigit() or self.total_page is None:
            self.total_page = input("该商店的总页数输入有误，请重新输入：\n")
        self.item_extra_traction_number = input("请输入批量交易数量：\n")
        if not is_valid_transaction_number(self.item_extra_traction_number):
            self.item_extra_traction_number = input("输入错误，请输入批量交易数量：\n")
        self.currency = input("请输入该商店使用的货币：\n")
        if self.currency == '' or self.currency is None:
            self.currency = input("输入有误，请输入该商店使用的货币：\n")
        self.currency_alias = input("请输入该种货币的别名：\n")
        if self.currency_alias == '' or self.currency_alias is None:
            self.currency_alias = input("输入有误，请重新输入商店使用货币的别名：\n")
        plugin = input("请输入所使用的经济插件的id:\n"
                       "[1] totaleconomy\n"
                       "[2] economylite\n")
        while plugin == '' or plugin is None or not plugin.isdigit() or int(plugin) not in [1, 2]:
            plugin = input("请输入所使用的经济插件的id:\n"
                           "[1] totaleconomy\n"
                           "[2] economylite\n")
        if int(plugin) == 1:
            self.eco_plugin = 'totaleconomy'
        elif int(plugin) == 2:
            self.eco_plugin = 'economylite'

        self.rows = 6
        self.update_tick = 20
        self.accept_tick = 10
        self.shop_mode = input("------选择商店模式------\n"
                               "[1] 仅出售\n"
                               "[2] 仅收购\n"
                               "[3] 出售的同时收购\n"
                               "请输入 1 - 3 的数字来选择：\n")
        if not self.shop_mode.isdigit() or self.shop_mode is None or not int(self.shop_mode) in [1, 2, 3]:
            self.shop_mode = input("---输入错误，请重新选择---：\n"
                                   "[1] 仅出售\n"
                                   "[2] 仅收购\n"
                                   "[3] 出售的同时收购\n"
                                   "请输入 1 - 3 的数字来选择：\n")
        self.data = {
            'virtualchest': {
                'TextTitle': self.shop_title,
                'Rows': self.rows,
                'AcceptableActionIntervalTick': self.accept_tick,
                'UpdateIntervalTick': self.update_tick
            }
        }

    def only_buy(self):
        for i in range(1):
            item = input("请输入第{}个商品文本：\n".format(i))
            if not is_valid_item_id(item):
                item = input("请输入第{}个商品文本：\n")
            strings = item.split(":")
            item_id = strings[0] + ":" + strings[1]
            item_meta = int(strings[2])
            item_price = float(strings[3])
            item_lore = [
                "&a&l出售",
                "&b左键点击一次购买 &e1 &b个",
                "&b左键Shift点击一次购买 &e{} &b个".format(self.item_extra_traction_number),
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias)
            ]
            item_lore_1 = [
                "&a&l出售",
                "&b左键点击一次购买 &e1 &b个",
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias)
            ]
            item_lore_2 = [
                "&a&l出售",
                "&4你没有足够的钱",
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias)
            ]
            primary_click_once_commands = """cost: {}:{}:{};
                                             console: give %player_name% {} 1 {};
                                             sound: minecraft:block.note.hat""".format(self.eco_plugin,
                                                                                       self.currency,
                                                                                       item_price,
                                                                                       item_id,
                                                                                       item_meta)

            primary_shift_click_commands = """cost: {}:{}:{};
                                              console: give %player_name% {} {} {};
                                              sound: minecraft:block.note.hat""".format(self.eco_plugin,
                                                                                        self.currency,
                                                                                        item_price * int(
                                                                                            self.item_extra_traction_number),
                                                                                        item_id,
                                                                                        self.item_extra_traction_number,
                                                                                        item_meta)

            data = [
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore,
                        "PrimaryAction": {
                            "Command": primary_click_once_commands,
                            "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                            "KeepInventoryOpen": True
                        },
                        "PrimaryShiftAction": {
                            "Command": primary_shift_click_commands,
                            "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                            "KeepInventoryOpen": True
                        },
                        "Requirements": "%economy_balance_{}% >= {}".format(self.currency, item_price * int(
                            self.item_extra_traction_number))
                    },
                    "Item_1": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore_1,
                        "PrimaryAction": {
                            "Command": primary_click_once_commands,
                            "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                            "KeepInventoryOpen": True
                        },
                        "Requirements": "%economy_balance_{}% >= {}".format(self.currency, item_price)
                    },
                    "Item_2": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore_1,
                        "Requirements": "%economy_balance_{}% < {}".format(self.currency, item_price)
                    }
                }
            ]
            self.data['virtualchest']['Slot{}'.format(i)] = data

    def save(self):
        if not path.exists(path.join(os.getcwd(), "shops")):
            os.mkdir(path.join(os.getcwd(), "shops"))
        with open(path.join(os.getcwd(), "shops", self.file_name + '.conf'), mode='w+', encoding='utf-8') as file:
            conf = pyhocon.ConfigFactory.from_dict(self.data)
            file.write(pyhocon.HOCONConverter.to_hocon(conf))


if __name__ == "__main__":
    sp = shop()
    sp.only_buy()
    sp.save()
