import os
import utils

def asset_load(filepath):
    asset = utils.json_read(filepath)
    return asset

def assets_load(foldername):
    filepaths = [f'assets/{foldername}/jsons/{filename}' for filename in os.listdir(f'assets/{foldername}/jsons')]
    assets = []
    for filepath in filepaths:
        asset = asset_load(filepath)
        assets.append(asset)
    return assets

def asset_get_by_id(assets, asset_id):
    asset = {}
    for _asset in assets:
        _asset_id = _asset['image_filepath'].split('/')[-1].split('.')[0]
        if _asset_id == asset_id:
            asset = _asset
            break
    return asset

def asset_get_by_filepath(assets_layers, filepath):
    asset = {}
    for asset_layer in assets_layers:
        found = False
        for _asset in asset_layer:
            if filepath == _asset['image_filepath']:
                asset = _asset
                found = True
                break
        if found:
            break
    return asset

def asset_get_index(row_i, col_i, col_n):
    asset_index = row_i*col_n + col_i
    return asset_index

def asset_get_active(assets, row_i, col_i, col_n):
    asset_index = asset_get_index(row_i, col_i, col_n)
    asset_id = utils.format_id(asset_index)
    asset = asset_get_by_id(assets, asset_id)
    return asset

def asset_offset_up(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['y_offset'] -= 1

def asset_offset_down(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['y_offset'] += 1

def asset_offset_left(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['x_offset'] -= 1

def asset_offset_right(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['x_offset'] += 1

def asset_increase_size(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['size_mul'] += 0.1

def asset_decrease_size(pannel_assets, assets_layer_cur):
    row_i = pannel_assets['row_cur']
    col_i = pannel_assets['col_cur']
    col_n = pannel_assets['col_n']
    asset = asset_get_active(assets_layer_cur, row_i, col_i, col_n)
    asset['size_mul'] -= 0.1

