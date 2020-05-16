import pyhocon
import os


class button(object):

    def __init__(self):
        self.slot_index = input("Slot index\n")
        self.item_id = input("Item ID\n")
        self.meta = input("Meta\n")
        self.display_name = input("Display Name\n")
        self.lore = input("Lore (Use // to split)\n")
        self.commands = input("Commands (Use // to split)\n")
        self.keep_inv = input("Keep inv ?\n")

    def gen(self):
        commands = self.commands.split("//")
        cmd = """"""
        for command in commands:
            if not command.endswith(";"):
                cmd += (command + ';')
            else:
                cmd += command
        data = {
            "Slot{}".format(self.slot_index):
                {
                    "Item":
                        {
                            "Count": 1,
                            "ItemType": self.item_id,
                            "UnsafeDamage": int(self.meta),
                            "DisplayName": self.display_name,
                            "ItemLore": self.lore.split("//")
                        },
                    "PrimaryAction":
                        {
                            "Command": cmd,
                            "KeepInventoryOpen": bool(self.keep_inv)
                        }
                }
        }
        return data


if __name__ == "__main__":
    new_button = button()
    conf = pyhocon.ConfigFactory.from_dict(new_button.gen())
    if os.path.exists(os.path.join(os.getcwd(), "gen_command_button")):
        os.mkdir(os.path.join(os.getcwd(), 'gen_command_button'))
    with open(os.path.join(os.getcwd(), 'gen_command_button', "button.conf"), "w+", encoding='utf-8') as file:
        file.write(pyhocon.HOCONConverter.to_hocon(conf))
