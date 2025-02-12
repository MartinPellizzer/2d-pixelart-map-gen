import os
import json
import shutil
from threading import Thread

import pygame

import torch
from diffusers import StableDiffusionXLPipeline
from diffusers import StableDiffusionPipeline
from diffusers import DPMSolverMultistepScheduler

from PIL import Image
from torchvision import transforms
import matplotlib.pyplot as plt
from transformers import AutoModelForImageSegmentation


vault = f'/home/ubuntu/vault'

pipe = None
bg_model = None
prompt = f'''
    a wooden chair,
    minimalist,
    pixel art,
'''

prompt = f''


#############################################################################
# ;ai
#############################################################################
def bg_remove():
    global active_cell_row
    global active_cell_col
    index = active_cell_row*4+active_cell_col
    if index < 10: i_str = f'000{index}'
    elif index < 100: i_str = f'00{index}'
    elif index < 1000: i_str = f'0{index}'
    elif index < 10000: i_str = f'{index}'
    global bg_model
    if not bg_model:
        bg_model = AutoModelForImageSegmentation.from_pretrained('briaai/RMBG-2.0', trust_remote_code=True)
    torch.set_float32_matmul_precision(['high', 'highest'][0])
    bg_model.to('cuda')
    bg_model.eval()
    # Data settings
    image_size = (1024, 1024)
    transform_image = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(f'assets-tmp/{i_str}.png')
    input_images = transform_image(image).unsqueeze(0).to('cuda')
    # Prediction
    with torch.no_grad():
        preds = bg_model(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)
    asset_filepath = f'assets-tmp/{i_str}-transparent.png'
    image.save(asset_filepath)

if 0:
    def gen_image():
        global active_cell_row
        global active_cell_col
        global prompt
        global pipe
        model = {
            'checkpoint_filepath': f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors',
            'lora_filepath': f'{vault}/stable-diffusion/loras/xl/Hand-Painted_2d_Seamless_Textures.safetensors',
            'prompt': f'''
                sd seamless hand-painted texture of 
                small stone block floor,
                interlocking pattern, worn edges,
                masterpiece, detailed, high quality, high resolution, 4k texture
            '''
        }
        model = {
            'checkpoint_filepath': f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors',
            'lora_filepath': f'{vault}/stable-diffusion/loras/xl/pixel-art-xl-v1.1.safetensors',
            'prompt': f'''
                a seamless grass texture,
                minimalist,
                pixel art,
                white background,
            ''',
        }
        model = {
            'checkpoint_filepath': f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors',
            'lora_filepath': f'{vault}/stable-diffusion/loras/xl/pixel-art-xl-v1.1.safetensors',
            'prompt': f'''
                a wooden chair,
                minimalist,
                pixel art,
            ''',
        }
        if not pipe:
            pipe = StableDiffusionXLPipeline.from_single_file(
                model['checkpoint_filepath'], 
                torch_dtype=torch.float16, 
                use_safetensors=True, 
                variant="fp16"
            ).to('cuda')
            pipe.load_lora_weights(model['lora_filepath'])
        image = pipe(
            prompt=text_area['text'], 
            cross_attention_kwargs={'scale': 1}, 
            width=1024, 
            height=1024, 
            num_inference_steps=20, 
            guidance_scale=7.0
        ).images[0]
        index = active_cell_row*4+active_cell_col
        if index < 10: i_str = f'000{index}'
        elif index < 100: i_str = f'00{index}'
        elif index < 1000: i_str = f'0{index}'
        elif index < 10000: i_str = f'{index}'
        image.save(f'assets-tmp/{i_str}.png')
        # transparent or not
        if active_cell_row == 0:
            asset_filepath = f'assets-tmp/{i_str}.png'
        else:
            bg_remove()
            asset_filepath = f'assets-tmp/{i_str}-transparent.png'
        # reload map
        shutil.copy2(asset_filepath, f'assets/{i_str}.png')
        asset_filepath = f'assets/{i_str}.png'
        img = pygame.image.load(asset_filepath)
        img = pygame.transform.scale(img, (tile_size, tile_size))
        assets_icons[index] = {
            'asset_filepath': asset_filepath,
            'asset_filename': asset_filepath.split('/')[-1],
            'img': img,
        }
        for i in range(level_map_row_num):
            for j in range(level_map_col_num):
                tile = level_map[i][j]
                img_filepath = tile['sprites']['layer_1_filepath']
                if img_filepath == asset_filepath:
                    print(img_filepath, asset_filepath)
                    level_map[i][j]['sprites']['layer_1_filepath'] = img_filepath
                    sprites_layer_1[i][j] = pygame.image.load(img_filepath)
                    sprites_layer_1[i][j] = pygame.transform.scale(sprites_layer_1[i][j], (tile_size*camera_scale, tile_size*camera_scale))
                img_filepath = tile['sprites']['layer_2_filepath']
                if img_filepath == asset_filepath:
                    level_map[i][j]['sprites']['layer_2_filepath'] = img_filepath
                    sprites_layer_2[i][j] = pygame.image.load(img_filepath)
                    sprites_layer_2[i][j] = pygame.transform.scale(sprites_layer_2[i][j], (tile_size*camera_scale, tile_size*camera_scale))

def gen_image():
    global active_cell_row
    global active_cell_col
    global prompt
    global pipe
    model = {
        'checkpoint_filepath': f'{vault}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors',
        'lora_filepath': f'{vault}/stable-diffusion/loras/xl/pixel-art-xl-v1.1.safetensors',
        'prompt': f'''
            a wooden chair,
            minimalist,
            pixel art,
        ''',
    }
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            model['checkpoint_filepath'], 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.load_lora_weights(model['lora_filepath'])
    image = pipe(
        prompt=text_area['text'], 
        cross_attention_kwargs={'scale': 1}, 
        width=1024, 
        height=1024, 
        num_inference_steps=20, 
        guidance_scale=7.0
    ).images[0]
    index = active_cell_row*level_map['col_num']+active_cell_col
    if index < 10: i_str = f'000{index}'
    elif index < 100: i_str = f'00{index}'
    elif index < 1000: i_str = f'0{index}'
    elif index < 10000: i_str = f'{index}'
    image.save(f'assets-tmp/{i_str}.png')
    # transparent or not
    if active_cell_row == 0:
        asset_filepath = f'assets-tmp/{i_str}.png'
    else:
        bg_remove()
        asset_filepath = f'assets-tmp/{i_str}-transparent.png'
    # reload map
    shutil.copy2(asset_filepath, f'assets-packs/{level_map["asset_pack_name"]}/{i_str}.png')
    asset_filepath = f'assets-packs/{level_map["asset_pack_name"]}/{i_str}.png'
    img = pygame.image.load(asset_filepath)
    img = pygame.transform.scale(img, (tile_size, tile_size))
    assets_icons[index] = {
        'asset_filepath': asset_filepath,
        'asset_filename': asset_filepath.split('/')[-1],
        'img': img,
    }
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            tile = level_map['tiles'][i*level_map['col_num']+j]
            if tile[0] == asset_filepath:
                level_map['tiles'][i*level_map['col_num']+j][0] = img_filepath
                sprites_layer_1[i*level_map['col_num']+j][0] = pygame.image.load(img_filepath)
                sprites_layer_1[i*level_map['col_num']+j][0] = pygame.transform.scale(
                    sprites_layer_1[i*level_map['col_num']+j][0], 
                    (tile_size*camera_scale, tile_size*camera_scale)
                )
            if tile[1] == asset_filepath:
                level_map['tiles'][i*level_map['col_num']+j][1] = img_filepath
                sprites_layer_2[i*level_map['col_num']+j][1] = pygame.image.load(img_filepath)
                sprites_layer_2[i*level_map['col_num']+j][1] = pygame.transform.scale(
                    sprites_layer_2[i*level_map['col_num']+j][1], 
                    (tile_size*camera_scale, tile_size*camera_scale)
                )

#############################################################################
# ;pygame utils
#############################################################################
tile_size = 64

def get_map_cell_hover_index():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col_index = (mouse_x - map_frame_x - camera_x) // tile_size // camera_scale
    row_index = (mouse_y - map_frame_y - camera_y) // tile_size // camera_scale
    return row_index, col_index

def save_map():
    global level_map
    j = json.dumps(level_map, indent=4)
    with open(current_map_filename, 'w') as f:
        print(j, file=f)
        print(level_map)

def load_map():
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            tile = level_map[i][j]
            img_filepath = tile['sprites']['layer_1_filepath']
            if img_filepath != '':
                level_map[i][j]['sprites']['layer_1_filepath'] = img_filepath
                sprites_layer_1[i][j] = pygame.image.load(img_filepath)
                sprites_layer_1[i][j] = pygame.transform.scale(sprites_layer_1[i][j], (tile_size, tile_size))
            else:
                level_map[i][j]['sprites']['layer_1_filepath'] = ''
                sprites_layer_1[i][j] = None
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            tile = level_map[i*level_map['col_num']*j]
            img_filepath = tile['sprites']['layer_2_filepath']
            if img_filepath != '':
                level_map[i][j]['sprites']['layer_2_filepath'] = img_filepath
                sprites_layer_2[i][j] = pygame.image.load(img_filepath)
                sprites_layer_2[i][j] = pygame.transform.scale(sprites_layer_2[i][j], (tile_size, tile_size))
            else:
                level_map[i][j]['sprites']['layer_2_filepath'] = ''
                sprites_layer_2[i][j] = None

def open_map():
    global level_map
    global sprites_layer_1
    global sprites_layer_2
    global sprites_layer_3
    if os.path.exists(current_map_filename):
        with open(current_map_filename) as f:
            level_map = json.load(f)
    else: return
    load_map()

#############################################################################
# ;new data
#############################################################################

def load_asset_pack(asset_pack_name):
    asset_pack_folderpath = f'assets-packs/{asset_pack_name}'
    assets_filepaths = [
        f'{asset_pack_folderpath}/{filename}' 
        for filename in os.listdir(f'{asset_pack_folderpath}')
    ]
    for i in range(asset_col_num* asset_row_num):
        if i < 10: i_str = f'000{i}'
        elif i < 100: i_str = f'00{i}'
        elif i < 1000: i_str = f'0{i}'
        elif i < 10000: i_str = f'{i}'
        found = False
        for asset_filepath in assets_filepaths:
            if i_str in asset_filepath:
                img = pygame.image.load(asset_filepath)
                img = pygame.transform.scale(img, (tile_size, tile_size))
                assets_icons.append({
                    'asset_filepath': asset_filepath,
                    'asset_filename': asset_filepath.split('/')[-1],
                    'img': img,
                })
                found = True
                break
        if not found:
            assets_icons.append({
                'asset_filepath': '',
                'asset_filename': '',
                'img': '',
            })
            
# init new map system
level_map = {
    'id': '0',
    'asset_pack_name': '0000',
    'row_num': 8,
    'col_num': 8,
    'tiles': [],
}

for i in range(level_map['row_num'] * level_map['col_num']):
    level_map['tiles'].append(['', '', ''])

sprites_layer_1 = []
sprites_layer_2 = []
sprites_layer_3 = []

for i in range(level_map['row_num'] * level_map['col_num']):
    sprites_layer_1.append(None)
    sprites_layer_2.append(None)
    sprites_layer_3.append(None)

assets_icons = []
asset_col_num = 4
asset_row_num = 4
asset_icon_size = 64
load_asset_pack(level_map['asset_pack_name'])



#############################################################################
# ;pygame
#############################################################################

pygame.init()


'''
# init map old
maps_filenames = [
    'map_0.json',
    'map_1.json',
    'map_2.json',
]
current_map_filename = maps_filenames[0]

level_map_row_num = 8
level_map_col_num = 8
level_map = []
for i in range(level_map_row_num):
    row = []
    for j in range(level_map_col_num):
        row.append({
            'sprites': {
                'layer_1_filepath': '',
                'layer_2_filepath': '',
                'layer_3_filepath': '',
            },
            'row_index': i,
            'col_index': j,
        })
    level_map.append(row)

sprites_layer_1 = []
for i in range(level_map_row_num):
    row = []
    for j in range(level_map_col_num):
        row.append(None)
    sprites_layer_1.append(row)

sprites_layer_2 = []
for i in range(level_map_row_num):
    row = []
    for j in range(level_map_col_num):
        row.append(None)
    sprites_layer_2.append(row)

sprites_layer_3 = []
for i in range(level_map_row_num):
    row = []
    for j in range(level_map_col_num):
        row.append(None)
    sprites_layer_3.append(row)

open_map()

'''

active_cell_row = 0
active_cell_col = 0

#########################################
# assets
#########################################
'''
def load_asset_pack():
    global current_asset_pack_filepath
    assets_filepaths = [f'{current_asset_pack_filepath}/{filename}' for filename in os.listdir(f'{current_asset_pack_filepath}')]
    for i in range(16):
        if i < 10: i_str = f'000{i}'
        elif i < 100: i_str = f'00{i}'
        elif i < 1000: i_str = f'0{i}'
        elif i < 10000: i_str = f'{i}'
        found = False
        for asset_filepath in assets_filepaths:
            if i_str in asset_filepath:
                img = pygame.image.load(asset_filepath)
                img = pygame.transform.scale(img, (tile_size, tile_size))
                assets_icons.append({
                    'asset_filepath': asset_filepath,
                    'asset_filename': asset_filepath.split('/')[-1],
                    'img': img,
                })
                found = True
                break
        if not found:
            assets_icons.append({
                'asset_filepath': '',
                'asset_filename': '',
                'img': '',
            })
            

assets_packs_filepaths = [
    f'assets',
    f'assets-packs/pack-0000',
    f'assets-packs/pack-0001',
    f'assets-packs/pack-0002',
]
current_asset_pack_filepath = assets_packs_filepaths[0]
assets_icons = []
load_asset_pack()
'''


#########################################
# frames
#########################################
window_w = 1920
window_h = 1080

left_frame_x = 0
left_frame_y = 0
left_frame_w = 320
left_frame_h = window_h

asset_tab_frame_x = left_frame_x
asset_tab_frame_y = left_frame_y
asset_tab_frame_w = left_frame_w
asset_tab_frame_h = 30

asset_frame_x = asset_tab_frame_x
asset_frame_y = asset_tab_frame_h
asset_frame_w = asset_icon_size*asset_col_num
asset_frame_h = asset_icon_size*asset_row_num

right_frame_w = 320
right_frame_h = window_h
right_frame_x = window_w - right_frame_w
right_frame_y = 0

tab_frame_x = left_frame_w
tab_frame_y = 0
tab_frame_w = window_w - left_frame_w - right_frame_w
tab_frame_h = 30

map_frame_x = left_frame_w
map_frame_y = 0 + tab_frame_h
map_frame_w = window_w - left_frame_w - right_frame_w
map_frame_h = window_h

screen = pygame.display.set_mode([window_w, window_h])

camera_x = 0
camera_y = 0
mouse_x = 0
mouse_y = 0

camera_x_start = 0
camera_y_start = 0
mouse_x_start = 0
mouse_y_start = 0
is_panning_begin = False

camera_scale = 1

running = True


reload_images_map = False

text_area = {
    'text': '',
    'x': 0,
    'y': 500,
    'w': 300,
    'h': 300,
}

############################################################################
# ;draw
############################################################################

'''
def draw_map_grid():
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            w = tile_size*camera_scale
            h = tile_size*camera_scale
            x = map_frame_x + w*j + camera_x
            y = map_frame_y + h*i + camera_y
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)
'''

def draw_map_grid():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera_scale
            h = tile_size*camera_scale
            x = map_frame_x + w*j + camera_x
            y = map_frame_y + h*i + camera_y
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)

def draw_map_tile(img, row_i, col_i):
    if img != None:
        w = tile_size*camera_scale
        h = tile_size*camera_scale
        x = map_frame_x + w*col_i + camera_x
        y = map_frame_y + h*row_i + camera_y
        screen.blit(img, (x, y))

'''
def draw_map_tiles():
    for row_i in range(level_map_row_num):
        for col_i in range(level_map_col_num):
            draw_map_tile(sprites_layer_1[row_i][col_i], row_i, col_i)
            draw_map_tile(sprites_layer_2[row_i][col_i], row_i, col_i)
'''

def draw_map_tiles():
    for row_i in range(level_map['row_num']):
        for col_i in range(level_map['col_num']):
            draw_map_tile(sprites_layer_1[row_i*level_map['col_num']+col_i], row_i, col_i)
            draw_map_tile(sprites_layer_2[row_i*level_map['col_num']+col_i], row_i, col_i)


def draw_left_frame():
    # assets
    for row_num in range(asset_row_num):
        for col_num in range(asset_col_num):
            # background
            x = asset_frame_x + asset_icon_size*col_num + 1
            y = asset_frame_y + asset_icon_size*row_num + 1
            w = asset_icon_size - 1
            h = asset_icon_size - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
            # img
            # jump
            asset_filepath = assets_icons[row_num*asset_col_num+col_num]['asset_filepath']
            if asset_filepath != '':
                asset_icon = assets_icons[row_num*asset_col_num + col_num]['img']
                x = asset_frame_x + asset_icon_size*col_num
                y = asset_frame_y + asset_icon_size*row_num
                screen.blit(asset_icon, (x, y))
            # border selected
            if active_cell_row == row_num and active_cell_col == col_num:
                x = asset_frame_x + asset_icon_size*col_num + 1
                y = asset_frame_y + asset_icon_size*row_num + 1
                w = asset_icon_size - 1
                h = asset_icon_size - 1
                pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1,)


'''
def draw_left_frame():
    # assets
    for row_num in range(asset_row_num):
        for col_num in range(asset_col_num):
            # background
            x = asset_frame_x + asset_icon_size*col_num + 1
            y = asset_frame_y + asset_icon_size*row_num + 1
            w = asset_icon_size - 1
            h = asset_icon_size - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
            # img
            asset_filepath = assets_icons[row_num*asset_col_num+col_num]['asset_filepath']
            if asset_filepath != '':
                asset_icon = assets_icons[row_num*asset_col_num + col_num]['img']
                x = asset_frame_x + asset_icon_size*col_num
                y = asset_frame_y + asset_icon_size*row_num
                screen.blit(asset_icon, (x, y))
            # border selected
            if active_cell_row == row_num and active_cell_col == col_num:
                x = asset_frame_x + asset_icon_size*col_num + 1
                y = asset_frame_y + asset_icon_size*row_num + 1
                w = asset_icon_size - 1
                h = asset_icon_size - 1
                pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1,)
'''

def draw_left_tabs():
    font = pygame.font.SysFont('Arial', 16)
    x = asset_tab_frame_x
    y = asset_tab_frame_y
    w = asset_tab_frame_w
    h = asset_tab_frame_h
    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    tab_i = -1
    tab_w = 80
    for tab_i in range(2):
        x = asset_tab_frame_x + tab_w*tab_i
        y = asset_tab_frame_y
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, tab_w, h), 1)
        text_surface = font.render(f'ast {tab_i}', False, (255, 255, 255))
        screen.blit(text_surface, (x + 10, y + 5))

def draw_right_frame():
    pygame.draw.rect(screen, '#303030', pygame.Rect(right_frame_x, right_frame_y, right_frame_w, right_frame_h))

def draw_map_tabs():
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'AST 0', False, (255, 255, 255))
    pygame.draw.rect(screen, '#303030', pygame.Rect(tab_frame_x, tab_frame_y, tab_frame_w, tab_frame_h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(tab_frame_x, tab_frame_y, tab_frame_w, tab_frame_h), 1)
    tab_i = -1
    tab_w = 80
    for tab_i in range(2):
        x1 = tab_frame_x + tab_w*tab_i
        y1 = tab_frame_y
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x1, y1, tab_w, tab_frame_h), 1)
        text_surface = font.render(f'map {tab_i}', False, (255, 255, 255))
        screen.blit(text_surface, (x1 + 10, y1 + 5))

def draw_debug():
    font = pygame.font.SysFont('Arial', 16)
    row_index, col_index = get_map_cell_hover_index()
    text_surface = font.render(f'x: {col_index} - y: {row_index}', False, (255, 255, 255))
    screen.blit(text_surface, (0, 400))

def draw_prompt():
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(text_area['x'], text_area['y'], text_area['w'], text_area['h']), 1)
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(text_area['text'], False, (255, 255, 255))
    screen.blit(text_surface, (text_area['x'], text_area['y']))

def draw_main():
    pygame.font.init()
    # window bg
    screen.fill('#101010')
    # map
    draw_map_grid()
    draw_map_tiles()
    draw_map_tabs()
    # left frame
    pygame.draw.rect(screen, '#202020', pygame.Rect(0, 0, left_frame_w, left_frame_h))
    draw_left_frame()
    draw_left_tabs()
    ## right frame
    draw_right_frame()
    ## prompt
    draw_prompt()
    ## debug
    draw_debug()
    pygame.display.flip()

###################################################################################
# ;input
###################################################################################
def input_mousewheel():
    global camera_scale
    camera_scale += event.y
    if camera_scale < 1: camera_scale = 1
    elif camera_scale > 8: camera_scale = 8
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            if sprites_layer_1[i][j] != None:
                sprites_layer_1[i][j] = pygame.transform.scale(
                    sprites_layer_1[i][j], (tile_size*camera_scale, tile_size*camera_scale)
                )
            if sprites_layer_2[i][j] != None:
                sprites_layer_2[i][j] = pygame.transform.scale(
                    sprites_layer_2[i][j], (tile_size*camera_scale, tile_size*camera_scale)
                )

def input_return():
    thread = Thread(target = gen_image)
    thread.start()
    thread.join()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            input_mousewheel()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT:
                pass
            else:
                if event.key == pygame.K_BACKSPACE:
                    text_area['text'] = text_area['text'][:-1]
                elif event.key == pygame.K_SPACE:
                    text_area['text'] += ' '
                elif event.key == pygame.K_DELETE:
                    text_area['text'] = ''
                elif event.key == pygame.K_RETURN:
                    input_return()
                elif event.key == pygame.K_PLUS:
                    pass
                elif event.key == pygame.K_MINUS:
                    pass
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_map()
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    open_map()
                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pass
                else:
                    text_area['text'] += pygame.key.name(event.key)

    '''
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == True: # left click
        if not mouse_left_pressed:
            mouse_left_pressed = True
            ## asset panel
            x1 = asset_frame_x
            y1 = asset_frame_y
            x2 = asset_frame_x + asset_icon_size*asset_col_num
            y2 = asset_frame_y + asset_icon_size*asset_row_num
            if (mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2):
                print(x1, y1, x2, y2)
                active_cell_col = (mouse_x - asset_frame_x) // asset_icon_size
                active_cell_row = (mouse_y - asset_frame_y) // asset_icon_size
            ## map tab panel
            x1 = tab_frame_x
            y1 = tab_frame_y
            x2 = tab_frame_x + tab_frame_w
            y2 = tab_frame_y + tab_frame_h
            if mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2:
                tab_i = -1
                tab_w = 80
                for tab_i in range(2):
                    x1 = tab_frame_x + tab_w*tab_i
                    y1 = tab_frame_y
                    x2 = tab_frame_x + tab_w*tab_i + tab_w
                    y2 = tab_frame_y + map_frame_h
                    if mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2:
                        if current_map_filename != maps_filenames[tab_i]:
                            current_map_filename = maps_filenames[tab_i]
                            open_map()
            ## asset tab panel
            x1 = asset_tab_frame_x
            y1 = asset_tab_frame_y
            x2 = asset_tab_frame_x + asset_tab_frame_w
            y2 = asset_tab_frame_y + asset_tab_frame_h
            if mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2:
                tab_i = -1
                tab_w = 80
                for tab_i in range(2):
                    x1 = asset_tab_frame_x + tab_w*tab_i
                    y1 = asset_tab_frame_y
                    x2 = asset_tab_frame_x + tab_w*tab_i + tab_w
                    y2 = asset_tab_frame_y + asset_tab_frame_h
                    if mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2:
                        if current_asset_pack_filepath != assets_packs_filepaths[tab_i]:
                            current_asset_pack_filepath = assets_packs_filepaths[tab_i]
                            load_asset_pack()

        ## map frame
        x1 = map_frame_x
        y1 = map_frame_y
        x2 = map_frame_x + map_frame_w
        y2 = map_frame_y + map_frame_h
        if mouse_x >= x1 and mouse_x < x2 and mouse_y >= y1 and mouse_y < y2:
            row_index, col_index = get_map_cell_hover_index()
            if row_index >= 0 and row_index < level_map_row_num and col_index >= 0 and col_index < level_map_col_num:
                asset_icon = assets_icons[active_cell_row*4+active_cell_col]
                img_filepath = asset_icon['asset_filepath']
                if img_filepath != '':
                    if active_cell_row == 0:
                        level_map[row_index][col_index]['sprites']['layer_1_filepath'] = img_filepath
                        sprites_layer_1[row_index][col_index] = pygame.image.load(img_filepath)
                        sprites_layer_1[row_index][col_index] = pygame.transform.scale(sprites_layer_1[row_index][col_index], (tile_size*camera_scale, tile_size*camera_scale))
                    else:
                        level_map[row_index][col_index]['sprites']['layer_2_filepath'] = img_filepath
                        sprites_layer_2[row_index][col_index] = pygame.image.load(img_filepath)
                        sprites_layer_2[row_index][col_index] = pygame.transform.scale(sprites_layer_2[row_index][col_index], (tile_size*camera_scale, tile_size*camera_scale))
                else:
                    level_map[row_index][col_index]['sprites']['layer_1_filepath'] = ''
                    level_map[row_index][col_index]['sprites']['layer_2_filepath'] = ''
                    sprites_layer_1[row_index][col_index] = None
                    sprites_layer_2[row_index][col_index] = None
    else:
        mouse_left_pressed = False
    if pygame.mouse.get_pressed()[2] == True: # right click
        if mouse_x > map_frame_x and mouse_y > map_frame_y and mouse_x < map_frame_w and mouse_y < map_frame_h:
            row_index, col_index = get_map_cell_hover_index()
            if row_index >= 0 and row_index < level_map_row_num and col_index >= 0 and col_index < level_map_col_num:
                if level_map[row_index][col_index] != {}:
                    level_map[row_index][col_index]['sprites']['layer_1_filepath'] = ''
                    level_map[row_index][col_index]['sprites']['layer_2_filepath'] = ''
                    sprites_layer_1[row_index][col_index] = None
                    sprites_layer_2[row_index][col_index] = None
                    sprites_layer_3[row_index][col_index] = None
    if pygame.mouse.get_pressed()[1] == True: # middle click
        if not is_panning_begin:
            is_panning_begin = True
            camera_x_start = camera_x
            camera_y_start = camera_y
            mouse_x_start = mouse_x
            mouse_y_start = mouse_y
        camera_x = camera_x_start + mouse_x - mouse_x_start
        camera_y = camera_y_start + mouse_y - mouse_y_start
    else:
        is_panning_begin = False
    '''
    
    draw_main()

pygame.quit()
