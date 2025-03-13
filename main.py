import os

import pygame

import g
import ai
import utils

pygame.init()

screen = pygame.display.set_mode([g.WINDOW_W, g.WINDOW_H])
font_arial_16 = pygame.font.SysFont('Arial', 16)

mouse = {
    'x': 0,
    'y': 0,
    'left_click_cur': 0,
    'left_click_old': 0,
    'right_click_cur': 0,
    'right_click_old': 0,
}

frame_left = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': g.WINDOW_H,
}

frame_center = {
    'x': 320,
    'y': 0,
    'w': g.WINDOW_W - 320,
    'h': g.WINDOW_H,
}

frame_assets_tabs = {
    'x': frame_left['x'],
    'y': frame_left['y'],
    'w': frame_left['w'],
    'h': 30, 
}

pannel_assets = {
    'x': frame_assets_tabs['x'],
    'y': frame_assets_tabs['y'] + frame_assets_tabs['h'],
    'w': 64*5,
    'h': 64*15,
    'col_n': 5,
    'row_n': 15,
    'icon_size': 64,
    'col_cur': 0,
    'row_cur': 0,
}

pannel_tiles = {
    'x': frame_center['x'],
    'y': frame_center['y'],
    'w': frame_center['w'],
    'h': frame_center['h'],
    'col_n': 7,
    'row_n': 7,
    'tile_size': 128,
    'col_cur': 0,
    'row_cur': 0,
}

#################################################################
# ;assets
#################################################################
def assets_jsons_load(foldername):
    filepaths = [f'assets/{foldername}/jsons/{filename}' for filename in os.listdir(f'assets/{foldername}/jsons')]
    assets_jsons = []
    for filepath in filepaths:
        asset_json = asset_json_load(filepath)
        assets_jsons.append(asset_json)
    return assets_jsons

def asset_json_load(filepath):
    asset_json = utils.json_read(filepath)
    return asset_json

def asset_json_by_id(_id):
    asset_json_searched = {}
    for asset_json in assets_jsons:
        asset_json_id = asset_json['image_filepath'].split('/')[-1].split('.')[0]
        if asset_json_id == _id:
            asset_json_searched = asset_json
            break
    return asset_json_searched

def asset_index(row_i, col_i):
    global pannel_assets
    index = row_i*pannel_assets['col_n'] + col_i
    return index

def asset_index_by_mouse_pos():
    global mouse
    mouse_rel_x = mouse['x'] - pannel_assets['x']
    mouse_rel_y = mouse['y'] - pannel_assets['y']
    row_i = mouse_rel_y // pannel_assets['icon_size']
    col_i = mouse_rel_x // pannel_assets['icon_size']
    index = asset_index(row_i, col_i)
    return index

def asset_gen(foldername):
    global assets_jsons
    prompt = {}
    prompt['text'] = 'pixel art, rock texture'

    # gen image
    image = ai.gen_image(prompt=prompt['text'])

    # save image
    asset_index = utils.assets_get_active_index(pannel_assets)
    asset_id = utils.format_id(asset_index)
    image.save(f'assets/{foldername}/images/{asset_id}.png')

    # save json
    asset_data = {
        'image_filepath': f'assets/{foldername}/images/{asset_id}.png',
        'x_offset': 0,
        'y_offset': 0,
    }
    utils.json_write(f'assets/{foldername}/jsons/{asset_id}.json', asset_data)

    # load assets
    assets_jsons = assets_jsons_load(foldername)

    # load pyimg
    pyimg_load(asset_data)

#################################################################
# ;pyimg
#################################################################
def pyimg_load(asset_json):
    global pyimgs
    filepath = asset_json['image_filepath']
    found = False
    for i, pyimg in enumerate(pyimgs):
        if pyimg['image_filepath'] == filepath:
            pyimgs[i] = {
                'image_filepath': filepath, 
                'image': pygame.image.load(filepath),
            }
            found = True
            break
    if not found:
        pyimgs.append({
            'image_filepath': filepath, 
            'image': pygame.image.load(filepath),
        })

def pyimg_by_filepath(image_filepath):
    global pyimgs
    pyimg = {} 
    for pyimg_cur in pyimgs:
        if pyimg_cur['image_filepath'] == image_filepath:
            pyimg = pyimg_cur
            break
    return pyimg

#################################################################
# ;tiles
#################################################################
def tiles_init():
    global tiles_list
    tiles_list = []
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            tiles_list.append([None, None, None, None, None])

def tile_index(row_i, col_i):
    global pannel_tiles
    index = row_i*pannel_tiles['col_n'] + col_i
    return index

def tile_index_by_mouse_pos():
    global mouse
    mouse_rel_x = mouse['x'] - pannel_tiles['x']
    mouse_rel_y = mouse['y'] - pannel_tiles['y']
    row_i = mouse_rel_y // pannel_tiles['tile_size']
    col_i = mouse_rel_x // pannel_tiles['tile_size']
    index = tile_index(row_i, col_i)
    return index

def map_save():
    global tiles_list
    global assets_l0_jsons
    global assets_l1_jsons
    utils.json_write(f'maps/0000.json', tiles_list)
    utils.json_write(f'maps/0000-assets-l0.json', assets_l0_jsons)
    utils.json_write(f'maps/0000-assets-l1.json', assets_l1_jsons)

def map_load():
    global tiles_list
    global assets_l0_jsons
    global assets_l1_jsons
    tiles_list = utils.json_read(f'maps/0000.json')
    assets_l0_jsons = utils.json_read(f'maps/0000-assets-l0.json')
    assets_l1_jsons = utils.json_read(f'maps/0000-assets-l1.json')

    for asset in assets_l0_jsons:
        pyimg_load(asset)
    for asset in assets_l1_jsons:
        pyimg_load(asset)

#################################################################
# ;init
#################################################################
tiles_list = []
pyimgs = []
assets_jsons = []

assets_l0_jsons = []
assets_l1_jsons = []
assets_l0_jsons = assets_jsons_load('textures')
assets_l1_jsons = assets_jsons_load('characters')

for asset_json in assets_l0_jsons:
    pyimg_load(asset_json)
for asset_json in assets_l1_jsons:
    pyimg_load(asset_json)

assets_jsons = assets_l0_jsons
layer_cur = 0

tiles_init()
## test code
'''
tiles_list[0][0] = f'assets/textures/images/0000.png'
tiles_list[1][0] = f'assets/textures/images/0001.png'
tiles_list[9][0] = f'assets/textures/images/0008.png'
'''

###############################################################
# ;inputs
###############################################################
def inputs_keyboard():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if layer_cur == 0:
                    asset_gen('textures')
                elif layer_cur == 1:
                    asset_alpha_gen('characters')
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_save()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_load()

def mouse_click_asset_tab():
    global layer_cur
    global assets_jsons
    global pannel_assets
    x1 = frame_assets_tabs['x']
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + frame_assets_tabs['w']
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tab_index = (mouse['x'] - x1) // 64
        if tab_index == 0:
            assets_jsons = assets_l0_jsons
            layer_cur = 0
        elif tab_index == 1:
            assets_jsons = assets_l1_jsons
            layer_cur = 1

def mouse_click_asset():
    x1 = pannel_assets['x']
    y1 = pannel_assets['y']
    x2 = pannel_assets['x'] + pannel_assets['icon_size']*pannel_assets['col_n']
    y2 = pannel_assets['y'] + pannel_assets['icon_size']*pannel_assets['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        mouse_rel_x = mouse['x'] - pannel_assets['x']
        mouse_rel_y = mouse['y'] - pannel_assets['y']
        row_i = mouse_rel_y // pannel_assets['icon_size']
        col_i = mouse_rel_x // pannel_assets['icon_size']
        pannel_assets['col_cur'] = col_i
        pannel_assets['row_cur'] = row_i

def mouse_click_tile():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tile_index = tile_index_by_mouse_pos()
        asset_index = pannel_assets['row_cur']*pannel_assets['col_n']+pannel_assets['col_cur']
        asset_id = utils.format_id(asset_index)
        if layer_cur == 0:
            tiles_list[tile_index][0] = f'assets/textures/images/{asset_id}.png'
        elif layer_cur == 1:
            tiles_list[tile_index][1] = f'assets/characters/images/{asset_id}.png'

def mouse_clear_tile():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tile_index = tile_index_by_mouse_pos()
        if layer_cur == 0:
            tiles_list[tile_index][0] = None
        elif layer_cur == 1:
            tiles_list[tile_index][1] = None

def mouse_pos():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

def mouse_left():
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]
    if mouse['left_click_cur'] == 1:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            mouse_click_asset_tab()
            mouse_click_asset()
            mouse_click_tile()
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']

def mouse_right():
    mouse['right_click_cur'] = pygame.mouse.get_pressed()[2]
    if mouse['right_click_cur'] == 1:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            mouse_clear_tile()
    else:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']

def inputs_mouse():
    mouse_pos()
    mouse_left()
    mouse_right()

def inputs_manager():
    inputs_keyboard()
    inputs_mouse()

##########################################################################
# ;update
##########################################################################
def update_manager():
    pass

##########################################################################
# ;draw
##########################################################################
def draw_frame_left():
    x = frame_left['x']
    y = frame_left['y']
    w = frame_left['w']
    h = frame_left['h']
    pygame.draw.rect(screen, '#202020', (x, y, w, h))
    draw_frame_assets_tabs()
    draw_frame_assets()

def draw_frame_assets_tabs():
    x = frame_assets_tabs['x']
    y = frame_assets_tabs['y']
    w = frame_assets_tabs['w']
    h = frame_assets_tabs['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    for i in range(5):
        text_surface = font_arial_16.render(f'L{i}', False, (255, 255, 255))
        screen.blit(text_surface, (x+(64*i)+6, y+6))
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, 64, h), 1)

def draw_frame_assets():
    draw_frame_assets_grid()
    draw_frame_assets_icons()
    draw_frame_assets_active()

def draw_frame_assets_grid():
    for row_i in range(pannel_assets['row_n']):
        for col_i in range(pannel_assets['col_n']):
            x = pannel_assets['x'] + (pannel_assets['icon_size']*col_i) + 1
            y = pannel_assets['y'] + (pannel_assets['icon_size']*row_i) + 1
            w = pannel_assets['icon_size'] - 1
            h = pannel_assets['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))

def draw_frame_assets_icons():
    for row_i in range(pannel_assets['row_n']):
        for col_i in range(pannel_assets['col_n']):
            index = asset_index(row_i, col_i)
            _id = utils.format_id(index)
            asset_json = asset_json_by_id(_id)
            if asset_json != {}:
                image_filepath = asset_json['image_filepath']
                pyimg = pyimg_by_filepath(image_filepath)
                img = pygame.transform.scale(pyimg['image'], (pannel_assets['icon_size'], pannel_assets['icon_size']))
                x = pannel_assets['x'] + pannel_assets['icon_size']*col_i
                y = pannel_assets['y'] + pannel_assets['icon_size']*row_i
                screen.blit(img, (x, y))

def draw_frame_assets_active():
    x = pannel_assets['x'] + (pannel_assets['icon_size']*pannel_assets['col_cur'])
    y = pannel_assets['y'] + (pannel_assets['icon_size']*pannel_assets['row_cur'])
    w = pannel_assets['icon_size']
    h = pannel_assets['icon_size']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_frame_center():
    x = frame_center['x']
    y = frame_center['y']
    w = frame_center['w']
    h = frame_center['h']
    pygame.draw.rect(screen, '#101010', (x, y, w, h))
    draw_tiles_grid()
    draw_tiles_images()

def draw_tiles_grid():
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            x = pannel_tiles['x'] + (pannel_tiles['tile_size']*col_i) 
            y = pannel_tiles['y'] + (pannel_tiles['tile_size']*row_i)
            w = pannel_tiles['tile_size']
            h = pannel_tiles['tile_size']
            pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_tiles_images():
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            index = tile_index(row_i, col_i)
            tile = tiles_list[index]
            for i in range(5): # draw all layers
                image_filepath = tile[i]
                if image_filepath != None:
                    pyimg = pyimg_by_filepath(image_filepath)
                    img = pygame.transform.scale(pyimg['image'], (pannel_tiles['tile_size'], pannel_tiles['tile_size']))
                    x = pannel_tiles['x'] + pannel_tiles['tile_size']*col_i
                    y = pannel_tiles['y'] + pannel_tiles['tile_size']*row_i
                    screen.blit(img, (x, y))

def draw_manager():
    screen.fill('#101010')
    draw_frame_left()
    draw_frame_center()
    pygame.display.flip()

running = True
while running:
    inputs_manager()
    update_manager()
    draw_manager()

pygame.quit()

