from elements import Element
import random


class Monster:
    def __init__(self, name, elem_name, hp, attack):
        from state_machine import StateMachine
        from scene_manager import SceneManager

        self.state_machine = StateMachine.get_instance()
        self.scene_manager = SceneManager.get_instance()

        self.name = name
        self.image = None
        self.elem = Element.get_element(elem_name)
        self.symbol = self.elem["symbol"]
        self.color = self.elem["color"]
        self.hp = hp
        self.max_hp = hp
        self.attack = attack


class Ally(Monster):
    def __init__(
        self, name, elem_name, hp, attack, rcv, skill_id, skill_mod, skill_value
    ):
        super().__init__(name, elem_name, hp, attack)
        self.rcv = rcv

        self.skill_id = skill_id
        self.skill_mod = skill_mod
        self.skill_value = skill_value

    def ally_attack(self, gems):
        enemy = self.state_machine._current_enemy
        elem_mod = Element.get_elem_ratio(self.elem, enemy.elem)
        mod = (
            random.uniform(0.7, 1.3) * (self.state_machine._combo + gems - 2) * elem_mod
        )
        dmg = max(int(self.attack * mod) - enemy.defense, 1)
        dmg = enemy.check_shields(dmg, gems)
        self.scene_manager.set_message(
            f"{self.state_machine._combo} COMBO ~ {self.name} did {dmg} {self.symbol} damage"
        )
        return dmg


class Enemy(Monster):
    def __init__(self, name, elem_name, hp, attack, defense, skill):
        super().__init__(name, elem_name, hp, attack)
        self.defense = defense
        self.cooldown = 0  # random.randint(2, 4)
        self.skill = skill
        self.shield = ""

    def take_damage(self, damage):
        self.hp -= damage

    def is_alive(self):
        if self.hp <= 0:
            return False
        else:
            return True

    def do_action(self):
        self.shield = ""
        self.cooldown -= 1

        # To make skills based on enemy
        if self.cooldown <= 0:
            self.do_skill()
            self.cooldown = 1 + random.randint(1, 4)
        else:
            self.do_attack()

        # if damage > (party.max_hp / 10):
        #   global shake_timer
        #    shake_timer = 1000

    def do_attack(self):
        party = self.state_machine._party
        damage = max(int(self.attack * 2 * random.uniform(0.5, 1.5)), 1)
        self.scene_manager.set_message(f"{self.name} did {damage} to {party.name}")
        self.state_machine.set_queue(1500)
        party.take_damage(damage)

    def do_skill(self):
        if self.skill == "weak":
            self.remove_weak()
        elif self.skill == "void":
            self.call_void()
        elif self.skill == "flood":
            self.flood()
        elif self.skill == "destroy":
            self.destroy()
        elif self.skill == "poison":
            self.call_poison()
        elif self.skill == "counter":
            self.shield = "counter"
        elif self.skill == "shield":
            self.shield = "shield"

    def check_shields(self, dmg, gems):
        if self.shield == "shield":
            if self.state_machine._combo >= 5:
                self.shield = ""
                return dmg
            else:
                self.scene_manager.set_message(f"{self.name} absorbed the attack")
                self.state_machine.set_queue(1500)
                return 1

        if self.shield == "counter":
            if gems < 5:
                self.do_action()
                self.scene_manager.set_message(f"{self.name} did a counter attack")
                self.state_machine.set_queue(1500)

        return dmg

    def flood(self):
        gem_grid = self.state_machine._gem_grid.gems
        for col in gem_grid:
            for gem in col:
                gem.elem = self.elem
                gem.flash = 50

    def destroy(self):
        gem_grid = self.state_machine._gem_grid.gems
        chosen_elem = random.choice(Element.matrix)
        self.state_machine._party.hp = int(0.2 * self.state_machine._party.hp)
        for col in gem_grid:
            for gem in col:
                if gem.elem == chosen_elem:
                    gem.elem = Element.LIFE
                    gem.flash = 50
        self.state_machine.set_queue(1500)

    def call_void(self):
        gem_grid = self.state_machine._gem_grid.gems
        count = random.randint(10, 20)
        for _ in range(count):
            gem = random.choice([gem for col in gem_grid for gem in col])
            gem.elem = Element.VOID
            gem.flash = 50
        self.state_machine.set_queue(1500)

    def call_poison(self):
        gem_grid = self.state_machine._gem_grid.gems
        count = random.randint(5, 10)
        for _ in range(count):
            gem = random.choice([gem for col in gem_grid for gem in col])
            gem.elem = Element.POISON
            gem.flash = 50
        self.state_machine.set_queue(1500)

    def remove_weak(self):
        gem_grid = self.state_machine._gem_grid.gems
        strong_elem = Element.get_insulter(self.elem)
        weak_elem = Element.get_destroyer(self.elem)

        weak_exists = False
        for col in gem_grid:
            for gem in col:
                if gem.elem == weak_elem:
                    gem.elem = strong_elem
                    gem.flash = 50
                    weak_exists = True
        if weak_exists:
            self.scene_manager.set_message(
                f"{self.name} changes {weak_elem['symbol']} into {strong_elem['symbol']}"
            )
            self.state_machine.set_queue(1500)
