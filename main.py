import os

import pygame
import easygui

import g
import ai
import utils
import lib_assets

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

prompt = {}
prompt['text'] = 'pixel art, '

########################################################
# ;widgets
########################################################
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

frame_right = {
    'x': g.WINDOW_W - 320,
    'y': 0,
    'w': 320,
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

prompt_textarea = {
    'x': frame_left['x'],
    'y': pannel_assets['y'] + pannel_assets['h'],
    'w': frame_left['w'],
    'h': 30, 
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

## generate asset with ai
## save png - save json - reload jsons - add/update pyimg
def asset_gen(foldername):
    global assets_layers
    global asset_layer_cur
    # gen image
    image = ai.gen_image(prompt=prompt['text'])
    # save image
    asset_i = utils.assets_get_active_index(pannel_assets)
    asset_id = utils.format_id(asset_i)
    image.save(f'assets/{foldername}/images/{asset_id}.png')
    # save json
    asset_data = {
        'image_filepath': f'assets/{foldername}/images/{asset_id}.png',
        'x_offset': 0,
        'y_offset': 0,
        'size_mul': 1,
    }
    utils.json_write(f'assets/{foldername}/jsons/{asset_id}.json', asset_data)
    # load assets
    assets_layers[layer_cur] = lib_assets.assets_load(foldername)
    asset_layer_cur = assets_layers[layer_cur]
    # load pyimg
    pyimg_load(asset_data)

def asset_alpha_gen(foldername):
    global assets_layers
    # gen image
    image = ai.gen_image(prompt=prompt['text'])
    image = ai.bg_remove_new(image)
    # save image
    asset_i = utils.assets_get_active_index(pannel_assets)
    asset_id = utils.format_id(asset_i)
    image.save(f'assets/{foldername}/images/{asset_id}.png')
    # save json
    asset_data = {
        'image_filepath': f'assets/{foldername}/images/{asset_id}.png',
        'x_offset': 0,
        'y_offset': 0,
        'size_mul': 1,
    }
    utils.json_write(f'assets/{foldername}/jsons/{asset_id}.json', asset_data)
    # load assets
    assets_layers[layer_cur] = lib_assets.assets_load(foldername)
    asset_layer_cur = assets_layers[layer_cur]
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
    global assets_layers
    utils.json_write(f'maps/0000.json', tiles_list)
    utils.json_write(f'maps/0000-assets-layers.json', assets_layers)

def map_load():
    global tiles_list
    global assets_layers
    tiles_list = utils.json_read(f'maps/0000.json')
    assets_layers = utils.json_read(f'maps/0000-assets-layers.json')
    for asset_layer in assets_layers:
        for asset in asset_layer:
            pyimg_load(asset)

def map_new():
    pass
    '''
    filepath = easygui.fileopenbox()
    if not filepath: return
    filename = filepath.split('/')[-1].split('.')[0]
    global tiles_list
    global assets_layers
    utils.json_write(f'maps/{filename}.json', tiles_list)
    utils.json_write(f'maps/0000-assets-layers.json', assets_layers)
    '''

def map_open():
    filepath = easygui.fileopenbox()
    if not filepath: return
    filename = filepath.split('/')[-1].split('.')[0]
    global tiles_list
    global assets_layers
    tiles_list = utils.json_read(f'maps/{filename}.json')
    assets_layers = utils.json_read(f'maps/{filename}-assets-layers.json')
    for asset_layer in assets_layers:
        for asset in asset_layer:
            pyimg_load(asset)

#################################################################
# ;init
#################################################################
tiles_list = []
pyimgs = []
assets_jsons = []

assets_layers = [
    [],
    [],
    [],
    [],
    [],
]
assets_layers[0] = lib_assets.assets_load('textures')
assets_layers[1] = lib_assets.assets_load('characters')
'''
for layer in assets_layers:
    for item in layer:
        print(item)
quit()
'''

for asset_layer in assets_layers:
    for asset in asset_layer:
        pyimg_load(asset)

for pyimg in pyimgs:
    print(pyimg)
# quit()

layer_cur = 0
assets_layer_cur = assets_layers[layer_cur]


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
            elif event.key == pygame.K_UP:
                lib_assets.asset_offset_up(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_DOWN:
                lib_assets.asset_offset_down(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_LEFT:
                lib_assets.asset_offset_left(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_RIGHT:
                lib_assets.asset_offset_right(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_KP_PLUS:
                lib_assets.asset_increase_size(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_KP_MINUS:
                lib_assets.asset_decrease_size(pannel_assets, assets_layer_cur)
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_save()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_load()
            elif event.key == pygame.K_n and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_new()
            elif event.key == pygame.K_o and pygame.key.get_mods() & pygame.KMOD_CTRL:
                map_open()
            elif event.key == pygame.K_BACKSPACE:
                prompt['text'] = prompt['text'][:-1]
            elif event.key == pygame.K_SPACE:
                prompt['text'] += ' '
            elif event.key == pygame.K_LCTRL:
                pass
            else:
                key_name = pygame.key.name(event.key)
                prompt['text'] += key_name

def mouse_click_asset_tab():
    global layer_cur
    global assets_jsons
    global pannel_assets
    global assets_layer_cur
    x1 = frame_assets_tabs['x']
    y1 = frame_assets_tabs['y']
    x2 = frame_assets_tabs['x'] + frame_assets_tabs['w']
    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tab_index = (mouse['x'] - x1) // 64
        assets_layer_cur = assets_layers[tab_index]
        layer_cur = tab_index

def asset_set_active():
    mouse_rel_x = mouse['x'] - pannel_assets['x']
    mouse_rel_y = mouse['y'] - pannel_assets['y']
    row_i = mouse_rel_y // pannel_assets['icon_size']
    col_i = mouse_rel_x // pannel_assets['icon_size']
    pannel_assets['col_cur'] = col_i
    pannel_assets['row_cur'] = row_i

def mouse_click_asset():
    x1 = pannel_assets['x']
    y1 = pannel_assets['y']
    x2 = pannel_assets['x'] + pannel_assets['icon_size']*pannel_assets['col_n']
    y2 = pannel_assets['y'] + pannel_assets['icon_size']*pannel_assets['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        asset_set_active()

def mouse_click_tile():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tile_index = tile_index_by_mouse_pos()
        asset_i = pannel_assets['row_cur']*pannel_assets['col_n']+pannel_assets['col_cur']
        asset_id = utils.format_id(asset_i)
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
    draw_prompt_textarea()

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
            index = lib_assets.asset_get_index(row_i, col_i, pannel_assets['col_n'])
            _id = utils.format_id(index)
            asset = lib_assets.asset_get_by_id(assets_layer_cur, _id)
            if asset != {}:
                image_filepath = asset['image_filepath']
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

def draw_prompt_textarea():
    x = prompt_textarea['x']
    y = prompt_textarea['y']
    w = prompt_textarea['w']
    h = prompt_textarea['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    text_surface = font_arial_16.render(f'{prompt["text"]}', False, (255, 255, 255))
    screen.blit(text_surface, (x+6, y+6))
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

# ;jump
def draw_tiles_images():
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            index = tile_index(row_i, col_i)
            tile = tiles_list[index]
            for i in range(len(assets_layers)): # draw all layers
                image_filepath = tile[i]
                if image_filepath != None:
                    asset = lib_assets.asset_get_by_filepath(assets_layers, image_filepath)
                    pyimg = pyimg_by_filepath(image_filepath)
                    img = pygame.transform.scale(
                        pyimg['image'], 
                        (pannel_tiles['tile_size']*asset['size_mul'], pannel_tiles['tile_size']*asset['size_mul'])
                    )
                    x = pannel_tiles['x'] + pannel_tiles['tile_size']*col_i + asset['x_offset']
                    y = pannel_tiles['y'] + pannel_tiles['tile_size']*row_i + asset['y_offset']
                    screen.blit(img, (x, y))

# ;jump
def draw_asset_attr():
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = lib_assets.asset_get_active(assets_jsons, row_i, col_i, col_n)
    if asset != {}:
        x = frame_right['x']
        y = frame_right['y']
        p = 16
        text_surface = font_arial_16.render(f'IMG_PATH: {asset["image_filepath"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x+p, y+p))
        y += 24
        text_surface = font_arial_16.render(f'X OFF : {asset["x_offset"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x+p, y+p))
        y += 24
        text_surface = font_arial_16.render(f'Y OFF : {asset["y_offset"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x+p, y+p))
        y += 24
        text_surface = font_arial_16.render(f'SIZE MUL : {asset["size_mul"]}', False, (255, 255, 255))
        screen.blit(text_surface, (x+p, y+p))
        y += 24

def draw_frame_right():
    x = frame_right['x']
    y = frame_right['y']
    w = frame_right['w']
    h = frame_right['h']
    pygame.draw.rect(screen, '#202020', (x, y, w, h))
    draw_asset_attr()

def draw_manager():
    screen.fill('#101010')
    draw_frame_center()
    draw_frame_left()
    draw_frame_right()
    pygame.display.flip()

running = True
while running:
    inputs_manager()
    update_manager()
    draw_manager()

pygame.quit()

