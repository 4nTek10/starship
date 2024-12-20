# starship
import pygame                                                                                                                       # Importowanie biblioteki PYGAME
from os.path import join
from random import randint, uniform
from pygame.sprite import Group

class Player(pygame.sprite.Sprite):                                                                                                 # Tworzymy klase GRACZ
    def __init__(self, groups):                                                                                                     # Konstruktor klasy
        super().__init__(groups)                                                                                                    # Wywołanie konstruktora klasy bazowej
        self.image = pygame.image.load(join
