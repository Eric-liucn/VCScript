import pyhocon
import os
from command_button import button
from decorate import decorate


class main(object):

    def __init__(self):
        if not os.path.exists(os.path.join(os.getcwd(), 'gen')):
            os.mkdir(os.path.join(os.getcwd(), 'gen'))
        self.file_name = input("菜单文件名称:\n")
        self.file_path = os.path.join(os.getcwd(), 'gen', self.file_name + '.conf')
        self.title = input("菜单标题:\n")
        self.rows = int(input("菜单行数:\n"))
        trigger = bool(input("是否需要触发器？（不需要直接回车）\n"))
        if trigger:
            self.trigger_item_id = input("触发器物品id:\n")
            self.trigger_by_primary = bool(input("能够左键触发？（不需要直接回车）\n"))
            self.trigger_by_secondary = bool(input("能够右键触发？（不需要直接回车）\n"))
        self.update_tick = 10  # int(input("菜单刷新Tick？（整数）\n"))
        self.accept_tick = 20  # int(input("菜单点击间隔Tick？（整数）\n"))
        if trigger:
            self.main_data = {
                'virtualchest': {
                    'TextTitle': self.title,
                    'Rows': self.rows,
                    'TriggerItem': {
                        'ItemType': self.trigger_item_id,
                        'EnablePrimaryAction': self.trigger_by_primary,
                        'TriggerItem.EnableSecondaryAction': self.trigger_by_secondary
                    },
                    'AcceptableActionIntervalTick': self.accept_tick,
                    'UpdateIntervalTick': self.update_tick
                }
            }
        else:
            self.main_data = {
                'virtualchest': {
                    'TextTitle': self.title,
                    'Rows': self.rows,
                    'AcceptableActionIntervalTick': self.accept_tick,
                    'UpdateIntervalTick': self.update_tick
                }
            }

    def add_cmd_button(self):
        while input("添加指令按钮？\n"):
            b = button()
            self.main_data['virtualchest'][list(b.gen().keys())[0]] = b.gen().get(list(b.gen().keys())[0])

    def add_decorate(self):
        de = decorate()
        de.gen()
        for key in list(de.conf_data.keys()):
            self.main_data['virtualchest'][key] = de.conf_data.get(key)

    def save(self):
        conf = pyhocon.ConfigFactory.from_dict(self.main_data)
        with open(self.file_path, 'w+', encoding='utf-8') as file:
            file.write(pyhocon.HOCONConverter.to_hocon(conf))


if __name__ == '__main__':
    menu = main()
    menu.add_cmd_button()
    menu.add_decorate()
    menu.save()
