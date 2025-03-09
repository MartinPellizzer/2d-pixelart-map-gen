import os 
import json

import copy
import pygame

import g
import f
import ai
import utils

tile_size = 32
asset_pack_cur = ''
layer_cur = 0

asset_pack_name = f'characters'
asset_pack_folderpath = f'assets/{asset_pack_name}'
asset_pack_images_folderpath = f'{asset_pack_folderpath}/images'
asset_pack_jsons_folderpath = f'{asset_pack_folderpath}/jsons'
asset_pack_images_filepaths = [f'{asset_pack_images_folderpath}/{filename}' for filename in os.listdir(asset_pack_images_folderpath)]
asset_pack_jsons_filepaths = [f'{asset_pack_jsons_folderpath}/{filename}' for filename in os.listdir(asset_pack_jsons_folderpath)]

pannel_assets = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'assets': [],
}


assets_packs = []
'''
asset_pack_1 = load_asset_pack('assets/textures')
asset_pack_2 = load_asset_pack('assets/characters')
assets_packs.append(asset_pack_1)
assets_packs.append(asset_pack_2)
'''

pannel_assets_clean = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'assets': [],
}

# pannel_assets = copy.deepcopy(pannel_assets_clean)

ex_tile = {
    'image_path': '',
    'x_offset': '',
    'y_offset': '',
}

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

frame_assets_tabs = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': 30,
}

frame_pannel_assets = {
    'x': 0,
    'y': frame_assets_tabs['h'],
    'w': pannel_assets['icon_size'] * pannel_assets['col_num'],
    'h': pannel_assets['icon_size'] * pannel_assets['row_num'],
}

frame_center = {
    'x': f.left['w'],
    'y': 0,
    'w': g.WINDOW_W - f.left['w'] - f.right['w'],
    'h': g.WINDOW_H,
}

frame_map = {
    'x': frame_center['x'],
    'y': frame_center['y'],
    'w': level_map['col_num'] * tile_size*camera['zoom'],
    'h': level_map['row_num'] * tile_size*camera['zoom'],
}

frame_prompt = {
    'x': 0,
    'y': frame_pannel_assets['y'] + frame_pannel_assets['h'],
    'w': pannel_assets['icon_size'] * pannel_assets['col_num'],
    'h': 30,
}

prompt = {
    'text': 'pixel art, ',
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

def clear_asset_pack():
    global pannel_assets
    pannel_assets = copy.deepcopy(pannel_assets_clean)
    for i in range(pannel_assets['row_num']):
        row = []
        for j in range(pannel_assets['col_num']):
            row.append({'image_filepath': None, 'x_offset': 0, 'y_offset': 0})
        pannel_assets['assets'].append(row)

def load_asset_pack(foldername):
    global pannel_assets
    _assets_filepaths = [f'assets/{foldername}/jsons/{filename}' for filename in os.listdir(f'assets/{foldername}/jsons')]
    _assets = []
    # clear 
    _assets = []
    for i in range(pannel_assets['row_num']):
        row = []
        for j in range(pannel_assets['col_num']):
            row.append({'image_filepath': None, 'x_offset': 0, 'y_offset': 0})
        _assets.append(row)
    # fill
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            _asset_index_cur = i*pannel_assets['col_num']+j
            _asset_id = utils.format_id(_asset_index_cur)
            for _asset_filepath in _assets_filepaths:
                _asset_filepath_id = _asset_filepath.split('/')[-1].split('.')[0]
                if _asset_id in _asset_filepath_id:
                    with open(_asset_filepath) as f: json_asset = json.load(f)
                    _assets[i][j] = json_asset
                    add_image_pygame(json_asset['image_filepath'])
                    break
    return _assets

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
font_arial_16 = pygame.font.SysFont('Arial', 16)

def draw_frame_left_tabs():
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
        text_surface = font_arial_16.render(f'pack {tab_i}', False, (255, 255, 255))
        screen.blit(text_surface, (x + 10, y + 5))

def draw_frame_left_icons_old():
    # draw icons background
    for row_num in range(pannel_assets['row_num']):
        for col_num in range(pannel_assets['col_num']):
            x = frame_pannel_assets['x'] + pannel_assets['icon_size']*col_num + 1
            y = frame_pannel_assets['y'] + pannel_assets['icon_size']*row_num + 1
            w = pannel_assets['icon_size'] - 1
            h = pannel_assets['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    # draw icons images
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            img_path = pannel_assets['assets'][i][j]['image_filepath']
            if img_path != None:
                img = get_pyimg_by_path(img_path)
                img = pygame.transform.scale(img, (pannel_assets['icon_size'], pannel_assets['icon_size']))
                x = frame_pannel_assets['x'] + pannel_assets['icon_size']*j
                y = frame_pannel_assets['y'] + pannel_assets['icon_size']*i
                screen.blit(img, (x, y))
    # draw icons outline active cell
    for row_num in range(pannel_assets['row_num']):
        for col_num in range(pannel_assets['col_num']):
            if row_num == pannel_assets['row_active'] and col_num == pannel_assets['col_active']:
                x = frame_pannel_assets['x'] + pannel_assets['icon_size']*col_num + 1
                y = frame_pannel_assets['y'] + pannel_assets['icon_size']*row_num + 1
                w = pannel_assets['icon_size'] - 1
                h = pannel_assets['icon_size'] - 1
                pygame.draw.rect(screen, '#ff00ff', pygame.Rect(x, y, w, h), 1,)
    # outline frame icons
    x = frame_pannel_assets['x']
    y = frame_pannel_assets['y']
    w = frame_pannel_assets['w']
    h = frame_pannel_assets['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h,), 1,)

def draw_frame_left_icons_background():
    for row_num in range(pannel_assets['row_num']):
        for col_num in range(pannel_assets['col_num']):
            x = frame_pannel_assets['x'] + pannel_assets['icon_size']*col_num + 1
            y = frame_pannel_assets['y'] + pannel_assets['icon_size']*row_num + 1
            w = pannel_assets['icon_size'] - 1
            h = pannel_assets['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))

def draw_frame_left_icons():
    draw_frame_left_icons_background()
    # draw icons images
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            img_path = pannel_assets['assets'][i][j]['image_filepath']
            if img_path != None:
                img = get_pyimg_by_path(img_path)
                img = pygame.transform.scale(img, (pannel_assets['icon_size'], pannel_assets['icon_size']))
                x = frame_pannel_assets['x'] + pannel_assets['icon_size']*j
                y = frame_pannel_assets['y'] + pannel_assets['icon_size']*i
                screen.blit(img, (x, y))

def draw_frame_left_prompt():
    x = frame_prompt['x']
    y = frame_prompt['y']
    w = frame_prompt['w']
    h = frame_prompt['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h,), 1,)
    text_surface = font_arial_16.render(prompt['text'], False, (255, 255, 255))
    screen.blit(text_surface, (x, y))

def draw_frame_left():
    pygame.draw.rect(
        screen, '#202020', 
        pygame.Rect(frame_pannel_assets['x'], frame_pannel_assets['y'], frame_pannel_assets['w'], frame_pannel_assets['h'])
    )
    draw_frame_left_tabs()
    draw_frame_left_icons()
    x = f.left['x']
    y = f.left['y']
    w = f.left['w']
    h = f.left['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    draw_frame_left_prompt()

def get_asset_by_filepath(filepath):
    asset = None
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            _asset = pannel_assets['assets'][i][j]
            if filepath == _asset['image_filepath']:
                asset = _asset
                break
    return asset

def flatten_matrix(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list

def get_asset(assets_packs, image_filepath):
    asset = None
    for asset_pack in assets_packs:
        pack_name = asset_pack['pack_name']
        if pack_name == image_filepath.split('/')[1]:
            assets = asset_pack['assets']
            assets = flatten_matrix(assets)
            found = False
            for _asset in assets:
                if image_filepath == _asset['image_filepath']:
                    asset = _asset
                    found = True
                    break
            if found == True: 
                break
    return asset
    
def draw_map_tiles():
    # textures
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
    # characters
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            img_path = level_map['tiles'][i][j][1]
            if img_path != None:
                asset = get_asset(assets_packs, img_path)
                img = get_pyimg_by_path(img_path)
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = frame_center['x'] + w*j + camera['x'] + asset['x_offset']
                y = frame_center['y'] + h*i + camera['y'] + asset['y_offset']
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

def draw_debug():
    x = f.right['x']
    y = f.right['y']
    w = f.right['w']
    h = f.right['h']
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

def draw_frame_right():
    x = f.right['x']
    y = f.right['y']
    w = f.right['w']
    h = f.right['h']
    pygame.draw.rect(screen, '#202020', pygame.Rect(x, y, w, h))
    # draw_debug()

    i = pannel_assets['row_active']
    j = pannel_assets['col_active']
    json_asset_focus = pannel_assets['assets'][i][j]

    text_surface = font_arial_16.render(f'X_OFF: {json_asset_focus["x_offset"]}', False, (255, 255, 255))
    screen.blit(text_surface, (x, y))

    rect_w, rect_h = 32, 32
    rect_x = f.right['x'] + f.right['w'] - rect_w
    rect_y = y
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(rect_x, rect_y, rect_w, rect_h), 1)
    text_surface = font_arial_16.render(f'+', False, (255, 255, 255))
    screen.blit(text_surface, (rect_x+12, rect_y+6))

    rect_w, rect_h = 32, 32
    rect_x = f.right['x'] + f.right['w'] - rect_w*2
    rect_y = y
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(rect_x, rect_y, rect_w, rect_h), 1)
    text_surface = font_arial_16.render(f'-', False, (255, 255, 255))
    screen.blit(text_surface, (rect_x+12, rect_y+6))

    text_surface = font_arial_16.render(f'Y_OFF: {json_asset_focus["y_offset"]}', False, (255, 255, 255))
    screen.blit(text_surface, (x, y+32))

    rect_w, rect_h = 32, 32
    rect_x = f.right['x'] + f.right['w'] - rect_w
    rect_y = y + 32
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(rect_x, rect_y, rect_w, rect_h), 1)
    text_surface = font_arial_16.render(f'+', False, (255, 255, 255))
    screen.blit(text_surface, (rect_x+12, rect_y+6))

    rect_w, rect_h = 32, 32
    rect_x = f.right['x'] + f.right['w'] - rect_w*2
    rect_y = y+32
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(rect_x, rect_y, rect_w, rect_h), 1)
    text_surface = font_arial_16.render(f'-', False, (255, 255, 255))
    screen.blit(text_surface, (rect_x+12, rect_y+6))

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
    
def draw_frame_center():
    draw_map_grid()
    draw_map_tiles()
    draw_tile_dragging()
    delete_tile_dragging()

def manage_draw():
    screen.fill('#101010')

    draw_frame_left()
    draw_frame_center()
    draw_frame_right()

    pygame.display.flip()

mouse = {
    'x': 0,
    'y': 0,
    'left_click_old': -1,
    'left_click_cur': 0,
    'right_click_old': -1,
    'right_click_cur': 0,
}

# ;jump
def click_asset_tab():
    global layer_cur
    global assets_packs
    global asset_pack_cur

    i = 0
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        pack_name = 'textures'
        found = False
        for asset_pack in assets_packs:
            if asset_pack['pack_name'] == pack_name:
                found = True
                break
        if not found:
            assets = load_asset_pack(pack_name)
            assets_packs.append({
                'pack_name': pack_name,
                'assets': assets,
            })
        else:
            assets = assets_packs[0]['assets']
        pannel_assets['assets'] = assets
        layer_cur = 0
        asset_pack_cur = 'textures'
    i += 1
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        pack_name = 'characters'
        found = False
        for asset_pack in assets_packs:
            if asset_pack['pack_name'] == pack_name:
                found = True
                break
        if not found:
            assets = load_asset_pack(pack_name)
            assets_packs.append({
                'pack_name': pack_name,
                'assets': assets,
            })
        else:
            assets = assets_packs[1]['assets']
        pannel_assets['assets'] = assets
        layer_cur = 1
        asset_pack_cur = 'characters'

def click_asset_icon():
    x1 = frame_pannel_assets['x']
    y1 = frame_pannel_assets['y']
    x2 = frame_pannel_assets['x'] + frame_pannel_assets['w']
    y2 = frame_pannel_assets['y'] + frame_pannel_assets['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        col_index = (mouse['x'] - frame_pannel_assets['x']) // pannel_assets['icon_size']
        pannel_assets['col_active'] = col_index
        row_index = (mouse['y'] - frame_pannel_assets['y']) // pannel_assets['icon_size']
        pannel_assets['row_active'] = row_index

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
        col_index = (mouse['x'] - frame_center['x']) // (tile_size*camera['zoom'])
        level_map['col_active'] = col_index

        row_index = (mouse['y'] - frame_center['y']) // (tile_size*camera['zoom'])
        level_map['row_active'] = row_index

        i = pannel_assets['row_active']
        j = pannel_assets['col_active']
        tile_filepath = pannel_assets['assets'][i][j]['image_filepath']

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
                    asset_row_cur = pannel_assets['row_active']
                    asset_col_cur = pannel_assets['col_active']
                    img_path = pannel_assets['assets'][asset_row_cur][asset_col_cur]['image_filepath']
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


def gen_asset(asset_pack_name):
    image = ai.gen_image(
        pannel_assets['row_active'], pannel_assets['col_active'], 
        assets_pack=asset_pack_cur,
        prompt=prompt['text']
    )
    image_index = pannel_assets['row_active']*5+pannel_assets['col_active']
    image_index = utils.format_id(image_index)
    image_filepath = f'assets/{asset_pack_cur}/images/{image_index}.png'
    image.save(image_filepath)
    data = {
        'image_filepath': image_filepath,
        'x_offset': 0,
        'y_offset': 0,
    }
    utils.json_write(f'assets/{asset_pack_cur}/jsons/{image_index}.json', data)
    load_asset_pack(f'{asset_pack_cur}')
        
def gen_asset_alpha(asset_pack_name):
    image = ai.gen_image(
        pannel_assets['row_active'], pannel_assets['col_active'], 
        assets_pack=asset_pack_cur,
        prompt=prompt['text']
    )
    image_index = pannel_assets['row_active']*5+pannel_assets['col_active']
    image_index = utils.format_id(image_index)
    image_filepath = f'assets/{asset_pack_cur}/images/{image_index}.png'
    image.save(image_filepath)
    data = {
        'image_filepath': image_filepath,
        'x_offset': 0,
        'y_offset': 0,
    }
    utils.json_write(f'assets/{asset_pack_cur}/jsons/{image_index}.json', data)

    image = ai.bg_remove(
        pannel_assets['row_active'], pannel_assets['col_active'], 
        assets_pack=f'{asset_pack_cur}',
    )
    image_index = pannel_assets['row_active']*5+pannel_assets['col_active']
    image_index = utils.format_id(image_index)
    image_filepath = f'assets/{asset_pack_cur}/images/{image_index}.png'
    image.save(image_filepath)
    data = {
        'image_filepath': image_filepath,
        'x_offset': 0,
        'y_offset': 0,
    }
    utils.json_write(f'assets/{asset_pack_cur}/jsons/{image_index}.json', data)

    load_asset_pack(f'{asset_pack_cur}')

def load_map():
    global level_map
    global pyimgs
    global assets_packs
    level_map = utils.json_read(f'maps/0000.json')
    # level map
    tiles = level_map['tiles']
    # pyimgs
    tiles = flatten_matrix(tiles)
    paths = flatten_matrix(tiles)
    for path in paths:
        if path != None:
            add_image_pygame(path)
    # assets
    packs_names = []
    for path in paths:
        if path != None:
            pack_name = path.split('/')[1]
            if pack_name not in packs_names:
                packs_names.append(pack_name)
    
    for i, pack_name in enumerate(packs_names):
        found = False
        for asset_pack in assets_packs:
            if asset_pack['pack_name'] == pack_name:
                found = True
                break
        if not found:
            assets = load_asset_pack(pack_name)
            assets_packs.append({
                'pack_name': pack_name,
                'assets': assets,
            })
        else:
            assets = assets_packs[i]['assets']
        pannel_assets['assets'] = assets
        layer_cur = i
    # ;jump
    # def add_image_pygame(path):
    print(packs_names)

def save_map():
    global level_map
    utils.json_write(f'maps/0000.json', level_map)

def save_assets():
    for asset_pack in assets_packs:
        pack_name = asset_pack['pack_name']
        assets = asset_pack['assets']
        assets = flatten_matrix(assets)
        for asset in assets:
            image_filepath = asset['image_filepath']
            if image_filepath != None:
                asset_filename = image_filepath.split('/')[-1].replace('.png', '.json')
                utils.json_write(f'assets/{pack_name}/jsons/{asset_filename}', asset)

def input_keyboard():
    global running
    global prompt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print('here')
                print(asset_pack_cur)
                if asset_pack_cur == 'textures':
                    gen_asset(asset_pack_name)
                elif asset_pack_cur == 'characters':
                    gen_asset_alpha(asset_pack_name)
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_BACKSPACE:
                prompt['text'] = prompt['text'][:-1]
            elif event.key == pygame.K_SPACE:
                prompt['text'] += ' '
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_map()
                save_assets()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                load_map()
            else:
                key_name = pygame.key.name(event.key)
                prompt['text'] += key_name

def click_asset_attr():
    i = pannel_assets['row_active']
    j = pannel_assets['col_active']
    json_asset_focus = pannel_assets['assets'][i][j]

    rect_w, rect_h = 32, 32
    rect_x1 = f.right['x'] + f.right['w'] - rect_w
    rect_y1 = f.right['y']
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h
    if mouse['x'] >= rect_x1 and mouse['y'] >= rect_y1 and mouse['x'] < rect_x2 and mouse['y'] < rect_y2:
        json_asset_focus['x_offset'] += 16

    rect_w, rect_h = 32, 32
    rect_x1 = f.right['x'] + f.right['w'] - rect_w*2
    rect_y1 = f.right['y']
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h
    if mouse['x'] >= rect_x1 and mouse['y'] >= rect_y1 and mouse['x'] < rect_x2 and mouse['y'] < rect_y2:
        json_asset_focus['x_offset'] -= 16

    rect_w, rect_h = 32, 32
    rect_x1 = f.right['x'] + f.right['w'] - rect_w
    rect_y1 = f.right['y'] + 32
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h
    if mouse['x'] >= rect_x1 and mouse['y'] >= rect_y1 and mouse['x'] < rect_x2 and mouse['y'] < rect_y2:
        json_asset_focus['y_offset'] += 16

    rect_w, rect_h = 32, 32
    rect_x1 = f.right['x'] + f.right['w'] - rect_w*2
    rect_y1 = f.right['y'] + 32
    rect_x2 = rect_x1 + rect_w
    rect_y2 = rect_y1 + rect_h
    if mouse['x'] >= rect_x1 and mouse['y'] >= rect_y1 and mouse['x'] < rect_x2 and mouse['y'] < rect_y2:
        json_asset_focus['y_offset'] -= 16

def input_mouse_left_click():
    global mouse
    global level_map
    global dragging
    global dragging_start_x
    global dragging_start_y
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]
    if mouse['left_click_cur'] == True:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            click_asset_tab()
            click_asset_icon()
            click_asset_attr()
            # click_map_tile()
            dragging = True
            dragging_start_x = mouse['x']
            dragging_start_y = mouse['y']
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            dragging = False
            for i in range(level_map_tmp['row_num']):
                for j in range(level_map_tmp['col_num']):
                    img_path = level_map_tmp['tiles'][i][j][layer_cur]
                    if img_path != None:
                        level_map['tiles'][i][j][layer_cur] = img_path

def input_mouse_right_click():
    global mouse
    global level_map
    global dragging_right
    global dragging_start_x
    global dragging_start_y
    mouse['right_click_cur'] = pygame.mouse.get_pressed()[2]
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

def input_mouse_pos():
    global mouse
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

def input_mouse():
    input_mouse_pos()
    input_mouse_left_click()
    input_mouse_right_click()

def manage_inputs():
    input_keyboard()
    input_mouse()

running = True
while running:
    manage_inputs()
    manage_draw()

pygame.quit()

