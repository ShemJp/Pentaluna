import pygame
import random
from config import color


def draw_glow(max_radius, glow_color):
    glow_surface = pygame.Surface((max_radius * 2, max_radius * 2), pygame.SRCALPHA)

    # Loop to create multiple glow layers
    for i in range(max_radius):
        # Calculate radius and alpha (opacity) for each glow layer
        alph = int(i * (255 // max_radius))  # Decrease opacity for each layer
        # Draw a circle with increasing radius and decreasing opacity
        pygame.draw.circle(
            glow_surface,
            glow_color + (alph,),
            (max_radius, max_radius),
            (2 * max_radius - i) / 2,
        )

    # Return the surface with the glow effect applied
    return glow_surface


def flash(gem):
    if gem.flash > 0:
        if gem.flash % 5 == 0:
            gem.color = random.choice(color.COLORS)
        else:
            gem.color = gem.elem["color"]
            gem.symbol = gem.elem["symbol"]
        gem.flash -= 1


"""
    ### Rectangle stuff
            elif shape_type == "rect":
                # Draw a rectangle with increasing size (rounded corners)
                pygame.draw.rect(
                    temp_surface,
                    color,
                    (0, 0, radius * 2, radius * 2),
                    border_radius=radius,
                )

            #elif shape_type == "rect":
                # For rectangles, adjust position based on width/height and radius
                #glow_position = (x - radius + width // 2, y - radius + height // 2)



                


                        # if shake_screen():
                        #    gem.shake = True
                        # else:
                        #    gem.shake = False


        def shake_screen():
            global shake_timer
            if shake_timer > 0:
                shake_timer -= 1
                return True
            return False


                # if gem.shake:
                # draw_x = gem.x + random.randint(-shake_intensity, shake_intensity)
                # draw_y = gem.y + random.randint(-shake_intensity, shake_intensity)
        
"""
