
        self.next_attack = []
        self.combo = 0


            else:
                if state_machine.game_state == GameState.CHOOSE_DUNGEON:
                    dungeon_list.current_dungeon = dungeon_scene.show(
                        dungeon_list, state_machine
                    )
                    if dungeon_list.current_dungeon:
                        enemy = dungeon_list.current_dungeon.get_new_enemy()
                        state_machine.queue_drop(sum(gem_grid.gems, []))
                elif state_machine.game_state == GameState.PLAYER_INPUT:
                    player_input(gem_grid)
                    battle_scene.show(gem_grid, party, enemy, state_machine)
                # elif self.game_state == GameState.PLAYER_ACTION:
                # player_action()
                # elif self.game_state == GameState.ENEMY_TURN:
                # enemy_turn()
                # elif self.game_state == GameState.ATTACK_SEQUENCE:
                # attack_action(*self.next_attack)



def player_action():
    if state_machine.all_gems_clear:
        party.do_damage()
        state_machine.game_state = GameState.ENEMY_TURN
        state_machine.all_gems_clear = False

    else:
        attack_found = False
        for y in range(config.GRID_HEIGHT - 1, -1, -1):
            if attack_found:
                break
            for x in range(GRID_WIDTH):
                gem = gem_grid[x][y]
                gem_count = find_matches(gem)
                if gem_count > 0:
                    state_machine.queue_animation(1000)
                    attack_found = True
                    state_machine.game_state = GameState.ATTACK_SEQUENCE
                    state_machine.next_attack = (gem_count, gem.elem)
                    state_machine.combo += 1
                    break
        if not attack_found:
            if any(gem.matched for col in gem_grid for gem in col):
                state_machine.queue_drop(cascade())
            else:
                state_machine.all_gems_clear = True





