import pygame

import config
from config import color
import event_manager

from state_machine import StateMachine

from state_machine import GameState
from scene_manager import SceneManager

from gems import GemGrid
from gems import Gem
from party import Party
from dungeons import DungeonList


# Singletons
state_machine = StateMachine.get_instance()
scene_manager = SceneManager.get_instance()

# Load Game Data
state_machine._dungeon_list = DungeonList()
state_machine._party = Party()

# Initialize Pygame
pygame.init()
pygame.display.set_caption("*** PENTALUNA : FALLEN MOONS ***")

# Timed Events
clock = pygame.time.Clock()
start_time = 0
shake_intensity = 5  # Max pixel movement
shake_timer = 0  # Timer to track the duration


def main():
    run = True
    while run:
        event_manager.update()
        if not state_machine.check_queues():
            if state_machine.get_state() == GameState.MAIN_MENU:
                main_menu()
            elif state_machine.get_state() == GameState.PARTY_SELECT:
                party_select()
            elif state_machine.get_state() == GameState.DUNGEON_SELECT:
                dungeon_select()
            else:
                battle_loop()

        scene_manager.draw()
        pygame.display.flip()
        clock.tick(60)

  
    


def battle_loop():
    if state_machine.get_state() == GameState.PLAYER_TURN:
        player_turn()
    elif state_machine.get_state() == GameState.PLAYER_ACTION:
        player_action()
    elif state_machine.get_state() == GameState.PLAYER_ATTACK:
        player_attack()
    elif state_machine.get_state() == GameState.ENEMY_TURN:
        enemy_turn()
    return


def main_menu():
    if event_manager.is_key_pressed(pygame.K_SPACE):
        scene_manager.fade = 2000
        state_machine.set_next(GameState.PARTY_SELECT)
    return


def party_select():
    name = state_machine._name
    if event_manager.is_key_pressed(pygame.K_RETURN):
        state_machine._party.name = state_machine._name
        scene_manager.fade = 1000
        state_machine.set_next(GameState.DUNGEON_SELECT)
    elif event_manager.is_key_pressed(pygame.K_BACKSPACE):
        name = name[:-1]
    else:
        input_text = event_manager.get_input_text()
        if input_text and input_text.isprintable():
            name += input_text
    state_machine._name = name


def dungeon_select():
    chosen_dungeon = ""
    width, height = state_machine._dungeon_list.list[0].image_tb.get_size()
    offsets = [
        (0, 0),
        (50 + width, 0),
        (100 + width * 2, 0),
        (0, height + 60),
        (50 + width, height + 60),
        (100 + width * 2, height + 60),
        (50 + width, height * 2 + 120),
    ]
    # Check for mouse click event
    if event_manager.mouse_button_down:
        mouse_x, mouse_y = event_manager.get_mouse_pos()
        for i, dungeon in enumerate(state_machine._dungeon_list.list):
            x_offset, y_offset = offsets[i]
            if dungeon.is_clicked(mouse_x, mouse_y, x_offset, y_offset):
                chosen_dungeon = dungeon

        if chosen_dungeon:
            set_dungeon(chosen_dungeon)
        return


def player_turn():
    global start_time
    match_time = 7500

    elapsed_time = pygame.time.get_ticks() - start_time if start_time else 0

    scene_manager.set_message(
        f"{int((match_time-elapsed_time)/100)/10} seconds to match", False
    )

    if elapsed_time > match_time:
        start_time = 0
        if Gem.get_choice():
            Gem.get_choice().clear_choice()
        state_machine.set_queue(1000)
        state_machine.set_state(GameState.PLAYER_ACTION)

    if event_manager.mouse_button_down:
        mouse_x, mouse_y = event_manager.get_mouse_pos()
        for col in state_machine._gem_grid.gems:
            for gem in col:
                if gem.is_clicked(mouse_x, mouse_y):
                    if not start_time:
                        start_time = pygame.time.get_ticks()
                    if not Gem.get_choice():
                        # Select the first gem
                        gem.set_choice()
                    elif gem == Gem.get_choice():
                        # Deselect the gem if it's the same one clicked again
                        gem.clear_choice()
                    elif state_machine._gem_grid.get_neighbours(gem, Gem.get_choice()):
                        # Swap gems if they are neighbors
                        state_machine._gem_grid.swap(gem, Gem.get_choice())
                        gem.clear_choice()


def player_action():
    if state_machine._finished_matches:
        state_machine._party.do_damage()
        state_machine.set_state(GameState.ENEMY_TURN)
        state_machine._finished_matches = False
    else:
        attack_found = False
        for y in range(config.ROWS - 1, -1, -1):
            if attack_found:
                break
            for x in range(config.COLUMNS):
                gem = state_machine._gem_grid.gems[x][y]
                gem_count = state_machine._gem_grid.find_matches(gem)
                if gem_count > 0:
                    state_machine.set_queue(1000)
                    attack_found = True
                    state_machine._next_attack = (gem_count, gem.elem)
                    state_machine.set_state(GameState.PLAYER_ATTACK)
                    state_machine._combo += 1
                    break
        if not attack_found:
            if any(gem.matched for col in state_machine._gem_grid.gems for gem in col):
                state_machine._gem_grid.cascade()
                state_machine.set_queue(500)
            else:
                state_machine._finished_matches = True


def player_attack():
    gems, elem = state_machine._next_attack
    state_machine._party.party_action(gems, elem)

    for row in state_machine._gem_grid.gems:
        for gem in row:
            if gem.matched:
                gem.color = color.WHITE
    state_machine.set_queue(1000)
    state_machine.set_state(GameState.PLAYER_ACTION)


def enemy_turn():
    if state_machine._current_enemy.is_alive():
        enemy_action()
    else:
        '''
        state_machine.set_queue(1500)
        scene_manager.fade_color = color.RED
        scene_manager.fade = 1500
        '''
        next_enemy()


def enemy_action():
    state_machine._current_enemy.do_action()
    state_machine.set_queue(1500)
    state_machine.set_state(GameState.PLAYER_TURN)


def set_dungeon(dungeon):
    state_machine._current_dungeon = dungeon
    state_machine._floor = 0
    next_enemy()


def next_enemy():
    dungeon = state_machine._current_dungeon
    scene_manager.battle_scene.load = True

    if state_machine._floor >= len(dungeon.enemies):
        print(f"All {state_machine._floor} enemies are dead")
        state_machine._party.hp=state_machine._party.max_hp
        state_machine._game_state = GameState.DUNGEON_SELECT
        return
    else:
        # Add new enemy and new grid to queue instead of immediately
        state_machine._gem_grid = GemGrid()
        state_machine._current_enemy = dungeon.enemies[state_machine._floor]
        state_machine._floor += 1
        print(
            f"{state_machine._floor} Floor: New Enemy is {state_machine._current_enemy.name}"
        )
        state_machine.set_queue(1500)
        state_machine.set_state(GameState.PLAYER_TURN)

main()