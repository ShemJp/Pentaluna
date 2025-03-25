# imports.py
import pygame
import json
import os

# To remove
pygame.init()
screen = pygame.display.set_mode((800, 600))


def get_script_dir():
    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )  # Get the directory of the current script
    return script_dir


def load_json_file(filename):
    script_dir = get_script_dir()
    file_path = os.path.join(script_dir, "..", "json", filename + ".json")
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_image(folder, filename, resize=False, size=0):
    script_dir = get_script_dir()
    file_path = os.path.join(script_dir, "..", "images", folder, filename + ".jpeg")
    image = pygame.image.load(file_path)
    original_width, original_height = image.get_size()
    if resize:
        new_width = size
        new_height = int(original_height * (new_width / original_width))
        new_image = pygame.transform.scale(image, (new_width, new_height)).convert()
    else:
        new_image = image
    return new_image


def data_collection(data):
    script_dir = get_script_dir()
    file_path = os.path.join(script_dir, "..", "tools", "data" + ".txt")
    file = open(file_path, "a")
    # file.write(data)
    file.close()
