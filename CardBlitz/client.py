import os
import pygame
import CardBlitz.static_values as val
import pandas as pd
import socket
import threading
from CardBlitz.classes import *


# setup window
window = pygame.display.set_mode((val.window_width+val.interface_width, val.window_height))
pygame.display.set_caption("Card Blitz")
pygame.font.init()
font_arial = pygame.font.SysFont('arial', 20)

# in-game resource tracking
map = []
card_database = []
objects = []
ui_images = []

# turn tracking
player = Player('p1')
opponent = Player('p2')
turn_player = 'p1'

# global variables for clicking & dragging
drag_start_x = 0
drag_start_y = 0
dragging = False
drag_color = (0, 0, 0)
clicked_object = ''

# networking variables
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
    for image_file in os.listdir(os.path.join(os.getcwd(), 'data', 'img', 'cards')):
        img = pygame.image.load(os.path.join(os.getcwd(), 'data', 'img', 'cards', image_file)).convert()
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

def init_interface():
    global ui_images
    path = os.path.join(os.getcwd(), 'data', 'img', 'ui')
    for image in os.listdir(path):
        img = pygame.image.load(os.path.join(path, image)).convert()
        ui_images.append(img)

def draw_interface():
    global ui_images
    global font_arial
    ui_resources = pygame.Surface((val.interface_width, val.interface_resources_height))

    icon_attack = pygame.transform.scale(ui_images[0], (50, 50))
    icon_move = pygame.transform.scale(ui_images[1], (50, 50))
    icon_skill = pygame.transform.scale(ui_images[2], (50, 50))
    ui_resources.blit(icon_attack, (75, 100))
    ui_resources.blit(icon_move, (75, 200))
    ui_resources.blit(icon_skill, (75, 300))

    text_attack = font_arial.render("Attack Tokens : {}".format(player.resources['attack_tokens']), True, val.color_white)
    text_move = font_arial.render("Movement Tokens : {}".format(player.resources['move_tokens']), True, val.color_white)
    text_skill = font_arial.render("Skill Tokens : {}".format(player.resources['skill_tokens']), True, val.color_white)
    ui_resources.blit(text_attack,(150, 112))
    ui_resources.blit(text_move, (150, 212))
    ui_resources.blit(text_skill, (150, 312))

    # blit resource panel
    window.blit(ui_resources, (800, 200))

    # blit next_turn button
    myFont = pygame.font.SysFont('arial', 30)
    myFont.set_bold(True)
    text_nextTurn = myFont.render("NEXT TURN", True, val.color_black)
    window.blit(ui_images[3], (900, 625))
    window.blit(text_nextTurn, (915, 645))

'''
def keydown_controller(event):
    global player, opponent, turn_player
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if player.id == 'p1':
                player.id = 'p2'
                opponent.id = 'p1'
            elif player.id == 'p2':
                player.id = 'p1'
                opponent.id = 'p2'
        elif event.key == pygame.K_BACKSPACE:
            print(player.id, opponent.id, 'current turn:', turn_player)
            for i in player.resources.keys():
                print(player.resources[i])
            for i in opponent.resources.keys():
                print(opponent.resources[i])
'''

def drag_controller(event):
    global objects, drag_color, dragging, drag_start_x, drag_start_y, player, turn_player, clicked_object
    if event.type == pygame.MOUSEBUTTONDOWN:
        # if clicked location was inside the grid
        if pygame.rect.Rect(0, 0, val.window_width, val.window_height).collidepoint(event.pos):
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
        # if clicked location was on the UI
        elif pygame.rect.Rect(val.window_width, 0, val.interface_width, val.window_height).collidepoint(event.pos):
            # if clicked on NEXT_TURN button
            if pygame.rect.Rect(900, 625, 200, 75).collidepoint(event.pos):
                print('next turn button!')
                clicked_object = 'NEXT_TURN'
            # NEXT TURN
            pass
    elif event.type == pygame.MOUSEBUTTONUP:
        if pygame.rect.Rect(0, 0, val.window_width, val.window_height).collidepoint(event.pos):
            if event.button == val.left_mouse:
                if (dragging == True) & in_map(event.pos[0], event.pos[1]) & is_empty(event.pos[0], event.pos[1]):
                    for object in objects:
                        # find object at start of dragging
                        if object.rect.collidepoint(drag_start_x, drag_start_y):
                            # and set its position to event.pos
                            # if you are turn player
                            if player.id == turn_player:
                                # if you have a move token
                                if player.resources['move_tokens'] > 0:
                                    object.drag = False
                                    command_move((object.xpos, object.ypos), event.pos)
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
                        if attacker != defender :
                            #if you are turn player
                            if player.id == turn_player:
                                # if you have an attack token
                                if player.resources['attack_tokens'] > 0:
                                    defender.hp_current -= attacker.card.atk
                                    player.resources['attack_tokens'] -= 1
                dragging = False
        elif pygame.rect.Rect(val.window_width, 0, val.interface_width, val.window_height).collidepoint(event.pos):
            # if clicked on NEXT_TURN button
            if pygame.rect.Rect(900, 625, 200, 75).collidepoint(event.pos):
                if clicked_object == 'NEXT_TURN':
                    if player.id == turn_player:
                        clicked_object = ''
                        change_turn()


def command_move(target, destination):
    global objects, player, client
    for object in objects:
        if object.rect.collidepoint(target[0], target[1]):
            object.xpos, object.ypos = snap_to_grid(destination[0], destination[1])
            object.rect = pygame.rect.Rect(object.xpos, object.ypos, val.square_size, val.square_size)
            player.resources['move_tokens'] -= 1
            break
    send_message(client, ','.join(('move',str(target), str(destination))))

def change_turn():
    global turn_player, player, opponent
    print('inside change_turn : ')
    if turn_player == player.id:
        # change turn and refill tokens
        turn_player = opponent.id
        opponent.resources['attack_tokens'] = 2
        opponent.resources['move_tokens'] = 3
        opponent.resources['skill_tokens'] = 0
        print('next turn! {}'.format(turn_player))
    elif turn_player == opponent.id:
        # change turn and refill tokens
        turn_player = player.id
        player.resources['attack_tokens'] = 2
        player.resources['move_tokens'] = 3
        player.resources['skill_tokens'] = 0
        print('next turn!2 {}'.format(turn_player))



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


def init_networking():
    global client
    server = val.server2
    port = val.port
    client.connect((server, port))
    thread = threading.Thread(target=receive_data, args=(client, (server, port)))
    thread.start()

def receive_data(conn, addr):
    print('starting thread')
    connected = True
    while connected:
        header = conn.recv(val.header_len).decode(val.utf8)
        print(header)
        if header != '':
            msg_len = int(header)
            msg = conn.recv(msg_len).decode(val.utf8)
            if msg.split(',')[0] == 'move':
                print(msg)

def send_message(conn, msg_string):
    message = msg_string.encode(val.utf8)
    msg_len = len(message)

    # pad header into max length
    header = str(msg_len).encode(val.utf8)
    header += b' '*(val.header_len - len(header))

    conn.send(header)
    conn.send(message)


def main():
    global client
    init_database()
    init_objects()
    init_interface()

    init_networking()
    send_message(client, 'Hello World from client!')
    while (True):
        draw_map()
        draw_interface()
        for event in pygame.event.get():
            drag_controller(event)
            #keydown_controller(event)
        draw_objects()
        draw_line()
        pygame.display.update()


main()
