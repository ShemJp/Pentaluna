import pygame

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen = pygame.display.set_mode((800, 600))

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Kanji characters to display
kanji_text = "火水木金土"  # "Fire Water Wood Gold Earth" in Kanji

# List of font names to display the text in
font_names = [
    "Meiryo", "MS Gothic", "Yu Gothic", "Hiragino Kaku Gothic Pro", 
    "Kozuka Gothic Pro", "Noto Sans CJK JP", "Takao Gothic", 
    "IPA Gothic", "Source Han Sans", "FutoGoB101 Pro"
]

# Starting position to display fonts
y_position = 50

# Render the fonts and display them
for font_name in font_names:
    try:
        font = pygame.font.SysFont(font_name, 40)  # 40px size for visibility
        text_surface = font.render(kanji_text, True, WHITE)  # Render the text in white
        screen.fill(BLACK)  # Clear screen and set background to black
        screen.blit(text_surface, (100, y_position))  # Draw the text on the screen
        
        # Update the display to show the rendered text
        pygame.display.flip()

        # Wait for a short time to allow seeing the output
        pygame.time.delay(1000)  # 1 second delay for each font

        # Increment the position for the next font rendering
        y_position += 60

    except Exception as e:
        print(f"Error with font {font_name}: {e}")

# Close pygame when the loop ends
pygame.quit()