# world_map.py - 世界地圖與角色移動模擬

"""
這個檔案模擬了JRPG中簡單的世界地圖和角色在其中移動的邏輯。
它用文字符號來表示地圖，並展示了角色如何與地圖互動。
"""

class WorldMap:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        self.map = [['.' for _ in range(width)] for _ in range(height)]
        self.player_pos = {'x': 0, 'y': 0}
        self.place_feature(5, 3, 'T') # Town
        self.place_feature(15, 7, 'D') # Dungeon
        self.place_feature(10, 5, 'E') # Enemy Area

    def place_feature(self, x, y, symbol):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.map[y][x] = symbol

    def display_map(self):
        print("-" * (self.width + 2))
        for y in range(self.height):
            row_display = ['|']
            for x in range(self.width):
                if x == self.player_pos['x'] and y == self.player_pos['y']:
                    row_display.append('P') # Player
                else:
                    row_display.append(self.map[y][x])
            row_display.append('|')
            print("".join(row_display))
        print("-" * (self.width + 2))

    def move_player(self, dx, dy):
        new_x = self.player_pos['x'] + dx
        new_y = self.player_pos['y'] + dy

        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            self.player_pos['x'] = new_x
            self.player_pos['y'] = new_y
            print(f"玩家移動到 ({new_x}, {new_y})")
            # 檢查是否進入特殊區域
            current_tile = self.map[new_y][new_x]
            if current_tile == 'T':
                print("你進入了一個城鎮！")
            elif current_tile == 'D':
                print("你發現了一個地牢入口！")
            elif current_tile == 'E':
                print("小心！你進入了敵人區域，可能會遭遇戰鬥！")
        else:
            print("移動超出地圖範圍。")

# 簡單的Demo運行
if __name__ == "__main__":
    game_map = WorldMap()
    game_map.display_map()
    game_map.move_player(1, 0)
    game_map.move_player(0, 1)
    game_map.move_player(4, 2) # 移動到城鎮附近
    game_map.display_map()
    game_map.move_player(0, 0) # 進入城鎮
    game_map.display_map()
