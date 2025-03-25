import pygame
from scene import Scene
from config import color

class DungeonSelect(Scene):
    def __init__(self):
        super().__init__()
        
        
    def show(self):

        self.screen.fill(color.WHITE)
        width, height = self.state_machine._dungeon_list.list[0].image_tb.get_size()
        offsets = [
            (0, 0),
            (50 + width, 0),
            (100 + width * 2, 0),
            (0, height + 60),
            (50 + width, height + 60),
            (100 + width * 2, height + 60),
            (50 + width, height * 2 + 120),
        ]
        for i, dungeon in enumerate(self.state_machine._dungeon_list.list):
            x_offset, y_offset = offsets[i]
            self.screen.blit(self.dungeon_gfx(dungeon), (50 + x_offset, 30 + y_offset))



    def dungeon_gfx(self, dungeon):
        image_width, image_height = dungeon.image_tb.get_size()
        frame = pygame.Surface((image_width, image_height + 45))
        frame.fill(color.WHITE)
        frame.blit(dungeon.image_tb, (0, 0))
        pygame.draw.rect(
            frame, dungeon.color, (0, 0, image_width, image_height + 45), 2
        )

        self.print_text(
            f"{dungeon.name}", 60, image_height + 10, color.BLACK, 20, frame
        )
        self.print_text(
            f"{dungeon.elem['symbol']}", 20, image_height + 10, dungeon.color, 20, frame
        )
        self.print_text(
            f"{dungeon.elem['symbol']}",
            image_width - 40,
            image_height + 10,
            dungeon.color,
            20,
            frame,
        )
        return frame