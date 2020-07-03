import os

import pygame
import CardBlitz.static_values as val
import pandas as pd

# setup window
window = pygame.display.set_mode((val.window_width, val.window_height))
pygame.display.set_caption("Card Blitz")

# in-game resource tracking
map = []
card_database = []
objects = []


# --------------------------------------------------------------------------------

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
        self.xpos = xpos
        self.ypos = ypos
        self.drag = False
        self.owner = owner
        self.rect = pygame.rect.Rect(xpos, ypos, xpos+val.square_size, ypos+val.square_size)

    # visualize map


def init_map():
    window.fill(val.color_black)
    for i in range(7):
        map.append([])
        for j in range(7):
            map[i].append([i * val.square_size, j * val.square_size])
            pygame.draw.rect(window, val.color_white,
                             (val.map_offset + i * (val.square_size + val.seperator_size),
                              val.map_offset + j * (val.square_size + val.seperator_size),
                              val.square_size,
                              val.square_size)
                             )


# load data
def init_database():
    db = pd.read_csv(os.path.join(os.getcwd(), 'data', 'database.csv'))
    image_list = []
    for image_file in os.listdir(os.path.join(os.getcwd(), 'data', 'img')):
        img = pygame.image.load(os.path.join(os.getcwd(), 'data', 'img', image_file)).convert()
        image_list.append(img)
    for index, row in db.iterrows():
        new_card = Card(index, row['name'], row['attack'], row['range'], row['health'], row['speed'], image_list[index])
        card_database.append(new_card)


def init_objects():
    objects.append(Object(card_database[0], 0, 0, 'p2'))
    objects.append(Object(card_database[1], 3, 0, 'p2'))
    objects.append(Object(card_database[2], 6, 0, 'p2'))
    objects.append(Object(card_database[3], 0, 6, 'p1'))
    objects.append(Object(card_database[4], 3, 6, 'p1'))
    objects.append(Object(card_database[5], 6, 6, 'p1'))

drag_start_x = 0
drag_start_y = 0
def draw_objects():
    for obj in objects:
        window.blit(obj.card.image, (val.map_offset + obj.xpos * (val.square_size + val.seperator_size),
                                val.map_offset + obj.ypos * (val.square_size + val.seperator_size)))
        if obj.drag == True:
            drag_start_x = obj.xpos
            drag_start_y = obj.ypos

def drag_controller(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        print('clicked!')
        for object in objects:
            if object.rect.collidepoint(event.pos):
                object.drag = True
                break
        pygame.draw.line(window, val.color_green, event.pos, (drag_start_x, drag_start_y))
    elif event.type == pygame.MOUSEBUTTONUP:
        dragged = None


# def init_etc_objects():


def main():
    init_map()
    init_database()
    init_objects()
    while (True):
        for event in pygame.event.get():
            drag_controller(event)
        draw_objects()
        pygame.display.update()


main()
