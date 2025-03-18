import os

import pygame
import easygui

import g
import ai
import utils
import lib_assets
import lib_pyimgs
import lib_tiles

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

pannel_tiles_dragging = {
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
# ;init
#################################################################
tiles_list = []
tiles_dragging_list = []
pyimgs = []
assets_jsons = []

assets_layers = [
    [],
    [],
    [],
    [],
    [],
]

assets_packs_foldernames = [
    'forest-grounds',
    'forest-objects',
    'forest-objects',
    'forest-objects',
    'characters',
]

assets_layers[0] = lib_assets.assets_load(assets_packs_foldernames[0])
assets_layers[1] = lib_assets.assets_load(assets_packs_foldernames[1])
assets_layers[2] = lib_assets.assets_load(assets_packs_foldernames[2])
assets_layers[3] = lib_assets.assets_load(assets_packs_foldernames[3])
assets_layers[4] = lib_assets.assets_load(assets_packs_foldernames[4])

for asset_layer in assets_layers:
    for asset in asset_layer:
        lib_pyimgs.pyimg_load(pygame, pyimgs, asset)

layer_cur = 0
assets_layer_cur = assets_layers[layer_cur]
tiles_list = lib_tiles.tiles_init(pannel_tiles)
tiles_dragging_list = lib_tiles.tiles_init(pannel_tiles_dragging)

###############################################################
# ;inputs
###############################################################
def inputs_keyboard():
    global tiles_list
    global assets_layers
    global asset_layer_cur
    global pyimgs
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_RETURN:
                if layer_cur == 0:
                    assets_layers, asset_layer_cur, pyimgs = lib_assets.asset_gen(assets_packs_foldernames[0], prompt, pannel_assets, pygame, assets_layers, layer_cur, pyimgs)
                else: 
                    assets_layers, asset_layer_cur, pyimgs = lib_assets.asset_gen_alpha(assets_packs_foldernames[layer_cur], prompt, pannel_assets, pygame, assets_layers, layer_cur, pyimgs)
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
                lib_tiles.map_save(tiles_list, assets_layers)
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                tiles_list, assets_layers, pyimgs = lib_tiles.map_load(pygame)
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

# ;jump
def mouse_click_tile():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tile_index = lib_tiles.tile_get_index_by_mouse_pos(pannel_tiles, mouse)
        asset_i = pannel_assets['row_cur']*pannel_assets['col_n']+pannel_assets['col_cur']
        asset_id = utils.format_id(asset_i)
        tiles_list[tile_index][layer_cur] = f'assets/{assets_packs_foldernames[layer_cur]}/images/{asset_id}.png'

drag = {
    'dragging': False,
    'dragging_start_x': 0,
    'dragging_start_y': 0,
}

def mouse_click_tile_drag():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        drag['dragging'] = True
        drag['dragging_start_x'] = mouse['x']
        drag['dragging_start_y'] = mouse['y']

def mouse_click_tile_drag_release():
    drag['dragging'] = False

def mouse_clear_tile():
    x1 = pannel_tiles['x']
    y1 = pannel_tiles['y']
    x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
    y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
        tile_index = lib_tiles.tile_get_index_by_mouse_pos(pannel_tiles, mouse)
        tiles_list[tile_index][layer_cur] = None

def mouse_pos():
    mouse['x'], mouse['y'] = pygame.mouse.get_pos()

def mouse_left():
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]
    if mouse['left_click_cur'] == 1:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            mouse_click_asset_tab()
            mouse_click_asset()
            # mouse_click_tile()
            mouse_click_tile_drag()
    else:
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            mouse_click_tile_drag_release()

def mouse_right():
    mouse['right_click_cur'] = pygame.mouse.get_pressed()[2]
    if mouse['right_click_cur'] == 1:
        if mouse['right_click_old'] != mouse['right_click_cur']:
            mouse['right_click_old'] = mouse['right_click_cur']
            mouse_clear_tile()
            print('right click')
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
                pyimg = lib_pyimgs.pyimg_by_filepath(pyimgs, image_filepath)
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

def draw_tiles_box_images():
    for row_i in range(pannel_tiles_dragging['row_n']):
        for col_i in range(pannel_tiles_dragging['col_n']):
            index = lib_tiles.tile_get_index(pannel_tiles_dragging, row_i, col_i)
            tile = tiles_dragging_list[index]
            for i in range(len(assets_layers)): # draw all layers
                image_filepath = tile[i]
                if image_filepath != None:
                    asset = lib_assets.asset_get_by_filepath(assets_layers, image_filepath)
                    pyimg = lib_pyimgs.pyimg_by_filepath(pyimgs, image_filepath)
                    img = pygame.transform.scale(
                        pyimg['image'], 
                        (pannel_tiles_dragging['tile_size']*asset['size_mul'], pannel_tiles_dragging['tile_size']*asset['size_mul'])
                    )
                    x = pannel_tiles_dragging['x'] + pannel_tiles_dragging['tile_size']*col_i + asset['x_offset']
                    y = pannel_tiles_dragging['y'] + pannel_tiles_dragging['tile_size']*row_i + asset['y_offset']
                    screen.blit(img, (x, y))


# ;jump
def draw_tiles_drag():
    global tiles_dragging_list
    if drag['dragging'] == True:
        x1 = pannel_tiles['x']
        y1 = pannel_tiles['y']
        x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
        y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
        if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
            x = drag['dragging_start_x']
            y = drag['dragging_start_y']
            w = mouse['x'] - drag['dragging_start_x']
            h = mouse['y'] - drag['dragging_start_y']
            pygame.draw.rect(screen, '#202020', pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

            tile_start_index = lib_tiles.tile_get_index_by_mouse_xy(pannel_tiles, x, y)
            tile_end_index = lib_tiles.tile_get_index_by_mouse_pos(pannel_tiles, mouse)

            tiles_dragging_list = lib_tiles.tiles_init(pannel_tiles)
            # print(tile_start_index, tile_end_index)
            '''
            x1 = pannel_tiles['x']
            y1 = pannel_tiles['y']
            x2 = pannel_tiles['x'] + pannel_tiles['tile_size']*pannel_tiles['col_n']
            y2 = pannel_tiles['y'] + pannel_tiles['tile_size']*pannel_tiles['row_n']
            if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                tile_index = lib_tiles.tile_get_index_by_mouse_pos(pannel_tiles, mouse)
                asset_i = pannel_assets['row_cur']*pannel_assets['col_n']+pannel_assets['col_cur']
                asset_id = utils.format_id(asset_i)
                tiles_list[tile_index][layer_cur] = f'assets/{assets_packs_foldernames[layer_cur]}/images/{asset_id}.png'
            '''

            asset_row_cur = pannel_assets['row_cur']
            asset_col_cur = pannel_assets['col_cur']
            for i in range(pannel_tiles_dragging['row_n']):
                for j in range(pannel_tiles_dragging['col_n']):
                    tile_index = i*pannel_tiles_dragging['col_n']+j
                    if tile_index >= tile_start_index and tile_index <= tile_end_index:
                        asset_i = pannel_assets['row_cur']*pannel_assets['col_n']+pannel_assets['col_cur']
                        asset_id = utils.format_id(asset_i)
                        tiles_dragging_list[tile_index][layer_cur] = f'assets/{assets_packs_foldernames[layer_cur]}/images/{asset_id}.png'
                        print(tiles_dragging_list)
                    '''
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
                    '''

            draw_tiles_box_images()

def draw_frame_center():
    x = frame_center['x']
    y = frame_center['y']
    w = frame_center['w']
    h = frame_center['h']
    pygame.draw.rect(screen, '#101010', (x, y, w, h))
    draw_tiles_grid()
    draw_tiles_images()
    draw_tiles_drag()

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
            index = lib_tiles.tile_get_index(pannel_tiles, row_i, col_i)
            tile = tiles_list[index]
            for i in range(len(assets_layers)): # draw all layers
                image_filepath = tile[i]
                if image_filepath != None:
                    asset = lib_assets.asset_get_by_filepath(assets_layers, image_filepath)
                    pyimg = lib_pyimgs.pyimg_by_filepath(pyimgs, image_filepath)
                    img = pygame.transform.scale(
                        pyimg['image'], 
                        (pannel_tiles['tile_size']*asset['size_mul'], pannel_tiles['tile_size']*asset['size_mul'])
                    )
                    x = pannel_tiles['x'] + pannel_tiles['tile_size']*col_i + asset['x_offset']
                    y = pannel_tiles['y'] + pannel_tiles['tile_size']*row_i + asset['y_offset']
                    screen.blit(img, (x, y))

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

