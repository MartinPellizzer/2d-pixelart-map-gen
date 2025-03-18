import utils

import lib_pyimgs

def tiles_init(pannel_tiles):
    tiles_list = []
    for row_i in range(pannel_tiles['row_n']):
        for col_i in range(pannel_tiles['col_n']):
            tiles_list.append([None, None, None, None, None])
    return tiles_list

def tile_get_index(pannel_tiles, row_i, col_i):
    index = row_i*pannel_tiles['col_n'] + col_i
    return index

def tile_get_rc_by_mouse_pos(pannel_tiles, mouse):
    mouse_rel_x = mouse['x'] - pannel_tiles['x']
    mouse_rel_y = mouse['y'] - pannel_tiles['y']
    row_i = mouse_rel_y // pannel_tiles['tile_size']
    col_i = mouse_rel_x // pannel_tiles['tile_size']
    return row_i, col_i

def tile_get_index_by_mouse_pos(pannel_tiles, mouse):
    mouse_rel_x = mouse['x'] - pannel_tiles['x']
    mouse_rel_y = mouse['y'] - pannel_tiles['y']
    row_i = mouse_rel_y // pannel_tiles['tile_size']
    col_i = mouse_rel_x // pannel_tiles['tile_size']
    index = tile_get_index(pannel_tiles, row_i, col_i)
    return index

def tile_get_rc_by_xy(pannel_tiles, x, y):
    x = x - pannel_tiles['x']
    y = y - pannel_tiles['y']
    row_i = y // pannel_tiles['tile_size']
    col_i = x // pannel_tiles['tile_size']
    return row_i, col_i

def tile_get_index_by_mouse_xy(pannel_tiles, x, y):
    x = x - pannel_tiles['x']
    y = y - pannel_tiles['y']
    row_i = y // pannel_tiles['tile_size']
    col_i = x // pannel_tiles['tile_size']
    index = tile_get_index(pannel_tiles, row_i, col_i)
    return index

def tile_get_index_by_mouse_xy(pannel_tiles, x, y):
    x = x - pannel_tiles['x']
    y = y - pannel_tiles['y']
    row_i = y // pannel_tiles['tile_size']
    col_i = x // pannel_tiles['tile_size']
    index = tile_get_index(pannel_tiles, row_i, col_i)
    return index

def map_save(tiles_list, assets_layers):
    utils.json_write(f'maps/0000.json', tiles_list)
    utils.json_write(f'maps/0000-assets-layers.json', assets_layers)

def map_load(pygame):
    tiles_list = utils.json_read(f'maps/0000.json')
    assets_layers = utils.json_read(f'maps/0000-assets-layers.json')
    pyimgs = []
    for asset_layer in assets_layers:
        for asset in asset_layer:
            lib_pyimgs.pyimg_load(pygame, pyimgs, asset)
    return tiles_list, assets_layers, pyimgs

