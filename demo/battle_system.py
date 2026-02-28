# battle_system.py - 回合制戰鬥模擬

"""
這個檔案模擬了JRPG中回合制戰鬥的基本流程。
它展示了角色如何進行攻擊、使用技能和物品。
"""

import random
from character_data import Character, Item, Skill

class Battle:
    def __init__(self, party, enemies):
        self.party = party
        self.enemies = enemies
        self.turn_order = []
        self.current_turn_index = 0

    def initialize_turn_order(self):
        # 根據速度決定行動順序
        all_combatants = self.party + self.enemies
        self.turn_order = sorted(all_combatants, key=lambda c: c.speed, reverse=True)
        print("--- 戰鬥開始！ ---")
        print("行動順序:", ", ".join([c.name for c in self.turn_order]))

    def is_game_over(self):
        # 判斷我方隊伍是否全滅
        if all(char.current_hp <= 0 for char in self.party):
            return True, "遊戲結束，你失敗了！"
        # 判斷敵人是否全滅
        if all(enemy.current_hp <= 0 for enemy in self.enemies):
            return True, "戰鬥勝利！"
        return False, None

    def display_battle_status(self):
        print("\n--- 戰場狀態 ---")
        print("我方隊伍:")
        for char in self.party:
            status = f"{char.name} (HP: {max(0, char.current_hp)}/{char.max_hp}, MP: {max(0, char.current_mp)}/{char.max_mp})"
            if char.current_hp <= 0:
                status += " [已陣亡]"
            print(f"- {status}")
        print("敵人:")
        for enemy in self.enemies:
            status = f"{enemy.name} (HP: {max(0, enemy.current_hp)}/{enemy.max_hp})"
            if enemy.current_hp <= 0:
                status += " [已擊敗]"
            print(f"- {status}")
        print("------------------")

    def get_target(self, attacker, targets):
        # 簡單的目標選擇邏輯，敵人隨機攻擊，玩家選擇第一個敵人
        if attacker in self.party: # 玩家角色
            # 這裡可以加入更複雜的玩家選擇邏輯，目前簡化為選擇第一個活著的敵人
            for i, target in enumerate(targets):
                if target.current_hp > 0:
                    print(f"選擇目標: {i+1}. {target.name}")
            while True:
                try:
                    choice = 1 # input("請選擇目標 (輸入數字): ")
                    target_index = int(choice) - 1
                    if 0 <= target_index < len(targets) and targets[target_index].current_hp > 0:
                        return targets[target_index]
                    else:
                        print("無效的目標選擇。")
                except ValueError:
                    print("請輸入有效數字。")
        else: # 敵方角色
            # 敵人隨機選擇一個活著的我方角色
            living_party = [char for char in self.party if char.current_hp > 0]
            if living_party:
                return random.choice(living_party)
            return None # 無目標可攻擊

    def calculate_damage(self, attacker, target, skill=None):
        base_damage = attacker.atk
        if skill:
            if skill.damage_multiplier:
                base_damage *= skill.damage_multiplier
            if skill.effect == 'heal':
                return -skill.value # 負傷害表示治療
            # 可以加入魔法攻擊計算
        
        # 簡單的傷害減免
        damage = max(0, int(base_damage - target.defense / 2))
        return damage

    def apply_damage(self, target, damage):
        target.current_hp -= damage
        if target.current_hp < 0:
            target.current_hp = 0
        if target.current_hp == 0:
            print(f"{target.name} 已陣亡！")

    def handle_turn(self, combatant):
        if combatant.current_hp <= 0:
            return # 已陣亡的角色無法行動

        print(f"\n--- {combatant.name} 的回合 ({combatant.job if hasattr(combatant, 'job') else '敵人'}) ---")

        if combatant in self.party: # 我方角色行動
            # 玩家行動選項：攻擊、技能、物品
            print("請選擇行動：1. 攻擊 2. 技能 3. 物品")
            action_choice = "1" # input("輸入數字選擇行動: ") # 簡化為直接攻擊

            if action_choice == "1": # 攻擊
                target = self.get_target(combatant, self.enemies)
                if target:
                    damage = self.calculate_damage(combatant, target)
                    self.apply_damage(target, damage)
                    print(f"{combatant.name} 攻擊了 {target.name}，造成 {damage} 點傷害！")
            elif action_choice == "2" and combatant.skills: # 技能
                print("選擇技能:")
                for i, skill in enumerate(combatant.skills):
                    print(f"{i+1}. {skill.name} (消耗MP: {skill.mp_cost})")
                skill_choice = "1" # input("輸入數字選擇技能: ")
                try:
                    skill_index = int(skill_choice) - 1
                    chosen_skill = combatant.skills[skill_index]
                    if combatant.current_mp >= chosen_skill.mp_cost:
                        combatant.current_mp -= chosen_skill.mp_cost
                        target = self.get_target(combatant, self.enemies)
                        if target:
                            damage = self.calculate_damage(combatant, target, chosen_skill)
                            if chosen_skill.effect == 'heal':
                                target.current_hp -= damage # 負傷害轉為治療
                                target.current_hp = min(target.max_hp, target.current_hp)
                                print(f"{combatant.name} 對 {target.name} 施放 {chosen_skill.name}，恢復 {abs(damage)} 點生命值！")
                            else:
                                self.apply_damage(target, damage)
                                print(f"{combatant.name} 對 {target.name} 施放 {chosen_skill.name}，造成 {damage} 點傷害！")
                    else:
                        print("MP不足！")
                except (ValueError, IndexError):
                    print("無效的技能選擇。")
            elif action_choice == "3" and combatant.inventory: # 物品
                print("選擇物品:")
                for i, item in enumerate(combatant.inventory):
                    print(f"{i+1}. {item.name}")
                item_choice = "1" # input("輸入數字選擇物品: ")
                try:
                    item_index = int(item_choice) - 1
                    chosen_item = combatant.inventory[item_index]
                    if chosen_item.item_type == 'consumable':
                        # 簡化為藥水恢復HP
                        if chosen_item.name == "HP藥水":
                            heal_amount = chosen_item.value
                            combatant.current_hp += heal_amount
                            combatant.current_hp = min(combatant.max_hp, combatant.current_hp)
                            print(f"{combatant.name} 使用了 {chosen_item.name}，恢復 {heal_amount} 點生命值！")
                            combatant.inventory.pop(item_index) # 消耗物品
                    else:
                        print("此物品無法在戰鬥中使用。")
                except (ValueError, IndexError):
                    print("無效的物品選擇。")
            else:
                print("無效的行動選擇，自動進行攻擊。")
                target = self.get_target(combatant, self.enemies)
                if target:
                    damage = self.calculate_damage(combatant, target)
                    self.apply_damage(target, damage)
                    print(f"{combatant.name} 攻擊了 {target.name}，造成 {damage} 點傷害！")

        else: # 敵方角色行動 (簡化為隨機攻擊我方一個角色)
            target = self.get_target(combatant, self.party)
            if target:
                damage = self.calculate_damage(combatant, target)
                self.apply_damage(target, damage)
                print(f"{combatant.name} 攻擊了 {target.name}，造成 {damage} 點傷害！")

    def start_battle(self):
        self.initialize_turn_order()
        
        while True:
            self.display_battle_status()
            game_over, message = self.is_game_over()
            if game_over:
                print(message)
                break

            combatant = self.turn_order[self.current_turn_index]
            self.handle_turn(combatant)

            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)
            # 過濾掉已陣亡的角色，重新建立行動順序
            self.turn_order = [c for c in self.turn_order if c.current_hp > 0]
            if not self.turn_order: # 所有人都陣亡，戰鬥結束
                break

# 簡單的Demo運行
if __name__ == "__main__":
    # 定義技能和物品 (從 character_data 載入)
    fireball = Skill("火球術", "發射一顆火球攻擊敵人。", 10, damage_multiplier=1.5)
    heal = Skill("治療術", "恢復隊友生命值。", 15, effect='heal', value=30)
    slash = Skill("猛烈斬擊", "對單一敵人造成物理傷害。", 5, damage_multiplier=1.2)
    potion = Item("HP藥水", "恢復50HP。", 'consumable', value=50)

    # 創建我方角色
    hero = Character("亞瑟", "劍士", 100, 30, 15, 10, 5, 5, 8)
    mage = Character("莉莉絲", "法師", 80, 50, 5, 5, 20, 10, 6)

    hero.add_skill(slash)
    hero.add_item(potion)
    mage.add_skill(fireball)
    mage.add_skill(heal)
    mage.add_item(potion)

    # 創建敵人
    goblin = Character("哥布林", "敵人", 40, 0, 8, 3, 0, 0, 5)
    wolf = Character("野狼", "敵人", 30, 0, 10, 2, 0, 0, 7)

    # 開始戰鬥
    # 由於這裡無法實現用戶輸入，我們將會簡化戰鬥流程
    # 在實際運行時，可以手動修改 `action_choice` 或 `input()` 的模擬
    battle = Battle([hero, mage], [goblin, wolf])
    # battle.start_battle() # 由於自動化運行無法模擬用戶輸入，這裡不直接調用
    # 如果要手動測試，請將上方 `input()` 註釋解除，或修改為固定選項
    print("\n若要運行戰鬥Demo，請手動執行此檔案，並解除`input()`的註釋，或模擬輸入。")
    print("目前為了自動化演示，將不會實際運行 `battle.start_battle()`。")
    print("你可以想像：亞瑟揮舞著劍，莉莉絲施放火球術！哥布林和野狼也咆哮著反擊！")
