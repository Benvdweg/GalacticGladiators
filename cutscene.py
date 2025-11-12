import pygame
import random

from utils.constants import Constants


class Cutscene:
    def __init__(self, screen, player_nickname, enemy_nickname, game_controller):
        self.screen = screen
        self.player_nickname = player_nickname
        self.enemy_nickname = enemy_nickname
        self.stars = self.create_stars()
        self.spaceship = self.load_spaceship()
        self.font = pygame.font.Font(None, 72)
        self.game_controller = game_controller

    def create_stars(self):
        return [(random.randint(0, Constants.SCREEN_WIDTH), random.randint(0, Constants.SCREEN_HEIGHT))
                for _ in range(100)]

    def load_spaceship(self):
        spaceship = pygame.image.load('GalacticGladiators/utils/images/spaceship.png')
        return pygame.transform.scale(spaceship, (100, 100))

    def draw_stars(self):
        for star in self.stars:
            if random.random() < 0.1:
                pygame.draw.circle(self.screen, Constants.WHITE, star, random.randint(1, 2))
            else:
                pygame.draw.circle(self.screen, Constants.WHITE, star, 1)

    def animate_spaceship(self):
        ship_y = Constants.SCREEN_HEIGHT
        while ship_y > -100:
            self.screen.fill(Constants.BLACK)
            self.draw_stars()
            self.screen.blit(self.spaceship, (Constants.SCREEN_WIDTH // 2 - 50, ship_y))
            pygame.display.flip()
            ship_y -= 5
            pygame.time.delay(10)

    def render_text(self, winner=None, score=None):
        if winner is None or score is None:
            player_text = self.font.render(self.player_nickname, True, Constants.WHITE)
            enemy_text = self.font.render(self.enemy_nickname, True, Constants.WHITE)
            vs_text = self.font.render("VS", True, Constants.YELLOW)
        else:
            player_text = self.font.render(winner + " heeft gewonnen", True, Constants.YELLOW)
            score_text = self.font.render(score, True, Constants.WHITE)

        if winner is None or score is None:
            total_height = player_text.get_height() + vs_text.get_height() + enemy_text.get_height() + 50
            start_y = (Constants.SCREEN_HEIGHT - total_height) // 2
            player_y = start_y
            vs_y = start_y + player_text.get_height() + 30
            enemy_y = vs_y + vs_text.get_height() + 30

            player_x = (Constants.SCREEN_WIDTH - player_text.get_width()) // 2
            vs_x = (Constants.SCREEN_WIDTH - vs_text.get_width()) // 2
            enemy_x = (Constants.SCREEN_WIDTH - enemy_text.get_width()) // 2

            player_pos = (player_x, player_y)
            vs_pos = (vs_x, vs_y)
            enemy_pos = (enemy_x, enemy_y)

            return (player_text, vs_text, enemy_text), (player_pos, vs_pos, enemy_pos)
        else:
            total_height = player_text.get_height() + score_text.get_height() + 50
            start_y = (Constants.SCREEN_HEIGHT - total_height) // 2
            player_y = start_y
            score_y = start_y + player_text.get_height() + 30

            player_x = (Constants.SCREEN_WIDTH - player_text.get_width()) // 2
            score_x = (Constants.SCREEN_WIDTH - score_text.get_width()) // 2

            player_pos = (player_x, player_y)
            score_pos = (score_x, score_y)

            return (player_text, score_text), (player_pos, score_pos)

    def animate_text(self, texts, positions):
        player_text, vs_text, enemy_text = texts
        player_pos, vs_pos, enemy_pos = positions

        alpha = 0
        while alpha < 255:
            self.screen.fill(Constants.BLACK)
            self.draw_stars()

            for text, pos in zip((player_text, vs_text, enemy_text), (player_pos, vs_pos, enemy_pos)):
                text_surface = text.copy()
                text_surface.set_alpha(alpha)
                self.screen.blit(text_surface, pos)

            pygame.display.flip()
            alpha += 5
            pygame.time.delay(10)

    def animate_end_text(self, texts, positions):
        player_text, score_text = texts
        player_pos, score_pos = positions

        alpha = 0
        while alpha < 255:
            self.screen.fill(Constants.BLACK)
            self.draw_stars()

            text_surface = player_text.copy()
            text_surface.set_alpha(alpha)
            self.screen.blit(text_surface, player_pos)

            text_surface = score_text.copy()
            text_surface.set_alpha(alpha)
            self.screen.blit(text_surface, score_pos)

            pygame.display.flip()
            alpha += 5
            pygame.time.delay(10)

    def display_final_frame(self, texts, positions):
        player_text, vs_text, enemy_text = texts
        player_pos, vs_pos, enemy_pos = positions

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            self.screen.fill(Constants.BLACK)
            self.draw_stars()

            for text, pos in zip((player_text, vs_text, enemy_text), (player_pos, vs_pos, enemy_pos)):
                self.screen.blit(text, pos)

            pygame.display.flip()
            pygame.time.delay(15)

    def display_end_final_frame(self, texts, positions):
        player_text, score_text = texts
        player_pos, score_pos = positions

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 3000:
            self.screen.fill(Constants.BLACK)
            self.draw_stars()

            self.screen.blit(player_text, player_pos)
            self.screen.blit(score_text, score_pos)

            pygame.display.flip()
            pygame.time.delay(15)

    def play(self):
        pygame.mixer.music.load("GalacticGladiators/utils/audio/battle-theme.mp3")
        pygame.mixer.music.play(-1)

        self.animate_spaceship()

        texts, positions = self.render_text()

        pygame.mixer.music.fadeout(6000)

        self.animate_text(texts, positions)
        self.display_final_frame(texts, positions)

        pygame.mixer.music.stop()

    def play_end_scene(self, winner, score, player_won):
        if player_won:
            pygame.mixer.music.load("GalacticGladiators/utils/audio/victory-theme.mp3")

        elif player_won is False:
            pygame.mixer.music.load("GalacticGladiators/utils/audio/defeat-theme.mp3")
        else:
            pygame.mixer.music.load("GalacticGladiators/utils/audio/draw-theme.mp3")
        pygame.mixer.music.play(-1)

        self.animate_spaceship()

        texts, positions = self.render_text(winner, score)

        pygame.mixer.music.fadeout(6000)

        self.animate_end_text(texts, positions)

        self.display_end_final_frame(texts, positions)

        pygame.mixer.music.stop()
