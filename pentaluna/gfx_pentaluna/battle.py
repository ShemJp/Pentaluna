# battle_scene.py
import pygame
import config
from config import color
from scene import Scene


class BattleScene(Scene):
    def __init__(self):
        super().__init__()

    def show(self):
        self.screen.fill(color.WHITE)
        self.show_gems(self.state_machine._gem_grid)
        self.enemy_gfx(self.state_machine._current_enemy)
        self.party_gfx(self.state_machine._party)

    def status_text(self, message):
        pygame.draw.rect(
            self.screen, color.BLACK, (config.start_x - 35, 10, 490, 55), 5
        )
        self.print_text(f"{message}", config.start_x - 15, 20, color.BLACK)

    def show_gems(self, gem_grid):
        width = config.COLUMNS * 60
        height = config.ROWS * 60

        pygame.draw.rect(
            self.screen,
            color.BLACK,
            (config.start_x - 35, config.start_y - 35, width + 10, height + 10),
            5,
        )
        for col in range(config.COLUMNS):
            self.print_text(
                chr(col + 65),
                config.start_x - 10 + col * 60,
                height + (config.start_y - 20),
                color.BLACK,
            )
        for row in range(config.ROWS):
            self.print_text(
                row + 1,
                config.start_x - 60,
                row * 60 + (config.start_y - 20),
                color.BLACK,
            )

        for col in gem_grid.gems:
            for gem in col:
                if not gem.dropped:
                    gem.drop()
                self.screen.blit(gem.draw(), (gem.x - 30, gem.y - 30))

    def enemy_gfx(self, enemy):
        image_width, image_height = enemy.image.get_size()
        surface = pygame.Surface((image_width + 140, image_height))
        surface.fill(color.WHITE)
        surface.blit(enemy.image, (0, 0))
        pygame.draw.rect(
            surface, enemy.elem["color"], (0, 0, image_width + 140, image_height), 5
        )
        self.print_text(f"{enemy.name}", image_width + 10, 20, color.BLACK, 24, surface)
        self.print_text(
            f"HP : {int(enemy.hp/enemy.max_hp*100)}%",
            image_width + 10,
            60,
            color.BLACK,
            20,
            surface,
        )

        surface.blit(self.elem_chart(80), (image_width+30, image_height-90))

        self.screen.blit(surface, (config.start_x - 35, 85))

    def party_gfx(self, party):
        image_width, image_height = party.leader.image.get_size()
        y_offset = 95
        surface = pygame.Surface((image_width + 180, 680))
        surface.fill(color.WHITE)

        pygame.draw.rect(surface, color.BLACK, (0, 0, image_width + 180, 680), 5)

        self.print_text(f"{party.name}", 20, 10, color.BLACK, 24, surface)
        self.print_text(
            f"HP: {party.hp} / {party.max_hp}", 210, 15, color.BLACK, 15, surface
        )
        self.print_text(f"{party.leader_skill.name}", 20, 45, color.BLACK, 15, surface)
        self.print_text(f"{party.leader_skill.desc}", 20, 70, color.BLACK, 12, surface)

        for ally in party.allies:
            surface.blit(self.draw_member(ally), (25, y_offset))
            y_offset += image_height + 10

        self.screen.blit(surface, (config.COLUMNS * 60 + config.start_x + 20, 10))

    def draw_member(self, ally):
        image_width, image_height = ally.image.get_size()
        portrait = pygame.Surface((image_width + 130, image_height))
        portrait.fill(color.WHITE)
        portrait.blit(ally.image, (0, 0))
        pygame.draw.rect(
            portrait, ally.color, (0, 0, image_width + 130, image_height), 2
        )

        self.print_text(f"{ally.name}", image_width + 5, 10, color.BLACK, 18, portrait)
        self.print_text(
            f"{ally.symbol}", image_width + 45, 50, ally.color, 24, portrait
        )
        self.print_text(
            f"ATK: {ally.attack}", image_width + 40, 95, color.BLACK, 12, portrait
        )
        return portrait
