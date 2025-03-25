from main_menu import MainMenu
from party_select import PartySelect
from dungeon_select import DungeonSelect
from battle import BattleScene
from state_machine import StateMachine
from state_machine import GameState


class SceneManager:
    _instance = None  # Class variable to hold the singleton instance

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.battle_scene = BattleScene()
        self.scenes = {
            GameState.MAIN_MENU: MainMenu(),
            GameState.PARTY_SELECT: PartySelect(),
            GameState.DUNGEON_SELECT: DungeonSelect(),
            GameState.PLAYER_TURN: self.battle_scene,
            GameState.PLAYER_ACTION: self.battle_scene,
            GameState.PLAYER_ATTACK: self.battle_scene,
            GameState.ENEMY_TURN: self.battle_scene,
        }
        self.fade = 0
        self.fade_color=""
        self.status_message = ""

    @classmethod
    def get_instance(cls):
        return cls._instance or cls()
    
    def set_message(self, message, to_print=True):
        self.status_message = message
        if to_print:
            print(message)

    def get_scene(self):
        state = StateMachine().get_state()
        if state in self.scenes:
            return self.scenes[state]

    def draw(self):
        scene = self.get_scene()
        if scene.load:
            scene.fade(1000,True)
            scene.load = False
        if self.fade:
            if self.fade_color:
                scene.fade(self.fade,False,self.fade_color)
                self.fade_color= ""
            else:
                scene.fade(self.fade)
            self.fade = 0
        else:
            scene.show()
            scene.status_text(self.status_message)
    