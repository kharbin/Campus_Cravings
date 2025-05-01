import pygame
from .constants import Constants

class Button:
    def __init__(self, x, y, width, height, text, callback, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, Constants.CRIMSON)
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.callback = callback

    def draw(self, screen, color=Constants.CREAM):  # Default to cream
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
