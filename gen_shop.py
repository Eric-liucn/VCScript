import pyhocon
import os
from os import path


def is_float_number(string: str):
    try:
        float(string)
        return True
    except TypeError:
        return False


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
        self.item_extra_traction_number = 64

        self.currency = input("请输入该商店使用的货币：\n")
        if self.currency == '' or self.currency is None:
            self.currency = input("输入有误，请输入该商店使用的货币：\n")
        self.currency_alias = input("请输入该种货币的别名：\n")
        if self.currency_alias == '' or self.currency_alias is None:
            self.currency_alias = input("输入有误，请重新输入商店使用货币的别名：\n")
        self.eco_plugin = 'economylite'

        self.rows = 6
        self.update_tick = 10
        self.accept_tick = 20
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

        if int(self.shop_mode) == 3:
            self.different_price = bool(input("同时出售/收购时价格是否不同？\n"))
        else:
            self.different_price = 0

        self.data = {
            'virtualchest': {
                'TextTitle': self.shop_title,
                'Rows': self.rows,
                'AcceptableActionIntervalTick': self.accept_tick,
                'UpdateIntervalTick': self.update_tick
            }
        }

    def is_valid_item_id(self, item_str: str):
        strings = item_str.split(":")
        if self.different_price:
            if not len(strings) == 5:
                return False
            if not is_float_number(strings[4]) or float(strings[4]) < 0:
                return False
        else:
            if not len(strings) == 4:
                return False
        if not is_float_number(strings[2]):
            return False
        if not is_float_number(strings[3]) or float(strings[3]) < 0:
            return False
        return True

    def only_buy(self):
        for i in range(45):
            item = input("请输入第{}个商品文本：\n".format(i))
            while not self.is_valid_item_id(item):
                item = input("请输入第{}个商品文本：\n".format(i))
            strings = item.split(":")
            item_id = strings[0] + ":" + strings[1]
            item_meta = int(strings[2])
            item_price = float(strings[3])

            if self.different_price is not None and self.different_price:
                item_sell_price = float(strings[4])
            else:
                item_sell_price = item_price

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

            buy_data = [
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore,
                    },
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
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore_1
                    },
                    "PrimaryAction": {
                        "Command": primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True
                    },
                    "Requirements": "%economy_balance_{}% >= {}".format(self.currency, item_price)
                },
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_lore_2
                    },
                    "Requirements": "%economy_balance_{}% < {}".format(self.currency, item_price)
                }
            ]

            item_sell_lore = [
                "&a&l收购",
                "&b左键点击一次出售 &e1 &b个",
                "&b左键Shift点击批量出售",
                "&6价格：&d{}&a{}&d一个".format(item_sell_price, self.currency_alias)
            ]
            sell_primary_click_once_commands = """cost-item:1;
                       cost: {}:{}:-{};
                       sound: minecraft:block.note.hat""".format(self.eco_plugin, self.currency, item_sell_price)

            sell_primary_shift_click_commands = """cost-item:{};
                       cost: {}:{}:-{};
                       sound: minecraft:block.note.hat""".format(9,
                                                                 self.eco_plugin,
                                                                 self.currency,
                                                                 item_sell_price * 9)

            sell_held_item_one = {
                "SearchInventory": True,
                "ItemType": item_id,
                "Count": 1,
                "UnsafeDamage": item_meta
            }

            sell_held_item_all = {
                "RepetitionUpperLimit": 256,
                "SearchInventory": True,
                "ItemType": item_id,
                "Count": 9,
                "UnsafeDamage": item_meta
            }

            sell_data = [
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_sell_lore
                    },
                    "PrimaryAction": {
                        "Command": sell_primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_one
                    },
                    "PrimaryShiftAction": {
                        "Command": sell_primary_shift_click_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_all
                    },
                }
            ]

            item_sell_and_buy_lore = [
                "&a出售",
                "&b左键点击一次购买 &e1 &b个",
                "&b左键Shift点击一次购买 &e{} &b个".format(self.item_extra_traction_number),
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias),
                "&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-",
                "&d收购",
                "&b右键点击一次出售 &e1 &b个",
                "&b右键Shift点击批量出售",
                "&6价格：&d{}&a{}&d一个".format(item_sell_price, self.currency_alias)
            ]

            item_sell_and_buy_lore_1 = [
                "&a出售",
                "&b左键点击一次购买 &e1 &b个",
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias),
                "&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-",
                "&d收购",
                "&b右键点击一次出售 &e1 &b个",
                "&b右键Shift点击批量出售",
                "&6价格：&d{}&a{}&d一个".format(item_sell_price, self.currency_alias)
            ]

            item_sell_and_buy_lore_2 = [
                "&a出售",
                "&4你没有足够的钱",
                "&6价格：&d{}&a{}&d一个".format(item_price, self.currency_alias),
                "&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-&2-&d-&e-&c-&b-&6-",
                "&d收购",
                "&b右键点击一次出售 &e1 &b个",
                "&b右键Shift点击批量出售",
                "&6价格：&d{}&a{}&d一个".format(item_sell_price, self.currency_alias)
            ]

            buy_and_sell_data = [
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_sell_and_buy_lore
                    },
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
                    "SecondaryAction": {
                        "Command": sell_primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_one
                    },
                    "SecondaryShiftAction": {
                        "Command": sell_primary_shift_click_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_all
                    },
                    "Requirements": "%economy_balance_{}% >= {}".format(self.currency, item_price * int(
                        self.item_extra_traction_number))
                },
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_sell_and_buy_lore_1
                    },
                    "PrimaryAction": {
                        "Command": primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True
                    },
                    "SecondaryAction": {
                        "Command": sell_primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_one
                    },
                    "SecondaryShiftAction": {
                        "Command": sell_primary_shift_click_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_all
                    },
                    "Requirements": "%economy_balance_{}% >= {}".format(self.currency, item_price)
                },
                {
                    "Item": {
                        "ItemType": item_id,
                        "UnsafeDamage": int(item_meta),
                        "Count": 1,
                        "ItemLore": item_sell_and_buy_lore_2
                    },
                    "SecondaryAction": {
                        "Command": sell_primary_click_once_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_one
                    },
                    "SecondaryShiftAction": {
                        "Command": sell_primary_shift_click_commands,
                        "CommandAfter": "console: vc update {} %player%".format(self.file_name),
                        "KeepInventoryOpen": True,
                        "HandheldItem": sell_held_item_all
                    },
                    "Requirements": "%economy_balance_{}% < {}".format(self.currency, item_price)
                }

            ]

            if int(self.shop_mode) == 1:
                self.data['virtualchest']['Slot{}'.format(i)] = buy_data
            elif int(self.shop_mode) == 2:
                self.data['virtualchest']['Slot{}'.format(i)] = sell_data
            elif int(self.shop_mode) == 3:
                self.data['virtualchest']['Slot{}'.format(i)] = buy_and_sell_data

    def add_decorate(self):
        for i in [45, 46, 47, 51, 52, 53]:
            decorate = \
                [
                    {
                        "Item": {
                            "Count": 1,
                            "ItemType": "minecraft:stained_glass_pane",
                            "UnsafeDamage": 2,
                            "DisplayName": ""
                        },
                        "Requirements": "tick % 40 <= 20"
                    },
                    {
                        "Item": {
                            "Count": 1,
                            "ItemType": "minecraft:stained_glass_pane",
                            "UnsafeDamage": 5,
                            "DisplayName": ""
                        },
                        "Requirements": "tick % 40 > 20"
                    }
                ]

            self.data['virtualchest']['Slot{}'.format(i)] = decorate

        last_page = {
            "Item":
                {
                    "Count": 1,
                    "ItemType": "minecraft:chest",
                    "UnsafeDamage": 0,
                    "DisplayName": "&a上一页"
                }
        }

        if int(self.this_page) == 1:
            last_page["Item"]["DisplayName"] = "&4没有上一页了"
        else:
            last_page["PrimaryAction"] = {
                "Command": """vc open {};
                              sound:minecraft:ui.button.click""".format(self.file_name + "_" +
                                                                        str((int(self.this_page) - 1))),
                "KeepInventoryOpen": True
            }
        self.data['virtualchest']['Slot48'] = last_page

        current_page = {
            "Item":
                {
                    "Count": 1,
                    "ItemType": "minecraft:paper",
                    "UnsafeDamage": 0,
                    "DisplayName": "&a当前页面：&e&l{}&f/&d{}".format(int(self.this_page), int(self.total_page))
                }
        }

        self.data['virtualchest']['Slot49'] = current_page

        next_page = {
            "Item":
                {
                    "Count": 1,
                    "ItemType": "minecraft:chest",
                    "UnsafeDamage": 0,
                    "DisplayName": "&a下一页"
                }
        }

        if int(self.this_page) == int(self.total_page):
            next_page["Item"]["DisplayName"] = "&4没有下一页了"
        else:
            next_page["PrimaryAction"] = {
                "Command": """vc open {};
                              sound:minecraft:ui.button.click""".format(self.file_name + "_" +
                                                                        str((int(self.this_page) + 1))),
                "KeepInventoryOpen": True
            }
        self.data['virtualchest']['Slot50'] = next_page

    def save(self):
        if not path.exists(path.join(os.getcwd(), "shops")):
            os.mkdir(path.join(os.getcwd(), "shops"))
        with open(path.join(os.getcwd(), "shops", self.file_name + '_' + str(self.this_page) + '.conf'), mode='w+',
                  encoding='utf-8') as file:
            conf = pyhocon.ConfigFactory.from_dict(self.data)
            file.write(pyhocon.HOCONConverter.to_hocon(conf))


if __name__ == "__main__":
    sp = shop()
    sp.only_buy()
    sp.add_decorate()
    sp.save()
