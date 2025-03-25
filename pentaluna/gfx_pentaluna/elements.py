from config import color
import random


class Element:
    FIRE = {"name": "fire", "color": color.RED, "symbol": "火"}
    WATER = {"name": "water", "color": color.BLUE, "symbol": "水"}
    EARTH = {"name": "earth", "color": color.YELLOW, "symbol": "土"}
    WOOD = {"name": "wood", "color": color.GREEN, "symbol": "木"}
    METAL = {"name": "metal", "color": color.STEEL, "symbol": "金"}
    LIFE = {"name": "life", "color": color.PINK, "symbol": "命"}
    VOID = {"name": "void", "color": color.SHADOW, "symbol": "虚"}
    POISON = {"name": "poison", "color": color.PURPLE, "symbol": "毒"}
    MIXED = {"name": "none", "color": color.BLACK, "symbol": ""}
    matrix = [FIRE, WATER, EARTH, WOOD, METAL]
    combo_matrix = [FIRE, EARTH, METAL, WATER, WOOD]

    @classmethod
    def get_element(cls, elem_name):
        return getattr(cls, elem_name.upper())

    @classmethod
    def random_elem(cls):
        return random.choice(cls.matrix + [cls.LIFE])

    @classmethod
    def get_destroyer(cls, elem):
        elem_index = cls.matrix.index(elem)
        return cls.matrix[(elem_index + 1) % len(cls.matrix)]

    @classmethod
    def get_creator(cls, elem):
        elem_index = cls.combo_matrix.index(elem)
        return cls.combo_matrix[(elem_index + 1) % len(cls.combo_matrix)]

    @classmethod
    def get_insulter(cls, elem):
        elem_index = cls.matrix.index(elem)
        return cls.matrix[(elem_index - 1) % len(cls.matrix)]

    @classmethod
    def get_elem_ratio(cls, atk_elem, def_elem):
        if cls.get_destroyer(def_elem) == atk_elem:
            return 2 / 3
        elif cls.get_insulter(def_elem) == atk_elem:
            return 3 / 2
        return 1
