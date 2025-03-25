from scene import Scene
import loaders
import config
from config import color


class MainMenu(Scene):
    def __init__(self):
        super().__init__()
        
    def show(self):
        self.screen.fill(color.WHITE)
        image = loaders.load_image("intro", "splash")
        self.screen.blit(image, (0, 0))
        self.print_text(
            "Press SPACE to continue",
            config.WIDTH / 3,
            config.HEIGHT * 0.9,
            color.HIGHLIGHT,
            30,
        )



