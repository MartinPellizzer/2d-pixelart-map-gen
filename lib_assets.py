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

def asset_get_by_filepath(assets_l0_jsons, assets_l1_jsons, filepath):
    asset = {}
    assets = [_asset for _asset in assets_l0_jsons if _asset['image_filepath'] == filepath]
    if assets == []:
        assets = [_asset for _asset in assets_l1_jsons if _asset['image_filepath'] == filepath]
    if assets != []:
        asset = assets[0]
    return asset

def asset_get_index(row_i, col_i, col_n):
    asset_index = row_i*col_n + col_i
    return asset_index

def asset_get_active(assets, row_i, col_i, col_n):
    asset_index = asset_get_index(row_i, col_i, col_n)
    asset_id = utils.format_id(asset_index)
    asset = asset_get_by_id(assets, asset_id)
    return asset

