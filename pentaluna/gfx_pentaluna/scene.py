import pygame
from config import color
import config
from state_machine import StateMachine
import math
from elements import Element


class Scene:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        self.state_machine = StateMachine.get_instance()
        self.load = True

    def print_text(self, word, x, y, text_color, size=20, surface=None):
        if not surface:
            surface = self.screen
        font = pygame.font.SysFont("Meiryo", size)
        text = font.render(f"{word}", True, text_color)
        return surface.blit(text, (x, y))

    def show(self):
        self.screen.fill(color.white)

    def status_text(self, message):
        message = message
        pass

    def fade(self, duration, fade_in=False, fade_color=color.BLACK):
        fade_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        delay = 20
        steps = int(duration / delay)
        for step in range(steps):
            alpha = (step / steps) * 255
            if fade_in:
                alpha = 255 - alpha
            pygame.draw.rect(
                fade_surface, fade_color + (alpha,), (0, 0, *self.screen.get_size())
            )
            self.show()
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(delay)

        self.screen.blit(fade_surface, (0, 0))
        pygame.display.update()

    def elem_chart(self, size):
        def draw_arrow(surface, start, end, size):
            length = int(size / 15)
            width = int(size / 50)
            # Calculate direction vector from start to end
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            distance = math.hypot(dx, dy)

            # Normalize the direction vector to ensure the arrowhead is placed at the circle edge
            dx /= distance
            dy /= distance

            # Adjust the end point so it's exactly at the circle edge
            adjusted_end = (end[0] - dx * circle_radius, end[1] - dy * circle_radius)

            # Draw the line
            pygame.draw.line(surface, color.BLACK, start, adjusted_end, width)

            # Calculate the arrowhead position (at the end of the line)
            angle = math.atan2(dy, dx)
            arrow_angle = math.pi / 10
            arrow_x = adjusted_end[0]
            arrow_y = adjusted_end[1]

            # Draw the arrowhead
            pygame.draw.polygon(
                surface,
                color.BLACK,
                [
                    (arrow_x, arrow_y),
                    (
                        arrow_x - length * math.cos(angle - arrow_angle),
                        arrow_y - length * math.sin(angle - arrow_angle),
                    ),
                    (
                        arrow_x - length * math.cos(angle + arrow_angle),
                        arrow_y - length * math.sin(angle + arrow_angle),
                    ),
                ],
            )

        # Function to calculate the position of each point
        def get_pentagon_points(center, radius, num_points):
            points = []
            angle_step = 2 * math.pi / num_points
            for i in range(num_points):
                angle = (
                    angle_step * i - math.pi / 2
                )  # Offset by -90 degrees to start at the top
                x = center[0] + radius * math.cos(angle)
                y = center[1] + radius * math.sin(angle)
                points.append((x, y))
            return points

        surface = pygame.Surface((size, size))
        surface.fill(color.WHITE)
        # Constants for the pentagon
        center = (size * 0.5, size * 0.5)
        radius = size * 0.35  # Radius of the pentagon
        circle_radius = size * 0.15  # Radius of the circles at the points
        no_points = 5  # Number of points on the pentagon

        points = get_pentagon_points(center, radius, no_points)

        # Draw the circles at the points of the pentagon with custom colors
        for i in range(no_points):
            draw_arrow(
                surface,
                points[i],
                points[(i + 2) % no_points],
                size
            )
        for i, point in enumerate(points):
            x = int(point[0])
            y = int(point[1])
            rad = int(circle_radius)
            elem_color = Element.combo_matrix[i]["color"]
            pygame.draw.circle(surface, elem_color, (x, y), rad)
            self.print_text(
                Element.combo_matrix[i]["symbol"],
                x - rad / 2,
                y - rad/1.5,
                color.WHITE,
                rad,
                surface,
            )
        return surface
