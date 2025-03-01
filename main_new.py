import os 

import copy
import pygame

import ai
import utils

window_w = 1920
window_h = 1080

tile_size = 32

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
    'h': window_h,
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
    'h': window_h,
}
frame_right['x'] = window_w - frame_right['w']

frame_center = {
    'x': frame_left['w'],
    'y': 0,
    'w': window_w - frame_left['w'] - frame_right['w'],
    'h': window_h,
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
images_pygame = []

def add_image_pygame(path):
    global images_pygame
    found = False
    for i, image_pygame in enumerate(images_pygame):
        if image_pygame['path'] == path:
            images_pygame[i] = {
                'path': path, 
                'img': pygame.image.load(path),
            }
            found = True
            break
    if not found:
        images_pygame.append({
            'path': path, 
            'img': pygame.image.load(path),
        })

for i in range(level_map['row_num']):
    row = []
    for j in range(level_map['col_num']):
        row.append(None)
    level_map['tiles'].append(row)
        
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

def load_asset_pack_textures_old():
    global assets_icons
    clear_asset_pack()
    assets_filepaths = [f'assets/textures/{filename}' for filename in os.listdir(f'assets/textures')]
    if assets_filepaths == []: return
    n_assets_to_load = len(assets_filepaths)
    k = 0
    all_assets_loaded = False
    for i in range(15):
        for j in range(5):
            assets_icons['icons'][i][j] = assets_filepaths[k]
            add_image_pygame(assets_filepaths[k])
            k += 1
            if k >= n_assets_to_load: all_assets_loaded = True
            if all_assets_loaded == True: break
        if all_assets_loaded == True: break

def load_asset_pack_textures():
    global assets_icons
    clear_asset_pack()
    assets_filepaths = [f'assets/textures/{filename}' for filename in os.listdir(f'assets/textures')]
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

def load_asset_pack_characters():
    global assets_icons
    clear_asset_pack()
    assets_icons['icons'][0][0] = 'assets/characters/succubus.png'
    assets_icons['icons'][0][1] = 'assets/characters/zombie.png'
    assets_icons['icons'][0][2] = 'assets/characters/hellhound.png'
    assets_icons['icons'][0][3] = 'assets/characters/pharoh.png'
    assets_icons['icons'][0][4] = 'assets/characters/harpy.png'
    assets_icons['icons'][1][0] = 'assets/characters/slime.png'
    add_image_pygame('assets/characters/succubus.png')
    add_image_pygame('assets/characters/zombie.png')
    add_image_pygame('assets/characters/hellhound.png')
    add_image_pygame('assets/characters/pharoh.png')
    add_image_pygame('assets/characters/harpy.png')
    add_image_pygame('assets/characters/slime.png')

clear_asset_pack()
# load_asset_pack_characters()
# load_asset_pack_textures()
print(assets_icons)

#######################################################
# ;pygame
#######################################################
pygame.init()

screen = pygame.display.set_mode([window_w, window_h])

# ;jump
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
                img = None
                for obj in images_pygame:
                    if obj['path'] == img_path:
                        img = obj['img']
                        break
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

def draw_map_grid():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera['zoom']
            h = tile_size*camera['zoom']
            x = frame_center['x'] + w*j + camera['x']
            y = frame_center['y'] + h*i + camera['y']
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)

    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            img_path = level_map['tiles'][i][j]
            if img_path != None:
                img = None
                for obj in images_pygame:
                    if obj['path'] == img_path:
                        img = obj['img']
                        break
                img = pygame.transform.scale(img, (w, h))
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = frame_center['x'] + w*j + camera['x']
                y = frame_center['y'] + h*i + camera['y']
                screen.blit(img, (x, y))

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
    # left frame
    draw_frame_right()
    # draw
    pygame.display.flip()

mouse = {
    'x': 0,
    'y': 0,
    'left_click_old': -1,
    'left_click_cur': 0,
}

def click_asset_tab():
    i = 0
    print('    frame assets tabs')
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('        frame assets tab {i}')
        load_asset_pack_textures()
    i += 1
    x1 = frame_assets_tabs['x'] + 80*i
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + 80*i + 80
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        print('        frame assets tab {i}')
        load_asset_pack_characters()

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
        level_map['tiles'][i][j] = tile_filepath

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ai.gen_image(
                    assets_icons['row_active'], assets_icons['col_active'], 
                    assets_pack='textures',
                    prompt='pixel art, grass tile texture',
                )
                load_asset_pack_textures()

    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]

    if mouse['left_click_cur'] == True: # left mouse button clicked
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            click_asset_tab()
            click_asset_icon()
            click_map_tile()
    else: # left mouse button released
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']

    draw_main()

pygame.quit()
