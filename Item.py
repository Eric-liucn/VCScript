import pyhocon


class Item(object):

    def __init__(self):
        self.slot_index = input("请输入格子的编号\n")
        self.item_id = input("请输入要出售的物品ID\n")
        self.item_meta = input("请输入要出售的物品的meta值\n")
        self.item_price = input("请输入要出售的物品的价格\n")
        self.currency = "dollar"
        self.currency_alias = '金币'
        self.item_count = 64
        self.shop_name = 'default_buy_shop'
        self.conf = None

    def gen_item(self):
        buy_count = {
            "Item": {
                "Count": 1,
                "ItemType": self.item_id,
                "UnsafeDamage": int(self.item_meta),
                "ItemLore": [
                    "&a&l出售",
                    "&b左键点击购买 &e1 &b个".format(self.item_count),
                    "&bShift左键点击购买 &e{} &b个".format(self.item_count),
                    "&6价格： &d{} &a{} &d一个".format(self.item_price, self.currency_alias)
                ]
            },
            "PrimaryAction": {
                'Command': """cost: totaleconomy:{}:{};
                              console: give %player_name% {} 1 {};
                              sound: minecraft:block.note.hat""".format(self.currency, self.item_price, self.item_id, self.item_meta),
                'CommandAfter': "console: vc update {} %player%".format(self.shop_name),
                'KeepInventoryOpen': True
            },
            'PrimaryShiftAction': {
                'Command': """cost: totaleconomy:{}:{};
                              console: give %player_name% {} {} {};
                              sound: minecraft:block.note.hat""".format(self.currency,
                                                                        float(self.item_price) * int(self.item_count),
                                                                        self.item_id, self.item_count,
                                                                        self.item_meta),
                'CommandAfter': "console: vc update {} %player%".format(self.shop_name),
                'KeepInventoryOpen': True
            },
            'Requirements': "%economy_balance_{}% >= {}".format(self.currency,
                                                                float(self.item_price) * int(self.item_count))
        }

        buy_one = {
            "Item": {
                "Count": 1,
                "ItemType": self.item_id,
                "UnsafeDamage": int(self.item_meta),
                "ItemLore": [
                    "&a&l出售",
                    "&b左键点击购买 &e1 &b个".format(self.item_count),
                    "&6价格： &d{} &a{} &d一个".format(self.item_price, self.currency_alias)
                ]
            },
            "PrimaryAction": {
                'Command': """cost: totaleconomy:{}:{};
                              console: give %player_name% {} 1 {};
                              sound: minecraft:block.note.hat""".format(self.currency, self.item_price, self.item_id, self.item_meta),
                'CommandAfter': "console: vc update {} %player%".format(self.shop_name),
                'KeepInventoryOpen': True
            },
            'Requirements': "%economy_balance_{}% >= {}".format(self.currency, float(self.item_price))
        }

        buy_none = {
            "Item": {
                "Count": 1,
                "ItemType": self.item_id,
                "UnsafeDamage": int(self.item_meta),
                "ItemLore": [
                    "&a&l出售",
                    "&4你没有足够的钱！",
                    "&6价格： &d{} &a{} &d一个".format(self.item_price, self.currency_alias)
                ]
            },
            'Requirements': "%economy_balance_{}% < {}".format(self.currency, float(self.item_price))
        }
        slot = 'Slot' + self.slot_index
        return {slot: [buy_count, buy_one, buy_none]}

    def print_conf(self):
        self.conf = pyhocon.ConfigFactory.from_dict(self.gen_item())
        with open('file.conf', 'w+', encoding='utf-8') as file:
            file.write(pyhocon.HOCONConverter.to_hocon(self.conf))
            file.close()


if __name__ == "__main__":
    item = Item()
    item.print_conf()
