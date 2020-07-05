import pygame
import CardBlitz.static_values as val

# properties of a player
class Player():
    def __init__(self, id):
        self.id = id
        self.resources = self.init_resources()
        self.active = False
        self.victory = False
        self.hand = []

    def init_resources(self):
        resources = {}
        resources['move_tokens'] = 2
        resources['attack_tokens'] = 2
        resources['skill_tokens'] = 1
        return resources


# properties of a card
class Card():
    def __init__(self, id, name, atk, range, hp, spd, image):
        self.id = id
        self.name = name
        self.atk = atk
        self.range = range
        self.hp = hp
        self.spd = spd
        self.image = image

# properties of an object
class Object():
    def __init__(self, card, xpos, ypos, owner):
        self.card = card
        self.hp_current = self.card.hp
        self.xpos = xpos
        self.ypos = ypos
        self.drag = False
        self.owner = owner
        self.rect = pygame.rect.Rect(xpos, ypos, val.square_size, val.square_size)