from scene import Scene
from config import color
import config
import pygame

class PartySelect(Scene):
    def __init__(self):
        super().__init__()

    def show(self):
        self.screen.fill(color.WHITE)  # Use white for the background to keep it clean
        
        self.screen.blit(self.elem_chart(150),(config.WIDTH-250,100))

        # Background with gradient effect
        self.draw_background()

        # Title Section with color
        self.draw_title()

        # Name input section with color
        self.draw_name_input()

        # Display player name with color
        self.draw_player_name(self.state_machine._name)


    def draw_background(self):
        pygame.draw.rect(self.screen, color.STEEL, (50, 50, config.WIDTH-100, config.HEIGHT-100), 5)

    def draw_title(self):
        """Draws the title for the scene."""
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Party Selection", True, color.BLACK)  # Use purple for the title
        title_rect = title_text.get_rect(center=(400, 100))
        self.screen.blit(title_text, title_rect)

    def draw_name_input(self):
        """Draws the input prompt for the user to enter their name."""
        input_rect = pygame.Rect(200, 200, 400, 50)
        pygame.draw.rect(self.screen, color.WHITE, input_rect)  # Use yellow for the input field background
        pygame.draw.rect(self.screen, color.BLACK, input_rect, 2)  # Black border around the input field
        self.print_text("Enter your name:", 300, 215, color.BLACK, 24)

    def draw_player_name(self, player_name):
        """Displays the current player's name."""
        name_font = pygame.font.Font(None, 36)
        name_text = name_font.render(f"Name: {player_name}", True, color.BLUE)  # Use blue for the player name
        name_rect = name_text.get_rect(center=(400, 300))
        self.screen.blit(name_text, name_rect)