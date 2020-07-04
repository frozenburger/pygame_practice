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

# global variables for dragging
drag_start_x = 0
drag_start_y = 0
dragging = False
drag_color = (0, 0, 0)



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
        self.rect = pygame.rect.Rect(xpos, ypos, val.square_size, val.square_size)

    # visualize map


def draw_map():
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
    global objects
    objects.append(Object(card_database[0], val.map_offset+0*(val.square_size+val.seperator_size), val.map_offset+0*(val.square_size+val.seperator_size), 'p2'))
    objects.append(Object(card_database[1], val.map_offset+3*(val.square_size+val.seperator_size), val.map_offset+0*(val.square_size+val.seperator_size), 'p2'))
    objects.append(Object(card_database[2], val.map_offset+6*(val.square_size+val.seperator_size), val.map_offset+0*(val.square_size+val.seperator_size), 'p2'))
    objects.append(Object(card_database[3], val.map_offset+0*(val.square_size+val.seperator_size), val.map_offset+6*(val.square_size+val.seperator_size), 'p1'))
    objects.append(Object(card_database[4], val.map_offset+3*(val.square_size+val.seperator_size), val.map_offset+6*(val.square_size+val.seperator_size), 'p1'))
    objects.append(Object(card_database[5], val.map_offset+6*(val.square_size+val.seperator_size), val.map_offset+6*(val.square_size+val.seperator_size), 'p1'))



def draw_objects():
    global objects
    for obj in objects:
        window.blit(obj.card.image, (obj.xpos, obj.ypos))

def drag_controller(event):
    global objects, drag_color, dragging, drag_start_x, drag_start_y
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == val.left_mouse:
            for object in objects:
                if object.rect.collidepoint(event.pos):
                    drag_color = val.color_green
                    dragging = True
                    object.drag = True
                    drag_start_x = object.xpos+50
                    drag_start_y = object.ypos+50
                    break
        elif event.button == val.right_mouse:
            for object in objects:
                if object.rect.collidepoint(event.pos):
                    drag_color = val.color_red
                    dragging = True
                    object.drag = True
                    drag_start_x = object.xpos+50
                    drag_start_y = object.ypos+50
                    break
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == val.left_mouse:
            if (dragging == True) & in_map(event.pos[0], event.pos[1]) & is_empty(event.pos[0], event.pos[1]):
                for object in objects:
                    # find object at start of dragging
                    if object.rect.collidepoint(drag_start_x, drag_start_y):
                        # and set its position to event.pos
                        object.xpos, object.ypos = snap_to_grid(event.pos[0], event.pos[1])
                        object.rect = pygame.rect.Rect(object.xpos, object.ypos, val.square_size, val.square_size)
                        object.drag = False
                        break
            dragging = False
        elif event.button == val.right_mouse:
            if (dragging == True) & in_map(event.pos[0], event.pos[1]) & is_empty(event.pos[0], event.pos[1]):
                for object in objects:
                    # find object at start of dragging
                    if object.rect.collidepoint(drag_start_x, drag_start_y):
                        # and set its position to event.pos
                        object.xpos, object.ypos = snap_to_grid(event.pos[0], event.pos[1])
                        object.rect = pygame.rect.Rect(object.xpos, object.ypos, val.square_size, val.square_size)
                        object.drag = False
                        break
            dragging = False


def in_map(xpos, ypos):
     x_cond = (val.map_offset < xpos) & (xpos < val.map_offset + (val.square_size + val.seperator_size) * 7)
     y_cond = (val.map_offset < ypos) & (ypos < val.map_offset + (val.square_size + val.seperator_size) * 7)
     return x_cond & y_cond

def is_empty(xpos, ypos):
    global objects
    result = True
    for object in objects:
        if object.rect.collidepoint(xpos, ypos):
            result = False
    return result

def draw_line():
    global window, drag_color, drag_start_x, drag_start_y
    if dragging:
        pygame.draw.line(window, drag_color, pygame.mouse.get_pos(), (drag_start_x, drag_start_y), 5)

def snap_to_grid(xpos, ypos):
    x_num = (xpos-val.map_offset) // (val.seperator_size + val.square_size)
    y_num = (ypos-val.map_offset) // (val.seperator_size + val.square_size)
    xpos = x_num * (val.seperator_size + val.square_size) + val.map_offset
    ypos = y_num * (val.seperator_size + val.square_size) + val.map_offset
    return xpos, ypos


# def init_etc_objects():


def main():
    init_database()
    init_objects()
    while (True):
        draw_map()
        for event in pygame.event.get():
            drag_controller(event)
        draw_objects()
        draw_line()
        pygame.display.update()


main()
