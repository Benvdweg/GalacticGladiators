import pygame

from utils.constants import Constants
from utils.game_states import GameState
from views.menu_view import MenuView
from DAL.game_dao import GameDAO


class MenuController:
    def __init__(self, screen, cnx):
        self.screen = screen
        self.menu_view = MenuView(screen)
        self.game_dao = GameDAO(cnx)
        self.scroll_offset = 0
        self.saved_games = []
        self.nickname = ""

    @staticmethod
    def handle_menu_events(event, new_game_rect, load_game_rect):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if new_game_rect.collidepoint(mouse_x, mouse_y):
                return GameState.NICKNAME_INPUT
            elif load_game_rect.collidepoint(mouse_x, mouse_y):
                return GameState.LOAD_GAME
        return GameState.MENU

    def handle_load_game_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = event.pos
                saved_games_rects, back_button_rect = self.draw_load_game_screen()
                for rect, game_id in saved_games_rects:
                    if rect.collidepoint(mouse_x, mouse_y):
                        return GameState.PLAYING, game_id
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    return GameState.MENU, None
        elif event.type == pygame.MOUSEWHEEL:
            self.handle_scroll(event)
        return GameState.LOAD_GAME, None

    def handle_scroll(self, event):
        self.scroll_offset -= event.y * Constants.SCROLL_SPEED
        total_height = len(self.saved_games) * 60
        visible_height = Constants.SCREEN_HEIGHT - Constants.SCREEN_HEIGHT // 4 - 150
        max_scroll = max(0, total_height - visible_height)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

    def handle_nickname_events(self, event, start_button_rect, back_button_rect, nickname):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return GameState.PLAYING, self.nickname
            elif event.key == pygame.K_BACKSPACE:
                self.nickname = self.nickname[:-1]
            elif event.unicode.isprintable():
                self.nickname += event.unicode
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if start_button_rect.collidepoint(mouse_x, mouse_y):
                return GameState.PLAYING, nickname
            elif back_button_rect.collidepoint(mouse_x, mouse_y):
                return GameState.MENU, nickname
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                return GameState.NICKNAME_INPUT, nickname[:-1]
            elif event.key == pygame.K_RETURN:
                return GameState.PLAYING, nickname
            else:
                return GameState.NICKNAME_INPUT, nickname + event.unicode
        return GameState.NICKNAME_INPUT, nickname

    def draw_main_menu(self):
        return self.menu_view.draw_main_menu()

    def draw_nickname_input(self, nickname):
        return self.menu_view.draw_nickname_input(nickname)

    def draw_load_game_screen(self):
        if not self.saved_games:
            self.saved_games = self.game_dao.get_all_games()
        return self.menu_view.draw_load_game_screen(self.saved_games, self.scroll_offset)
