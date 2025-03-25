import config
import pygame
from elements import Element
from config import color
import sfx


class GemGrid:
    def __init__(self):
        self.height = config.ROWS
        self.width = config.COLUMNS
        self.gems = self.spawn_gems()

    def spawn_gems(self):
        gems = []
        for i in range(self.width):
            gems_in_column = []
            for j in range(self.height):
                gem = Gem(Element.random_elem(), i, j)
                gems_in_column.append(gem)
            gems.append(gems_in_column)
        return gems

    def drop_all(self):
        for col in self.gems:
            for gem in col:
                gem.instant_drop()

    def swap(self, gem, target):
        self.gems[gem.col][gem.row], self.gems[target.col][target.row] = (
            self.gems[target.col][target.row],
            self.gems[gem.col][gem.row],
        )
        a_pos = gem.get_pos()
        b_pos = target.get_pos()

        gem.set_pos(*b_pos)
        target.set_pos(*a_pos)

    def get_neighbours(self, gem, target=None):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbours = []

        for dx, dy in directions:
            new_col, new_row = gem.col + dx, gem.row + dy

            if 0 <= new_col < self.width and 0 <= new_row < self.height:
                neighbours.append(self.gems[new_col][new_row])
            else:
                neighbours.append(None)

        if target:
            return target in neighbours

        return neighbours

    def find_matches(self, gem):
        match_count = 0
        real_matches = set()

        matches = self.cluster_check(gem)
        if len(matches) < 3:
            return match_count

        for gem in matches:
            left_gem, right_gem, up_gem, down_gem = self.get_neighbours(gem)

            if (
                left_gem
                and right_gem
                and not left_gem.matched
                and not right_gem.matched
            ):
                if gem.elem == left_gem.elem == right_gem.elem:
                    real_matches.update({gem, left_gem, right_gem})

            if up_gem and down_gem and not up_gem.matched and not down_gem.matched:
                if gem.elem == up_gem.elem == down_gem.elem:
                    real_matches.update({gem, up_gem, down_gem})

        for gem in real_matches:
            gem.matched = True
            match_count += 1
        return match_count

    def cluster_check(self, gem):
        if gem.matched:
            return []

        matches = []
        visited = set()

        def flood_fill(x, y):
            if (
                (x, y) in visited
                or x < 0
                or x >= len(self.gems)
                or y < 0
                or y >= len(self.gems[0])
            ):
                return
            visited.add((x, y))
            current_gem = self.gems[x][y]
            if current_gem.elem == gem.elem:
                matches.append(current_gem)
                flood_fill(x + 1, y)  # Right
                flood_fill(x - 1, y)  # Left
                flood_fill(x, y + 1)  # Down
                flood_fill(x, y - 1)  # Up

        flood_fill(gem.col, gem.row)
        return matches

    def cascade(self):
        for col in self.gems:
            count = 0
            for gem in col[:]:
                if gem.matched:
                    col.remove(gem)
                    count += 1

        for col_index, col in enumerate(self.gems):
            needed_gems = self.height - len(col)

            for row_index, gem in enumerate(col):
                new_row = row_index + needed_gems
                gem.set_to_drop(new_row)

            for j in range(needed_gems):
                gem = Gem(Element.random_elem(), col_index, needed_gems - (j + 1))
                col.insert(0, gem)

        return


class Gem:
    _choice = None

    def __init__(self, elem, col, row):
        self.elem = elem
        self.col = col
        self.row = row
        self.x = col * 60 + config.start_x
        self.final_y = config.start_y + 60 * row
        self.y = self.final_y + config.offscreen_y
        self.color = elem["color"]
        self.symbol = elem["symbol"]
        self.dropped = False
        self.matched = False
        self.shake = False
        self.flash = 0

    def set_to_drop(self, row):
        self.row = row
        self.final_y = config.start_y + 60 * row
        self.dropped = False

    def draw(self):
        surface = pygame.Surface((60, 60), pygame.SRCALPHA)

        if Gem._choice is self or self.matched:
            surface.blit(sfx.draw_glow(30,self.color),(0,0))
            pygame.draw.circle(surface, self.color + (200,), (30, 30), 20)
        else:        
            pygame.draw.circle(surface, self.color, (30, 30), 20)

        sfx.flash(self)

        font = pygame.font.SysFont("Meiryo", 20)
        text = font.render(f"{self.symbol}", True, color.WHITE)
        surface.blit(text, (20, 15))

        return surface

    def drop(self):
        if not self.dropped:
            if self.y < self.final_y:
                speed = max(10, (self.final_y - self.y) / 2)
                self.y += speed
                if self.y > self.final_y:
                    self.y = self.final_y
            else:
                self.dropped = True

    def instant_drop(self):
        self.dropped = True
        self.y = self.final_y
        self.dropped = True

    def is_clicked(self, mouse_x, mouse_y):
        gem_radius = 20
        distance = (mouse_x - self.x) ** 2 + (mouse_y - self.y) ** 2
        return distance <= gem_radius**2

    def get_pos(self):
        return self.col, self.row

    def set_pos(self, col, row):
        self.row = row
        self.col = col
        self.x = self.col * 60 + config.start_x
        self.y = config.start_y + 60 * self.row
        return

    def set_choice(self):
        Gem._choice = self

    def clear_choice(self):
        Gem._choice = None

    @classmethod
    def get_choice(cls):
        return cls._choice
