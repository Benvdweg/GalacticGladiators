import pygame


class Button:
    def __init__(self, text, pos, font_size=36, bg_color=(0, 0, 0), text_color=(255, 255, 255), radius=10, alpha=0,
                 name=None):
        self.x, self.y = pos
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.radius = radius
        self.alpha = alpha
        self.render_text()
        self.name = name

    def render_text(self):
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        text_width, text_height = self.rendered_text.get_size()
        button_width = text_width + 50  # Extra padding around text
        button_height = text_height + 25  # Extra padding around text

        self.surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)  # SRCALPHA for transparency
        self.surface.fill((0, 0, 0, self.alpha))  # Fill with background color and transparency

        # Draw rounded rectangle
        pygame.draw.rect(self.surface, self.bg_color, (0, 0, button_width, button_height), border_radius=self.radius)

        # Render text onto the button surface
        text_x = (button_width - text_width) // 2
        text_y = (button_height - text_height) // 2
        self.surface.blit(self.rendered_text, (text_x, text_y))

        # Create rect object for collision detection
        self.rect = pygame.Rect(self.x, self.y, button_width, button_height)

    def change_text(self, text, bg="black"):
        self.text = self.font.render(text, True, pygame.Color("white"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def is_clicked(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                return True
        return False
