from elements import Element
import loaders
from monster import Enemy


class DungeonList:
    def __init__(self):
        self.list = []
        self.prep_dungeons()
        self.current_dungeon = None

    def prep_dungeons(self):
        enemy_list = loaders.load_json_file("enemies")
        enemies=[]
        for i, e in enumerate(enemy_list):
            enemies.append(Enemy(**enemy_list[e]))
            enemies[i].image = loaders.load_image(
                "enemies", e, True, 350
            )

        dungeon_list = loaders.load_json_file("dungeons")
        for i, d in enumerate(dungeon_list):
            self.list.append(Dungeon(**dungeon_list[d]))
            self.list[i].image = loaders.load_image("dungeons", d)
            self.list[i].image_tb = loaders.load_image("dungeons", d, True, 240)
            for e in self.list[i].enemy_list:
                self.list[i].enemies.append(enemies[int(e)-1])


class Dungeon:
    def __init__(self, name, enemy_list, elem_name):
        self.name = name
        self.elem = Element.get_element(elem_name)
        self.color = self.elem["color"]
        self.floor = 0
        self.enemy_list=enemy_list
        self.enemies = []
        self.image = None
        self.image_tb = None

    def is_clicked(self, mouse_x, mouse_y, x_offset, y_offset):
        dungeon_width, dungeon_height = self.image_tb.get_size()
        left, top = (50 + x_offset, 30 + y_offset)

        if (
            left <= mouse_x <= left + dungeon_width
            and top <= mouse_y <= top + dungeon_height
        ):
            return True
        return False
