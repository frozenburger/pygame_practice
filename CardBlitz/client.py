import os
import pygame
import CardBlitz.static_values as val
import pandas as pd
from CardBlitz.classes import *

# setup window
window = pygame.display.set_mode((val.window_width+val.interface_width, val.window_height))
pygame.display.set_caption("Card Blitz")

# in-game resource tracking
map = []
card_database = []
objects = []
player = Player('p1')


# global variables for dragging
drag_start_x = 0
drag_start_y = 0
dragging = False
drag_color = (0, 0, 0)



# --------------------------------------------------------------------------------
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
    for index, obj in enumerate(objects):
        if obj.hp_current <= 0:
            objects.pop(index)
    for obj in objects:
        window.blit(obj.card.image, (obj.xpos, obj.ypos))
        hp_bar_size = int(val.square_size*(obj.hp_current / obj.card.hp))
        max_hp_rect = (obj.xpos, obj.ypos + val.square_size - val.hp_bar_height, val.square_size, val.hp_bar_height)
        cur_hp_rect = (obj.xpos, obj.ypos + val.square_size - val.hp_bar_height, hp_bar_size, val.hp_bar_height)
        pygame.draw.rect(window, val.color_red, max_hp_rect)
        pygame.draw.rect(window, val.color_green, cur_hp_rect)

        team_border = (obj.xpos, obj.ypos, val.square_size, val.square_size - val.hp_bar_height)
        if obj.owner == 'p1':
            pygame.draw.rect(window, val.color_red_light, team_border, val.team_boundary_thickness)
        elif obj.owner == 'p2':
            pygame.draw.rect(window, val.color_blue_light, team_border, val.team_boundary_thickness)



'''
        boundary_ext = pygame.Surface((val.square_size, val.square_size-val.hp_bar_height)).fill(val.color_blue_dark)
        boundary_int = pygame.Surface((val.square_size-2*(val.team_boundary_thickness), val.square_size-val.hp_bar_height-2*(val.team_boundary_thickness)))
        boundary_int.set_alpha(0)
        boundary_ext.blit(boundary_int, (val.team_boundary_thickness, val.team_boundary_thickness))
        window.blit(boundary_ext, (obj.xpos, obj.ypos))
'''



def drag_controller(event):
    global objects, drag_color, dragging, drag_start_x, drag_start_y, player
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == val.left_mouse:
            for object in objects:
                if object.rect.collidepoint(event.pos) & (player.id == object.owner):
                    drag_color = val.color_green
                    dragging = True
                    object.drag = True
                    drag_start_x = object.xpos+50
                    drag_start_y = object.ypos+50
                    break
        elif event.button == val.right_mouse:
            for object in objects:
                if object.rect.collidepoint(event.pos) & (player.id == object.owner):
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
            # check if target location is valid
            if (dragging == True) & in_map(event.pos[0], event.pos[1]) & (is_empty(event.pos[0], event.pos[1])==False):
                for object in objects:
                    if object.rect.collidepoint(drag_start_x, drag_start_y):
                        attacker = object
                    if object.rect.collidepoint(event.pos[0], event.pos[1]):
                        defender = object
                        object.drag = False
                if attacker.owner != defender.owner:
                    print(defender.hp_current, attacker.card.atk)
                    if attacker != defender :
                        defender.hp_current -= attacker.card.atk
                    print(defender.hp_current, attacker.card.atk)
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
        pygame.draw.line(window, drag_color, pygame.mouse.get_pos(), (drag_start_x, drag_start_y), val.drag_line_thickness)

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
