from elements import Element
import loaders
import random
from state_machine import StateMachine
from scene_manager import SceneManager
from monster import Ally


class Party:
    def __init__(self):
        self.state_machine = StateMachine.get_instance()
        self.scene_manager = SceneManager.get_instance()
        self.name = ""
        self.max_hp = 0
        self.hp = 0
        self.rcv = 0
        self.allies = []
        self.leader = None
        self.leader_skill = None
        self.round_damage = 0
        self.party_setup()

    def party_setup(self):
        ally_list = loaders.load_json_file("allies")
        random_keys = random.sample(list(ally_list.keys()), 4)
        for key in random_keys:
            ally = Ally(**ally_list[key])
            ally.image = loaders.load_image("allies", key, True, 180)
            self.allies.append(ally)
            loaders.data_collection(f"{ally_list[key]['name']} ")
        loaders.data_collection("\n")
        self.leader = self.allies[0]

        self.max_hp = sum(member.hp for member in self.allies)
        self.hp = self.max_hp
        self.rcv = sum(member.rcv for member in self.allies) / len(self.allies)
        self.leader_skill = self.set_skill()

    def set_skill(self):
        skill = loaders.load_json_file("skills")[self.leader.skill_id]
        return LeaderSkill(
            self.leader.elem["name"],
            self.leader.skill_mod,
            self.leader.skill_value,
            self.leader.skill_id,
            **skill,
        )

    def party_action(self, gems, elem):
        if not self.leader_skill.active:
            self.leader_skill.check_active(self.state_machine, gems, elem)

        attack_damage = 0
        for ally in self.allies:
            if ally.elem == elem:
                attack_damage += ally.ally_attack(gems)

        self.round_damage += attack_damage

        if elem is Element.LIFE:
            heal = int(random.uniform(0.7, 1.3) *self.rcv * (gems + self.state_machine._combo))
            self.hp += heal
            self.scene_manager.set_message(
                f"{self.state_machine._combo} COMBO ~ {self.name} healed for {heal}"
            )
            self.hp = self.max_hp if self.hp > self.max_hp else self.hp
        elif elem is Element.POISON:
            poison = int(random.uniform(0.7, 1.3) *self.rcv * 2 * (gems + self.state_machine._combo))
            self.hp -= poison
            self.scene_manager.set_message(
                f"{self.state_machine._combo} COMBO ~ {self.name} took {poison}"
            )
            self.hp = self.max_hp if self.hp > self.max_hp else self.hp
        elif attack_damage == 0:
            self.scene_manager.set_message(
                f"{self.state_machine._combo} COMBO ~ No-one attacked"
            )

        loaders.data_collection(f"{gems}  {elem['symbol']}  {attack_damage}\n")

    def do_damage(self):
        if self.round_damage == 0:
            self.scene_manager.set_message(f"{self.name} did no damage this turn")
        else:
            self.round_damage = int(
                self.round_damage * self.leader_skill.use_skill(self.state_machine)
            )
            self.scene_manager.set_message(
                f"{self.name} did {self.round_damage} to {self.state_machine._current_enemy.name}"
            )
        self.state_machine._current_enemy.take_damage(self.round_damage)
        loaders.data_collection(
            f"{self.state_machine._combo} COMBO\n{self.round_damage}\n\n"
        )
        self.round_damage = 0
        self.state_machine._combo = 0

    def take_damage(self, damage):
        self.hp -= damage


class LeaderSkill:
    def __init__(self, elem, mod, value, skill_id, name, desc):
        self.name = name
        self.scene_manager = SceneManager.get_instance()
        self.mod = mod
        self.value = value
        self.skill_id = skill_id
        self.desc = desc.format(elem=elem, mod=self.mod, value=self.value)
        self.active = False

    def check_active(self, state_machine, gems, elem):
        if self.active:
            return
        combo = state_machine._combo
        party = state_machine._party
        # Dictionary of skills and their condition
        effects = {
            "combo": f"{combo} >= {self.value}",
            "gem_count": f"{gems} >= {self.value}",
            "type": f"{elem} == {party.leader.elem}",
            "high_hp": f"(100 * {party.hp} / {party.max_hp}) > 80",
            "low_hp": f"(100 * {party.hp} / {party.max_hp}) < 50",
            "heal_to_dmg": f"{elem} == {Element.LIFE}",
        }

        if eval(effects[self.skill_id]):
            self.active = True

    def use_skill(self, state_machine):
        if self.active:
            party = state_machine._party
            self.scene_manager.set_message(
                f"{self.name} : {self.desc} ({party.leader.name})"
            )
            self.active = False
            return self.mod
        else:
            return 1
