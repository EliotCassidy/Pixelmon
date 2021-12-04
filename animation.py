import pygame


class AnimateSprite(pygame.sprite.Sprite):
    
    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Image\player.png")