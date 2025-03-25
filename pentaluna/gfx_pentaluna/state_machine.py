from enum import Enum, auto
import pygame


class GameState(Enum):
    MAIN_MENU = auto()
    PARTY_SELECT = auto()
    DUNGEON_SELECT = auto()
    PLAYER_TURN = auto()
    PLAYER_ACTION = auto()
    PLAYER_ATTACK = auto()
    ENEMY_TURN = auto()


class StateMachine:
    _instance = None  # Class variable to hold the singleton instance
    _name = ""
    _game_state = GameState.MAIN_MENU
    _next_state = None
    _start_time = 0
    _queue_time = 0
    _queue = False
    _next_attack = ()
    _combo = 0
    _dungeon_list = None
    _current_dungeon = None
    _floor = 0
    _current_enemy = None
    _party = None
    _gem_grid = None
    _finished_matches = False

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls._instance or cls()

    def set_state(self, new_state):
        self._game_state = new_state

    def get_state(self):
        return self._game_state

    def set_next(self, new_state):
        self._next_state = new_state

    def set_queue(self, time):
        self._queue = True
        self._queue_time = time
        self._start_time = pygame.time.get_ticks()

    def check_queues(self):
        if self._queue:
            elapsed_time = pygame.time.get_ticks() - self._start_time
            if elapsed_time > self._queue_time:
                self._queue = False
                self._queue_time = 0
            return True
        elif self._next_state:
            self.set_state(self._next_state)
            self._next_state = None
            return True
        else:
            return False
