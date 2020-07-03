import os

import pygame
from pygame import event
import CardBlitz.static_values as val
import pandas as pd

# setup window
window = pygame.display.set_mode((val.window_width, val.window_height))
pygame.display.set_caption("Card Blitz")

# in-game resource tracking
map = []
card_database = []
objects = {}

# --------------------------------------------------------------------------------

# properties of a card
class card():
    def __init__(self, id, name, atk, range, hp, spd, image, x, y):
        self.id = id
        self.name = name
        self.atk = atk
        self.range = range
        self.hp = hp
        self.spd = spd
        self.image = image
        self.x = x # in-class coordinates store single digit numbers
        self.y = y # in-class coordinates store single digit numbers



# visualize map
def init_map():
    window.fill(val.color_black)
    for i in range(7):
        map.append([])
        for j in range(7):
            map[i].append([i*val.square_size, j*val.square_size])
            pygame.draw.rect(window, val.color_white,
                (val.map_offset+i*(val.square_size+val.seperator_size),
                 val.map_offset+j*(val.square_size+val.seperator_size),
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
        new_card = card(index, row['name'], row['attack'], row['range'], row['health'], row['speed'], image_list[index], 0, 0)
        card_database.append(new_card)

def init_objects():
    objects['p1'] = [card_database[0], card_database[1], card_database[2]]
    objects['p2'] = [card_database[3], card_database[4], card_database[5]]
    objects['etc'] = []
    objects['p2'][0].x, objects['p2'][0].y = 0, 0
    objects['p2'][1].x, objects['p2'][1].y = 3, 0
    objects['p2'][2].x, objects['p2'][2].y = 6, 0
    objects['p1'][0].x, objects['p1'][0].y = 0, 6
    objects['p1'][1].x, objects['p1'][1].y = 3, 6
    objects['p1'][2].x, objects['p1'][2].y = 6, 6

def draw_objects():
    for obj in objects['p1']:
        window.blit(obj.image, (val.map_offset+obj.x*(val.square_size+val.seperator_size), val.map_offset+obj.y*(val.square_size+val.seperator_size)))
    for obj in objects['p2']:
        window.blit(obj.image, (val.map_offset+obj.x*(val.square_size+val.seperator_size), val.map_offset+obj.y*(val.square_size+val.seperator_size)))

'''
def drag_controller():
    if event.type == pygame.MOUSEBUTTONDOWN:
        for object in objects:
            if object.rect.collidepoint(event.pos):
                dragged = draggable
                break
    elif event.type == pygame.MOUSEBUTTONUP:
        dragged = None
        '''



# def init_etc_objects():



def main():
    init_map()
    init_database()
    init_objects()
    while(True):
        event.get()
        draw_objects()
        pygame.display.update()
main()