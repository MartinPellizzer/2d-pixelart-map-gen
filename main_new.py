import os 

import copy
import pygame

import g
import ai
import utils

tile_size = 32
asset_pack_cur = ''
layer_cur = 0

assets_icons_clean = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'icons': [],
}

assets_icons = copy.deepcopy(assets_icons_clean)

level_map = {
    'row_num': 7,
    'col_num': 7,
    'row_active': 0,
    'col_active': 0,
    'tiles': []
}

level_map_tmp = {
    'row_num': 7,
    'col_num': 7,
    'row_active': 0,
    'col_active': 0,
    'tiles': []
}

#######################################
# ;frames
#######################################
camera = {
    'x': 0,
    'y': 0,
    'zoom': 4,
}

frame_left = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': g.WINDOW_H,
}

frame_assets_tabs = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': 30,
}

frame_assets_icons = {
    'x': 0,
    'y': frame_assets_tabs['h'],
    'w': assets_icons['icon_size'] * assets_icons['col_num'],
    'h': assets_icons['icon_size'] * assets_icons['row_num'],
}

frame_right = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': g.WINDOW_H,
}
frame_right['x'] = g.WINDOW_W - frame_right['w']

frame_center = {
    'x': frame_left['w'],
    'y': 0,
    'w': g.WINDOW_W - frame_left['w'] - frame_right['w'],
    'h': g.WINDOW_H,
}

frame_map = {
    'x': frame_center['x'],
    'y': frame_center['y'],
    'w': level_map['col_num'] * tile_size*camera['zoom'],
    'h': level_map['row_num'] * tile_size*camera['zoom'],
}

#######################################
# ;map+img
#######################################
pyimgs = []

def add_image_pygame(path):
    global pyimgs
    found = False
    for i, image_pygame in enumerate(pyimgs):
        if image_pygame['path'] == path:
            pyimgs[i] = {
                'path': path, 
                'img': pygame.image.load(path),
            }
            found = True
            break
    if not found:
        pyimgs.append({
            'path': path, 
            'img': pygame.image.load(path),
        })

def clear_level_map_tiles():
    level_map['tiles'] = []
    for i in range(level_map['row_num']):
        row = []
        for j in range(level_map['col_num']):
            row.append([None, None, None, None, None])
        level_map['tiles'].append(row)
        
def clear_level_map_tmp_tiles():
    level_map_tmp['tiles'] = []
    for i in range(level_map_tmp['row_num']):
        row = []
        for j in range(level_map_tmp['col_num']):
            row.append([None, None, None, None, None])
        level_map_tmp['tiles'].append(row)

clear_level_map_tiles()
clear_level_map_tmp_tiles()

'''
level_map['tiles'][0][0] = 'assets/characters/succubus.png'
level_map['tiles'][0][1] = 'assets/characters/zombie.png'
level_map['tiles'][0][2] = 'assets/characters/hellhound.png'
level_map['tiles'][1][0] = 'assets/characters/pharoh.png'
level_map['tiles'][1][1] = 'assets/characters/harpy.png'
level_map['tiles'][1][2] = 'assets/characters/slime.png'
add_image_pygame('assets/characters/succubus.png')
add_image_pygame('assets/characters/zombie.png')
add_image_pygame('assets/characters/hellhound.png')
add_image_pygame('assets/characters/pharoh.png')
add_image_pygame('assets/characters/harpy.png')
add_image_pygame('assets/characters/slime.png')
'''

def clear_asset_pack():
    global assets_icons
    assets_icons = copy.deepcopy(assets_icons_clean)
    for i in range(assets_icons['row_num']):
        row = []
        for j in range(assets_icons['col_num']):
            row.append(None)
        assets_icons['icons'].append(row)

def load_asset_pack(foldername):
    global assets_icons
    global asset_pack_cur
    asset_pack_cur = foldername
    row_active = assets_icons['row_active']
    col_active = assets_icons['col_active']
    clear_asset_pack()
    assets_filepaths = [f'assets/{foldername}/{filename}' for filename in os.listdir(f'assets/{foldername}')]
    for i in range(15):
        for j in range(5):
            asset_index_cur = i*5+j
            asset_id = utils.format_id(asset_index_cur)
            for asset_filepath in assets_filepaths:
                asset_filepath_id = asset_filepath.split('/')[-1].split('.')[0]
                if asset_id in asset_filepath_id:
                    assets_icons['icons'][i][j] = asset_filepath
                    add_image_pygame(asset_filepath)
                    break
    assets_icons['row_active'] = row_active
    assets_icons['col_active'] = col_active

clear_asset_pack()

def get_pyimg_by_path(path):
    img = None
    for obj in pyimgs:
        if obj['path'] == path:
            img = obj['img']
            break
    return img

#######################################################
# ;pygame
#######################################################
pygame.init()

screen = pygame.display.set_mode([g.WINDOW_W, g.WINDOW_H])

def draw_frame_left_tabs():
    font = pygame.font.SysFont('Arial', 16)
    x = frame_assets_tabs['x']
    y = frame_assets_tabs['y']
    w = frame_assets_tabs['w']
    h = frame_assets_tabs['h']
    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    tab_i = -1
    tab_w = 80
    for tab_i in range(2):
        x = frame_assets_tabs['x'] + tab_w*tab_i
        y = frame_assets_tabs['y']
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, tab_w, h), 1)
        text_surface = font.render(f'pack {tab_i}', False, (255, 255, 255))
        screen.blit(text_surface, (x + 10, y + 5))

def draw_frame_left_icons():
    # draw icons background
    for row_num in range(assets_icons['row_num']):
        for col_num in range(assets_icons['col_num']):
            # background
            x = frame_assets_icons['x'] + assets_icons['icon_size']*col_num + 1
            y = frame_assets_icons['y'] + assets_icons['icon_size']*row_num + 1
            w = assets_icons['icon_size'] - 1
            h = assets_icons['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    # draw icons images
    for i in range(assets_icons['row_num']):
        for j in range(assets_icons['col_num']):
            img_path = assets_icons['icons'][i][j]
            if img_path != None:
                img = get_pyimg_by_path(img_path)
                img = pygame.transform.scale(img, (assets_icons['icon_size'], assets_icons['icon_size']))
                x = frame_assets_icons['x'] + assets_icons['icon_size']*j
                y = frame_assets_icons['y'] + assets_icons['icon_size']*i
                screen.blit(img, (x, y))
    # draw icons outline active cell
    for row_num in range(assets_icons['row_num']):
        for col_num in range(assets_icons['col_num']):
            if row_num == assets_icons['row_active'] and col_num == assets_icons['col_active']:
                x = frame_assets_icons['x'] + assets_icons['icon_size']*col_num + 1
                y = frame_assets_icons['y'] + assets_icons['icon_size']*row_num + 1
                w = assets_icons['icon_size'] - 1
                h = assets_icons['icon_size'] - 1
                pygame.draw.rect(screen, '#ff00ff', pygame.Rect(x, y, w, h), 1,)
    # outline frame icons
    x = frame_assets_icons['x']
    y = frame_assets_icons['y']
    w = frame_assets_icons['w']
    h = frame_assets_icons['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h,), 1,)

def draw_frame_left():
    pygame.draw.rect(
        screen, '#202020', 
        pygame.Rect(frame_assets_icons['x'], frame_assets_icons['y'], frame_assets_icons['w'], frame_assets_icons['h'])
    )
    draw_frame_left_tabs()
    draw_frame_left_icons()
    x = frame_left['x']
    y = frame_left['y']
    w = frame_left['w']
    h = frame_left['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_map_tiles():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            img_path = level_map['tiles'][i][j][0]
            if img_path != None:
                img = get_pyimg_by_path(img_path)
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = frame_center['x'] + w*j + camera['x']
                y = frame_center['y'] + h*i + camera['y']
                img = pygame.transform.scale(img, (w, h))
                screen.blit(img, (x, y))
            img_path = level_map['tiles'][i][j][1]
            if img_path != None:
                img = get_pyimg_by_path(img_path)
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = frame_center['x'] + w*j + camera['x']
                y = frame_center['y'] + h*i + camera['y']
                img = pygame.transform.scale(img, (w, h))
                screen.blit(img, (x, y))


def draw_map_grid():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera['zoom']
            h = tile_size*camera['zoom']
            x = frame_center['x'] + w*j + camera['x']
            y = frame_center['y'] + h*i + camera['y']
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)

    font = pygame.font.SysFont('Arial', 24)
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera['zoom']
            h = tile_size*camera['zoom']
            x = frame_center['x'] + w*j + camera['x']
            y = frame_center['y'] + h*i + camera['y']
            text_surface = font.render(f'{i} - {j}', False, (255, 0, 255))
            screen.blit(text_surface, (x, y))

def draw_frame_right():
    x = frame_right['x']
    y = frame_right['y']
    w = frame_right['w']
    h = frame_right['h']
    pygame.draw.rect(screen, '#202020', pygame.Rect(x, y, w, h))
    draw_debug()
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def get_map_tile_coords():
    row_index = -1
    col_index = -1
    x1 = frame_map['x']
    y1 = frame_map['y']
    x2 = frame_map['x'] + frame_map['w']
    y2 = frame_map['y'] + frame_map['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        col_index = (mouse['x'] - frame_center['x']) // (tile_size*camera['zoom'])
        row_index = (mouse['y'] - frame_center['y']) // (tile_size*camera['zoom'])
    return row_index, col_index
    

def draw_debug():
    x = frame_right['x']
    y = frame_right['y']
    w = frame_right['w']
    h = frame_right['h']
    font = pygame.font.SysFont('Arial', 24)
    y += 24
    text_surface = font.render(f'{mouse["x"]} - {mouse["y"]}', False, (255, 0, 255))
    screen.blit(text_surface, (x, y))
    y += 24
    i, j = get_map_tile_coords()
    text_surface = font.render(f'MAP CELL COORD: {i} / {j}', False, (255, 0, 255))
    screen.blit(text_surface, (x, y))
    y += 24
    i = level_map['row_active']
    j = level_map['col_active']
    text_surface = font.render(f'MAP CELL ACTIVE: {i} / {j}', False, (255, 0, 255))
    screen.blit(text_surface, (x, y))

def draw_main():
    # window bg
    screen.fill('#101010')

    # left frame
    draw_frame_left()
    # central frame
    draw_map_grid()
    draw_map_tiles()
    # left frame
    draw_frame_right()

    draw_tile_dragging()
    delete_tile_dragging()
    # draw
    pygame.display.flip()

mouse = {
    'x': 0,
    'y': 0,
    'left_click_old': -1,
    'left_click_cur': 0,
    'right_click_old': -1,
    'right_click_cur': 0,
}

def click_asset_tab():
    global layer_cur
    i = 0
    print('    frame assets tabs')
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('        frame assets tab {i}')
        load_asset_pack('textures')
        layer_cur = 0
    i += 1
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('        frame assets tab {i}')
        load_asset_pack('characters')
        layer_cur = 1

def click_asset_icon():
    x1 = frame_assets_icons['x']
    y1 = frame_assets_icons['y']
    x2 = frame_assets_icons['x'] + frame_assets_icons['w']
    y2 = frame_assets_icons['y'] + frame_assets_icons['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('    frame assets icons')
        col_index = (mouse['x'] - frame_assets_icons['x']) // assets_icons['icon_size']
        print(col_index)
        assets_icons['col_active'] = col_index
        row_index = (mouse['y'] - frame_assets_icons['y']) // assets_icons['icon_size']
        print(row_index)
        assets_icons['row_active'] = row_index

def get_tile_coords(x, y):
    col_index = (x - frame_center['x']) // (tile_size*camera['zoom'])
    row_index = (y - frame_center['y']) // (tile_size*camera['zoom'])
    return row_index, col_index

def click_map_tile():
    x1 = frame_map['x']
    y1 = frame_map['y']
    x2 = frame_map['x'] + frame_map['w']
    y2 = frame_map['y'] + frame_map['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('frame center')

        col_index = (mouse['x'] - frame_center['x']) // (tile_size*camera['zoom'])
        print(col_index)
        level_map['col_active'] = col_index

        row_index = (mouse['y'] - frame_center['y']) // (tile_size*camera['zoom'])
        print(row_index)
        level_map['row_active'] = row_index

        i = assets_icons['row_active']
        j = assets_icons['col_active']
        tile_filepath = assets_icons['icons'][i][j]

        i = level_map['row_active']
        j = level_map['col_active']
        level_map['tiles'][i][j][layer_cur] = tile_filepath

def draw_tile_dragging():
    if dragging == True:
        x1 = frame_map['x']
        y1 = frame_map['y']
        x2 = frame_map['x'] + frame_map['w']
        y2 = frame_map['y'] + frame_map['h']
        row_index_start, col_index_start = get_tile_coords(dragging_start_x, dragging_start_y)
        row_index_end, col_index_end = get_tile_coords(mouse['x'], mouse['y'])
        if row_index_end < row_index_start: row_index_end = row_index_start
        if col_index_end < col_index_start: col_index_end = col_index_start
        
        x = dragging_start_x
        y = dragging_start_y
        w = mouse['x'] - dragging_start_x
        h = mouse['y'] - dragging_start_y
        pygame.draw.rect(screen, '#202020', pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

        clear_level_map_tmp_tiles()

        for i in range(level_map_tmp['row_num']):
            for j in range(level_map_tmp['col_num']):
                if i >= row_index_start and j >= col_index_start and i <= row_index_end and j <= col_index_end:
                    asset_row_cur = assets_icons['row_active']
                    asset_col_cur = assets_icons['col_active']
                    img_path = assets_icons['icons'][asset_row_cur][asset_col_cur]
                    level_map_tmp['tiles'][i][j][layer_cur] = img_path
                    if img_path != None:
                        img = get_pyimg_by_path(img_path)
                        w = tile_size*camera['zoom']
                        h = tile_size*camera['zoom']
                        x = frame_center['x'] + w*j + camera['x']
                        y = frame_center['y'] + h*i + camera['y']
                        img = pygame.transform.scale(img, (w, h))
                        screen.blit(img, (x, y))

def delete_tile_dragging():
    if dragging_right == True:
        x1 = frame_map['x']
        y1 = frame_map['y']
        x2 = frame_map['x'] + frame_map['w']
        y2 = frame_map['y'] + frame_map['h']
        row_index_start, col_index_start = get_tile_coords(dragging_start_x, dragging_start_y)
        row_index_end, col_index_end = get_tile_coords(mouse['x'], mouse['y'])
        if row_index_end < row_index_start: row_index_end = row_index_start
        if col_index_end < col_index_start: col_index_end = col_index_start
        
        x = dragging_start_x
        y = dragging_start_y
        w = mouse['x'] - dragging_start_x
        h = mouse['y'] - dragging_start_y
        pygame.draw.rect(screen, '#202020', pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

        clear_level_map_tmp_tiles()

        for i in range(level_map_tmp['row_num']):
            for j in range(level_map_tmp['col_num']):
                if i >= row_index_start and j >= col_index_start and i <= row_index_end and j <= col_index_end:
                    img_path = None
                    level_map_tmp['tiles'][i][j][layer_cur] = img_path
                    w = tile_size*camera['zoom']
                    h = tile_size*camera['zoom']
                    x = frame_center['x'] + w*j + camera['x']
                    y = frame_center['y'] + h*i + camera['y']
                    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,),)
                    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)
                else:
                    img_path = 'do not del'
                    level_map_tmp['tiles'][i][j][layer_cur] = img_path


dragging = False
dragging_right = False
dragging_start_x = 0
dragging_start_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if asset_pack_cur == 'characters':
                    ai.gen_image(
                        assets_icons['row_active'], assets_icons['col_active'], 
                        assets_pack='characters',
                        prompt='pixel art, 1girl, chibi, succubus',
                    )
                    ai.bg_remove(
                        assets_icons['row_active'], assets_icons['col_active'], 
                        assets_pack='characters',
                    )
                    load_asset_pack('characters')
                elif asset_pack_cur == 'textures':
                    ai.gen_image(
                        assets_icons['row_active'], assets_icons['col_active'], 
                        assets_pack='textures',
                        prompt='pixel art, grass tile texture',
                    )
                    load_asset_pack('textures')
                else:
                    load_asset_pack('')

    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]
    mouse['right_click_cur'] = pygame.mouse.get_pressed()[2]

    # mouse left
    if mouse['left_click_cur'] == True:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            click_asset_tab()
            click_asset_icon()
            # click_map_tile()
            
            dragging = True
            dragging_start_x = mouse['x']
            dragging_start_y = mouse['y']

    # mouse left
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            dragging = False
            for i in range(level_map_tmp['row_num']):
                for j in range(level_map_tmp['col_num']):
                    img_path = level_map_tmp['tiles'][i][j][layer_cur]
                    if img_path != None:
                        level_map['tiles'][i][j][layer_cur] = img_path

    if mouse['right_click_cur'] == True:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            dragging_right = True
            dragging_start_x = mouse['x']
            dragging_start_y = mouse['y']
    else:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            dragging_right = False
            for i in range(level_map_tmp['row_num']):
                for j in range(level_map_tmp['col_num']):
                    img_path = level_map_tmp['tiles'][i][j][layer_cur]
                    if img_path != 'do not del':
                        level_map['tiles'][i][j][layer_cur] = img_path

    draw_main()

pygame.quit()
