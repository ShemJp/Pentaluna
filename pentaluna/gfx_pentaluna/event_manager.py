# event_manager.py (as a module)
import pygame

# Global state variables
mouse_pos = (0, 0)
mouse_button_down = False
mouse_button_up = False
keys_pressed = set()
keys_released = set()
input_text = ""

# Update the state based on pygame events
def update():
    global mouse_pos, mouse_button_down, mouse_button_up, keys_pressed, keys_released, input_text

    mouse_button_down = False
    mouse_button_up = False
    keys_pressed.clear()
    keys_released.clear()
    input_text = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # Mouse events
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button_up = True

        # Keyboard events
        if event.type == pygame.KEYDOWN:
            keys_pressed.add(event.key)
            if event.unicode.isprintable():
                input_text = event.unicode
        elif event.type == pygame.KEYUP:
            keys_released.add(event.key)

# Helper functions to access the event state
def get_mouse_pos():
    return mouse_pos

def is_mouse_button_down():
    return mouse_button_down

def is_mouse_button_up():
    return mouse_button_up

def is_key_pressed(key):
    return key in keys_pressed

def get_input_text():
    return input_text