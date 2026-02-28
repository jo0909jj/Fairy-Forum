# character_data.py - 角色、物品與技能數據結構

"""
這個檔案定義了JRPG中常見的角色、物品和技能的數據結構。
它展示了我們如何組織遊戲中的各種數據。
"""

# 角色數據
class Character:
    def __init__(self, name, job, hp, mp, atk, defense, magic_atk, magic_def, speed):
        self.name = name
        self.job = job
        self.max_hp = hp
        self.current_hp = hp
        self.max_mp = mp
        self.current_mp = mp
        self.atk = atk
        self.defense = defense
        self.magic_atk = magic_atk
        self.magic_def = magic_def
        self.speed = speed
        self.skills = []
        self.inventory = []
        self.equipment = {'weapon': None, 'armor': None, 'accessory': None}

    def add_skill(self, skill):
        self.skills.append(skill)

    def add_item(self, item):
        self.inventory.append(item)

    def equip_item(self, item):
        if item.item_type in self.equipment:
            # 卸下舊裝備
            if self.equipment[item.item_type]:
                print(f"{self.name} 卸下了 {self.equipment[item.item_type].name}")
            self.equipment[item.item_type] = item
            print(f"{self.name} 裝備了 {item.name}！")
        else:
            print(f"{item.name} 無法裝備。")

    def display_status(self):
        print(f"--- {self.name} ({self.job}) ---")
        print(f"HP: {self.current_hp}/{self.max_hp}")
        print(f"MP: {self.current_mp}/{self.max_mp}")
        print(f"ATK: {self.atk}, DEF: {self.defense}")
        print(f"MAG ATK: {self.magic_atk}, MAG DEF: {self.magic_def}")
        print(f"Speed: {self.speed}")
        print("技能:", ", ".join([s.name for s in self.skills]))
        print("裝備:")
        for slot, item in self.equipment.items():
            print(f"  {slot}: {item.name if item else '無'}")
        print("背包:", ", ".join([i.name for i in self.inventory]))
        print("-" * 20)

# 物品數據
class Item:
    def __init__(self, name, description, item_type='consumable', value=0):
        self.name = name
        self.description = description
        self.item_type = item_type # e.g., 'consumable', 'weapon', 'armor', 'accessory'
        self.value = value

# 技能數據
class Skill:
    def __init__(self, name, description, mp_cost, damage_multiplier=1, effect=None):
        self.name = name
        self.description = description
        self.mp_cost = mp_cost
        self.damage_multiplier = damage_multiplier # 傷害倍率，用於戰鬥計算
        self.effect = effect # 特殊效果，例如 'heal', 'buff', 'debuff'

# 簡單的Demo運行
if __name__ == "__main__":
    # 定義一些技能
    fireball = Skill("火球術", "發射一顆火球攻擊敵人。", 10, damage_multiplier=1.5)
    heal = Skill("治療術", "恢復隊友生命值。", 15, effect='heal')
    slash = Skill("猛烈斬擊", "對單一敵人造成物理傷害。", 5, damage_multiplier=1.2)

    # 定義一些物品
    potion = Item("HP藥水", "恢復50HP。", 'consumable', value=50)
    sword = Item("新手劍", "一把普通的劍。", 'weapon', value=10)
    leather_armor = Item("皮甲", "輕便的皮製護甲。", 'armor', value=5)

    # 創建角色
    hero = Character("亞瑟", "劍士", 100, 30, 15, 10, 5, 5, 8)
    mage = Character("莉莉絲", "法師", 80, 50, 5, 5, 20, 10, 6)

    # 為角色添加技能和物品
    hero.add_skill(slash)
    hero.add_item(potion)
    hero.equip_item(sword)

    mage.add_skill(fireball)
    mage.add_skill(heal)
    mage.add_item(potion)
    mage.equip_item(leather_armor)

    # 顯示角色狀態
    hero.display_status()
    mage.display_status()
