import os

import pygame

import g
import utils

pygame.init()

screen = pygame.display.set_mode([g.WINDOW_W, g.WINDOW_H])
font_arial_16 = pygame.font.SysFont('Arial', 16)

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

pannel_assets = {
    'x': 0,
    'y': 0,
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
def tiles_init_old():
    global tiles_list
    tiles_list = []
    for row_i in range(pannel_tiles['row_n']):
        row_cur = []
        for col_i in range(pannel_tiles['col_n']):
            row_cur.append([None, None, None, None, None])
        tiles_list.append(row_cur)

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

#################################################################
# ;init
#################################################################
tiles_list = []
pyimgs = []
assets_jsons = []

assets_jsons = assets_jsons_load('textures')
for asset_json in assets_jsons:
    pyimg_load(asset_json)
    print(asset_json)
print(pyimgs)
tiles_init()
## test code
tiles_list[0][0] = f'assets/textures/images/0000.png'
tiles_list[1][0] = f'assets/textures/images/0001.png'
tiles_list[9][0] = f'assets/textures/images/0008.png'
print(tiles_list)

def inputs_keyboard():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

def inputs_manager():
    inputs_keyboard()

def update_manager():
    pass

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

def draw_frame_assets():
    draw_frame_assets_grid()
    draw_frame_assets_icons()

def draw_frame_left():
    x = frame_left['x']
    y = frame_left['y']
    w = frame_left['w']
    h = frame_left['h']
    pygame.draw.rect(screen, '#202020', (x, y, w, h))
    draw_frame_assets()

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
            # pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
            pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_tiles_images():
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            index = tile_index(row_i, col_i)
            tile = tiles_list[index]
            ## layer 0
            image_filepath = tile[0]
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

