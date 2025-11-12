import time

import pygame

from GalacticGladiators.utils.constants import Constants


class MenuView:
    def __init__(self, screen):
        self.screen = screen
        self.last_blink_time = time.time()
        self.cursor_visible = True

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw_main_menu(self):
        self.draw_text('Galactic Gladiators', Constants.FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                       Constants.SCREEN_HEIGHT // 3)
        new_game_rect = self.draw_text('New Game', Constants.SMALL_FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                                       Constants.SCREEN_HEIGHT // 2)
        load_game_rect = self.draw_text('Load Game', Constants.SMALL_FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                                        Constants.SCREEN_HEIGHT // 2 + 100)
        return new_game_rect, load_game_rect

    def draw_nickname_input(self, nickname):
        self.draw_text('Enter Your Nickname', Constants.FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                       Constants.SCREEN_HEIGHT // 3)

        # Draw nickname and blinking cursor
        nickname_surface = Constants.SMALL_FONT.render(nickname, True, Constants.WHITE)
        nickname_rect = nickname_surface.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2))
        self.screen.blit(nickname_surface, nickname_rect)

        # Blinking cursor
        if time.time() - self.last_blink_time > 0.5:  # Blink every 0.5 seconds
            self.last_blink_time = time.time()
            self.cursor_visible = not self.cursor_visible

        if self.cursor_visible:
            cursor_x = nickname_rect.right + 2
            pygame.draw.line(self.screen, Constants.WHITE,
                             (cursor_x, nickname_rect.top),
                             (cursor_x, nickname_rect.bottom), 2)

        start_button_rect = self.draw_text('Start', Constants.SMALL_FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                                           Constants.SCREEN_HEIGHT // 2 + 100)
        back_button_rect = self.draw_text('Back', Constants.SMALL_FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                                          Constants.SCREEN_HEIGHT // 2 + 200)
        return start_button_rect, back_button_rect

    def draw_load_game_screen(self, saved_games, scroll_offset):
        self.draw_text('Load Game', Constants.FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                       Constants.SCREEN_HEIGHT // 10)

        list_top = Constants.SCREEN_HEIGHT // 4
        list_bottom = Constants.SCREEN_HEIGHT - 150
        visible_height = list_bottom - list_top

        saved_games_rects = [
            (self.draw_text(f"{game.created_at}", Constants.SMALL_FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                            list_top + i * 60 - scroll_offset), game.game_id)
            for i, game in enumerate(saved_games)
            if list_top - 60 <= list_top + i * 60 - scroll_offset <= list_bottom + 60
        ]

        total_height = len(saved_games) * 60
        if total_height > visible_height:
            scroll_height = max(visible_height * (visible_height / total_height), 20)
            scroll_pos = (scroll_offset / (total_height - visible_height)) * (visible_height - scroll_height)
            pygame.draw.rect(self.screen, Constants.WHITE,
                             (Constants.SCREEN_WIDTH - 30, list_top + scroll_pos, 20, scroll_height))

        back_button_rect = self.draw_text('Back', Constants.FONT, Constants.WHITE, Constants.SCREEN_WIDTH // 2,
                                          Constants.SCREEN_HEIGHT - 45)

        return saved_games_rects, back_button_rect
