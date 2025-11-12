import pygame
import sys
import logging
import pygame.mixer

from utils.constants import Constants
from utils.game_states import GameState
from gameboard import GameBoard
from database_connector import connect_to_database
from controllers.game_controller import GameController
from controllers.menu_controller import MenuController
from DAL.player_dao import PlayerDAO

logging.basicConfig(level=logging.INFO)


def start_background_music(state):
    if state in {GameState.MENU, GameState.NICKNAME_INPUT, GameState.LOAD_GAME}:
        music_file = 'utils/audio/menu-background-theme.mp3'
    elif state == GameState.PLAYING:
        music_file = 'utils/audio/game-background-theme.mp3'
    else:
        return

    if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)


def stop_background_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def toggle_volume():
    current_volume = pygame.mixer.music.get_volume()
    new_volume = 0.05 if current_volume == 0 else 0
    pygame.mixer.music.set_volume(new_volume)


def initialize_pygame():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.05)
    Constants.FONT = pygame.font.Font(None, Constants.FONT_SIZE_LARGE)
    Constants.SMALL_FONT = pygame.font.Font(None, Constants.FONT_SIZE_SMALL)
    return pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))


def handle_quit():
    pygame.quit()
    sys.exit()


def main():
    cnx = connect_to_database()
    if cnx is None:
        logging.error("Failed to connect to the database.")
        return

    screen = initialize_pygame()
    pygame.display.set_caption("Galactic Gladiators")
    clock = pygame.time.Clock()

    game_state = {
        'state': GameState.MENU
    }

    game_controller = GameController(cnx, game_state)
    menu_controller = MenuController(screen, cnx)

    nickname = ''
    game_id = 0

    new_game_rect = None
    load_game_rect = None
    start_button_rect = None
    back_button_rect = None

    cheatcode = False
    end_cutscene_played = False
    current_music_state = None

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    handle_quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        cheatcode = not cheatcode
                    elif event.key == pygame.K_m:
                        toggle_volume()

                if game_state['state'] == GameState.MENU:
                    game_state['state'] = menu_controller.handle_menu_events(event, new_game_rect, load_game_rect)

                elif game_state['state'] == GameState.NICKNAME_INPUT:
                    game_state['state'], nickname = menu_controller.handle_nickname_events(event, start_button_rect,
                                                                                           back_button_rect, nickname)
                    if game_state['state'] == GameState.PLAYING:
                        game_id = game_controller.create_game(nickname)
                        game_state['state'] = GameState.CUTSCENE

                elif game_state['state'] == GameState.LOAD_GAME:
                    saved_games_rects, back_button_rect = menu_controller.draw_load_game_screen()
                    game_state['state'], game_id = menu_controller.handle_load_game_events(event)

            if ((current_music_state != game_state['state'] and (current_music_state in
                                                                 {GameState.PLAYING, GameState.CUTSCENE} or
                                                                 game_state['state'] in
                                                                 {GameState.PLAYING, GameState.CUTSCENE})) or
                    current_music_state is None):
                stop_background_music()
                start_background_music(game_state['state'])
                current_music_state = game_state['state']

            screen.fill(Constants.BLACK)

            if game_state['state'] == GameState.MENU:
                new_game_rect, load_game_rect = menu_controller.draw_main_menu()

            elif game_state['state'] == GameState.NICKNAME_INPUT:
                start_button_rect, back_button_rect = menu_controller.draw_nickname_input(nickname)

            elif game_state['state'] == GameState.LOAD_GAME:
                saved_games_rects, back_button_rect = menu_controller.draw_load_game_screen()

            elif game_state['state'] == GameState.CUTSCENE:
                game_controller.show_cutscene(screen, game_id)
                game_state['state'] = GameState.PLAYING

            elif game_controller.get_has_ended(game_id) and not end_cutscene_played:
                game_controller.show_cutscene(screen, game_id)
                end_cutscene_played = True

            elif game_state['state'] == GameState.PLAYING:
                player_dao = PlayerDAO(cnx)
                player, enemy_player = player_dao.get_players(game_id)

                game_board = GameBoard(screen, game_id, cnx, game_controller, player, enemy_player, cheatcode)
                game_board.draw()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        handle_quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game_controller.player.handle_click(event.pos, game_id)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            cheatcode = not cheatcode
                        elif event.key == pygame.K_m:
                            toggle_volume()

            pygame.display.flip()
            clock.tick(Constants.FPS)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    finally:
        cnx.close()
        handle_quit()


if __name__ == '__main__':
    main()
