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

print(asset_pack_images_filepaths)
print(asset_pack_jsons_filepaths)

pannel_assets_clean = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'icons': [],
}

# pannel_assets = copy.deepcopy(pannel_assets_clean)

pannel_assets = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'icons': [],
}


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
        pannel_assets['icons'].append(row)

def load_asset_pack(foldername):
    global pannel_assets
    global asset_pack_cur
    asset_pack_cur = foldername

    pannel_assets['icons'] = []
    for i in range(pannel_assets['row_num']):
        row = []
        for j in range(pannel_assets['col_num']):
            row.append({'image_filepath': None, 'x_offset': 0, 'y_offset': 0})
        pannel_assets['icons'].append(row)

    assets_filepaths = [f'assets/{foldername}/jsons/{filename}' for filename in os.listdir(f'assets/{foldername}/jsons')]
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            asset_index_cur = i*pannel_assets['col_num']+j
            asset_id = utils.format_id(asset_index_cur)
            for asset_filepath in assets_filepaths:
                asset_filepath_id = asset_filepath.split('/')[-1].split('.')[0]
                if asset_id in asset_filepath_id:
                    with open(asset_filepath) as f: 
                        json_asset = json.load(f)
                    image_filepath = json_asset['image_filepath']
                    x_offset = json_asset['x_offset']
                    y_offset = json_asset['y_offset']
                    if foldername == 'characters':
                        pannel_assets['icons'][i][j] = {'image_filepath': image_filepath, 'x_offset': x_offset, 'y_offset': y_offset}
                    else:
                        pannel_assets['icons'][i][j] = {'image_filepath': image_filepath, 'x_offset': 0, 'y_offset': 0}
                    add_image_pygame(image_filepath)
                    break

def load_asset_pack_old(foldername):
    global pannel_assets
    global asset_pack_cur
    asset_pack_cur = foldername
    row_active = pannel_assets['row_active']
    col_active = pannel_assets['col_active']
    clear_asset_pack()
    assets_filepaths = [f'assets/{foldername}/images/{filename}' for filename in os.listdir(f'assets/{foldername}/images')]
    for i in range(15):
        for j in range(5):
            asset_index_cur = i*5+j
            asset_id = utils.format_id(asset_index_cur)
            for asset_filepath in assets_filepaths:
                asset_filepath_id = asset_filepath.split('/')[-1].split('.')[0]
                if asset_id in asset_filepath_id:
                    if foldername == 'characters':
                        y_offset = (-tile_size*camera['zoom'])//4
                        pannel_assets['icons'][i][j] = {'image_filepath': asset_filepath, 'x_offset': 0, 'y_offset': y_offset}
                    else:
                        pannel_assets['icons'][i][j] = {'image_filepath': asset_filepath, 'x_offset': 0, 'y_offset': 0}
                    add_image_pygame(asset_filepath)
                    break
    pannel_assets['row_active'] = row_active
    pannel_assets['col_active'] = col_active

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
    for row_num in range(pannel_assets['row_num']):
        for col_num in range(pannel_assets['col_num']):
            # background
            x = frame_pannel_assets['x'] + pannel_assets['icon_size']*col_num + 1
            y = frame_pannel_assets['y'] + pannel_assets['icon_size']*row_num + 1
            w = pannel_assets['icon_size'] - 1
            h = pannel_assets['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    # draw icons images
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            img_path = pannel_assets['icons'][i][j]['image_filepath']
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

def get_icon_by_filepath(filepath):
    icon = None
    for i in range(pannel_assets['row_num']):
        for j in range(pannel_assets['col_num']):
            asset_icon = pannel_assets['icons'][i][j]
            if filepath == asset_icon['image_filepath']:
                icon = asset_icon
                break
    return icon

def draw_map_tiles():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            # textures
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
            img_path = level_map['tiles'][i][j][1]
            if img_path != None:
                icon = get_icon_by_filepath(img_path)
                y_offset = icon['y_offset']
                img = get_pyimg_by_path(img_path)
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = frame_center['x'] + w*j + camera['x']
                y = frame_center['y'] + h*i + camera['y'] + y_offset
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
    x = f.right['x']
    y = f.right['y']
    w = f.right['w']
    h = f.right['h']
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
        print('frame center')

        col_index = (mouse['x'] - frame_center['x']) // (tile_size*camera['zoom'])
        print(col_index)
        level_map['col_active'] = col_index

        row_index = (mouse['y'] - frame_center['y']) // (tile_size*camera['zoom'])
        print(row_index)
        level_map['row_active'] = row_index

        i = pannel_assets['row_active']
        j = pannel_assets['col_active']
        tile_filepath = pannel_assets['icons'][i][j]['image_filepath']

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
                    img_path = pannel_assets['icons'][asset_row_cur][asset_col_cur]['image_filepath']
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
                print('generating img...')
                if asset_pack_cur == 'characters':
                    image = ai.gen_image(
                        pannel_assets['row_active'], pannel_assets['col_active'], 
                        assets_pack='characters',
                        prompt='pixel art, 1girl, chibi, succubus',
                    )
                    image_index = pannel_assets['row_active']*5+pannel_assets['col_active']
                    image_index = utils.format_id(image_index)
                    image_filepath = f'assets/characters/images/{image_index}.png'
                    image.save(image_filepath)
                    data = {
                        'image_filepath': image_filepath,
                        'x_offset': 0,
                        'y_offset': 0,
                    }
                    utils.json_write(f'assets/characters/jsons/{image_index}.json', data)
                    '''
                    ai.bg_remove(
                        pannel_assets['row_active'], pannel_assets['col_active'], 
                        assets_pack='characters',
                    )
                    '''
                    load_asset_pack('characters')
                    
                elif asset_pack_cur == 'textures':
                    ai.gen_image(
                        pannel_assets['row_active'], pannel_assets['col_active'], 
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
