import os
import json
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
    asset_filepath = f'assets/{i_str}.png'
    image.save(asset_filepath)
    img = pygame.image.load(asset_filepath)
    img = pygame.transform.scale(img, (64, 64))
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
                level_map[i][j]['sprites']['layer_1_filepath'] = img_filepath
                sprites_layer_1[i][j] = pygame.image.load(img_filepath)
                sprites_layer_1[i][j] = pygame.transform.scale(sprites_layer_1[i][j], (64*camera_scale, 64*camera_scale))
            img_filepath = tile['sprites']['layer_2_filepath']
            if img_filepath == asset_filepath:
                level_map[i][j]['sprites']['layer_2_filepath'] = img_filepath
                sprites_layer_2[i][j] = pygame.image.load(img_filepath)
                sprites_layer_2[i][j] = pygame.transform.scale(sprites_layer_2[i][j], (64*camera_scale, 64*camera_scale))

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


#############################################################################
# ;pygame utils
#############################################################################

def get_cell_hover_index():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col_index = (mouse_x - left_frame_w - camera_x) // tile_size // camera_scale
    row_index = (mouse_y - camera_y) // tile_size // camera_scale
    return row_index, col_index

def save_map():
    global level_map
    j = json.dumps(level_map, indent=4)
    with open(current_map_filename, 'w') as f:
        print(j, file=f)
        print(level_map)

def load_map():
    global level_map
    global sprites_layer_1
    global sprites_layer_2
    global sprites_layer_3
    if os.path.exists(current_map_filename):
        with open(current_map_filename) as f:
            level_map = json.load(f)
    else: return
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            tile = level_map[i][j]
            img_filepath = tile['sprites']['layer_1_filepath']
            if img_filepath != '':
                level_map[i][j]['sprites']['layer_1_filepath'] = img_filepath
                sprites_layer_1[i][j] = pygame.image.load(img_filepath)
                sprites_layer_1[i][j] = pygame.transform.scale(sprites_layer_1[i][j], (64, 64))
            else:
                level_map[i][j]['sprites']['layer_1_filepath'] = ''
                sprites_layer_1[i][j] = None
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            tile = level_map[i][j]
            img_filepath = tile['sprites']['layer_2_filepath']
            if img_filepath != '':
                level_map[i][j]['sprites']['layer_2_filepath'] = img_filepath
                sprites_layer_2[i][j] = pygame.image.load(img_filepath)
                sprites_layer_2[i][j] = pygame.transform.scale(sprites_layer_2[i][j], (64, 64))
            else:
                level_map[i][j]['sprites']['layer_2_filepath'] = ''
                sprites_layer_2[i][j] = None

#############################################################################
# ;pygame
#############################################################################

pygame.init()


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

# debug
# level_map[0][0]['sprites']['layer_1_filepath'] = 'assets/0001.png'
# level_map[0][0]['sprites']['layer_2_filepath'] = 'assets/0007.png'

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

load_map()

active_cell_row = 0
active_cell_col = 0

#########################################
# assets
#########################################
assets_filepaths = [f'assets/{filename}' for filename in os.listdir('assets')]
assets_icons = []
for i in range(16):
    if i < 10: i_str = f'000{i}'
    elif i < 100: i_str = f'00{i}'
    elif i < 1000: i_str = f'0{i}'
    elif i < 10000: i_str = f'{i}'
    found = False
    for asset_filepath in assets_filepaths:
        if i_str in asset_filepath:
            img = pygame.image.load(asset_filepath)
            img = pygame.transform.scale(img, (64, 64))
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

asset_col_num = 4
asset_row_num = 4
asset_icon_size = 64
asset_frame_x = asset_tab_frame_x
asset_frame_y = asset_tab_frame_y
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
map_frame_y = 0 + tab_frame_y
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

tile_size = 64

reload_images_map = False

text_area = {
    'text': '',
    'x': 0,
    'y': 500,
    'w': 300,
    'h': 300,
}

def draw_map_grid():
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
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

def draw_map_tiles():
    for row_i in range(level_map_row_num):
        for col_i in range(level_map_col_num):
            draw_map_tile(sprites_layer_1[row_i][col_i], row_i, col_i)
            draw_map_tile(sprites_layer_2[row_i][col_i], row_i, col_i)

def draw_left_frame():
    # frame
    pygame.draw.rect(screen, '#202020', pygame.Rect(0, 0, left_frame_w, left_frame_h))

    # asset tabs
    x = asset_tab_frame_x
    y = asset_tab_frame_y
    w = asset_tab_frame_w
    h = asset_tab_frame_h
    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    tab_i = -1
    tab_w = 80
    tab_i += 1
    x = asset_tab_frame_x + 80*0
    y = asset_tab_frame_y
    w = 80
    h = asset_tab_frame_h
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'AST 0', False, (255, 255, 255))
    screen.blit(text_surface, (x + 10, y + 5))

    # assets
    for row_num in range(asset_row_num):
        for col_num in range(asset_col_num):
            # background
            x = asset_frame_x + asset_tab_frame_x + asset_icon_size*col_num + 1
            y = asset_frame_y + asset_tab_frame_h + asset_icon_size*row_num + 1
            w = asset_icon_size - 1
            h = asset_icon_size - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
            # img
            asset_filepath = assets_icons[row_num*asset_col_num+col_num]['asset_filepath']
            if asset_filepath != '':
                asset_icon = assets_icons[row_num*asset_col_num + col_num]['img']
                x = asset_frame_x + asset_tab_frame_x + asset_icon_size*col_num
                y = asset_frame_y + asset_tab_frame_h + asset_icon_size*row_num
                screen.blit(asset_icon, (x, y))
            # border selected
            if active_cell_row == row_num and active_cell_col == col_num:
                x = asset_frame_x + asset_tab_frame_x + asset_icon_size*col_num + 1
                y = asset_frame_y + asset_tab_frame_h + asset_icon_size*row_num + 1
                w = asset_icon_size - 1
                h = asset_icon_size - 1
                pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1,)


def draw():
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(f'AST 0', False, (255, 255, 255))

    # window bg
    screen.fill('#101010')

    # map
    draw_map_grid()
    draw_map_tiles()

    # left frame
    draw_left_frame()

    ## text area
    pygame.font.init()

    pygame.draw.rect(screen, '#ffffff', pygame.Rect(text_area['x'], text_area['y'], text_area['w'], text_area['h']), 1)

    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(text_area['text'], False, (255, 255, 255))
    screen.blit(text_surface, (text_area['x'], text_area['y']))

    ## debug
    font = pygame.font.SysFont('Arial', 16)
    row_index, col_index = get_cell_hover_index()
    text_surface = font.render(f'x: {col_index} - y: {row_index}', False, (255, 255, 255))
    screen.blit(text_surface, (0, 400))

    ## right frame
    pygame.draw.rect(screen, '#303030', pygame.Rect(right_frame_x, right_frame_y, right_frame_w, right_frame_h))

    ## tab frame
    pygame.draw.rect(screen, '#303030', pygame.Rect(tab_frame_x, tab_frame_y, tab_frame_w, tab_frame_h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(tab_frame_x, tab_frame_y, tab_frame_w, tab_frame_h), 1)
    tab_i = -1
    tab_w = 80
    tab_i += 1
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(tab_frame_x + tab_w*tab_i, tab_frame_y, tab_w, tab_frame_h), 1)
    text_surface = font.render(f'map {tab_i}', False, (255, 255, 255))
    screen.blit(text_surface, (tab_frame_x + tab_w*tab_i + 10, tab_frame_y + 5))

    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            camera_scale += event.y
            if camera_scale < 1: camera_scale = 1
            elif camera_scale > 8: camera_scale = 8
            for i in range(level_map_row_num):
                for j in range(level_map_col_num):
                    if sprites_layer_1[i][j] != None:
                        sprites_layer_1[i][j] = pygame.transform.scale(sprites_layer_1[i][j], (64*camera_scale, 64*camera_scale))
                    if sprites_layer_2[i][j] != None:
                        sprites_layer_2[i][j] = pygame.transform.scale(sprites_layer_2[i][j], (64*camera_scale, 64*camera_scale))
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
                    if active_cell_row == 0:
                        thread = Thread(target = gen_image)
                        thread.start()
                        thread.join()
                        index = active_cell_row*4+active_cell_col
                        if index < 10: i_str = f'000{index}'
                        elif index < 100: i_str = f'00{index}'
                        elif index < 1000: i_str = f'0{index}'
                        elif index < 10000: i_str = f'{index}'
                        image = Image.open(f'assets-tmp/{i_str}.png')
                        asset_filepath = f'assets/{i_str}.png'
                        image.save(asset_filepath)
                        img = pygame.image.load(asset_filepath)
                        img = pygame.transform.scale(img, (64, 64))
                        assets_icons[index] = {
                            'asset_filepath': asset_filepath,
                            'asset_filename': asset_filepath.split('/')[-1],
                            'img': img,
                        }
                    else:
                        thread = Thread(target = gen_image)
                        thread.start()
                        thread.join()
                        thread = Thread(target = bg_remove)
                        thread.start()
                        thread.join()
                    # img = pygame.image.load('test-1.png')
                    # img = pygame.transform.scale(img, (64, 64))
                    reload_images_map = True
                elif event.key == pygame.K_PLUS:
                    pass
                    # level_map_row_num += 1
                    # level_map_col_num += 1
                elif event.key == pygame.K_MINUS:
                    pass
                    # level_map_row_num -= 1
                    # level_map_col_num -= 1
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    save_map()
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    load_map()
                elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                    pass
                else:
                    text_area['text'] += pygame.key.name(event.key)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == True: # left click
        if not mouse_left_pressed:
            mouse_left_pressed = True
            ## asset panel
            if (mouse_x >= asset_frame_x and 
                mouse_x < asset_frame_x + asset_icon_size*asset_col_num and 
                mouse_y >= asset_frame_y and 
                mouse_y < asset_frame_y + asset_icon_size*asset_row_num):
                active_cell_col = mouse_x // asset_icon_size
                active_cell_row = mouse_y // asset_icon_size
            elif mouse_x >= map_frame_x and mouse_x < map_frame_x + map_frame_w and mouse_y >= map_frame_y and mouse_y < map_frame_y + map_frame_h:
                tab_i = -1
                tab_w = 80
                tab_i += 1
                if mouse_x >= map_frame_x + tab_w*tab_i and mouse_x < map_frame_x + tab_w*tab_i + tab_w and mouse_y >= map_frame_y and mouse_y < map_frame_y + map_frame_h:
                    current_map_filename = maps_filenames[0]
                    load_map()
                tab_i += 1
                if mouse_x >= map_frame_x + tab_w*tab_i and mouse_x < map_frame_x + tab_w*tab_i + tab_w and mouse_y >= map_frame_y and mouse_y < map_frame_y + map_frame_h:
                    current_map_filename = maps_filenames[1]
                    load_map()
        if mouse_x > left_frame_w and mouse_x < right_frame_x and mouse_y > tab_frame_h:
            row_index, col_index = get_cell_hover_index()
            if row_index >= 0 and row_index < level_map_row_num and col_index >= 0 and col_index < level_map_col_num:
                asset_icon = assets_icons[active_cell_row*4+active_cell_col]
                img_filepath = asset_icon['asset_filepath']
                if img_filepath != '':
                    if active_cell_row == 0:
                        level_map[row_index][col_index]['sprites']['layer_1_filepath'] = img_filepath
                        sprites_layer_1[row_index][col_index] = pygame.image.load(img_filepath)
                        sprites_layer_1[row_index][col_index] = pygame.transform.scale(sprites_layer_1[row_index][col_index], (64*camera_scale, 64*camera_scale))
                    else:
                        level_map[row_index][col_index]['sprites']['layer_2_filepath'] = img_filepath
                        sprites_layer_2[row_index][col_index] = pygame.image.load(img_filepath)
                        sprites_layer_2[row_index][col_index] = pygame.transform.scale(sprites_layer_2[row_index][col_index], (64*camera_scale, 64*camera_scale))
                else:
                    level_map[row_index][col_index]['sprites']['layer_1_filepath'] = ''
                    level_map[row_index][col_index]['sprites']['layer_2_filepath'] = ''
                    sprites_layer_1[row_index][col_index] = None
                    sprites_layer_2[row_index][col_index] = None
    else:
        mouse_left_pressed = False
    if pygame.mouse.get_pressed()[2] == True: # right click
        if mouse_x > map_frame_x and mouse_y > map_frame_y and mouse_x < map_frame_w and mouse_y < map_frame_h:
            row_index, col_index = get_cell_hover_index()
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
    
    draw()

pygame.quit()
