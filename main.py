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

prompt = f'''
'''

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
        prompt=prompt, 
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
    col_index = (mouse_x - sideview_w - camera_x) // cell_size // camera_scale
    row_index = (mouse_y - camera_y) // cell_size // camera_scale
    return row_index, col_index

def save_map():
    global level_map
    j = json.dumps(level_map, indent=4)
    with open('level_map.json', 'w') as f:
        print(j, file=f)
        print(level_map)

def load_map():
    global level_map
    global sprites_layer_1
    global sprites_layer_2
    global sprites_layer_3
    if os.path.exists('level_map.json'):
        with open('level_map.json') as f:
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
            
scene_images = []

pygame.init()

window_w = 1920
window_h = 1080

sideview_w = 320
sideview_h = window_h

mainview_x = sideview_w
mainview_y = 0
mainview_w = window_w - sideview_w
mainview_h = window_h

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

cell_size = 64

reload_images_map = False

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
                    prompt = prompt[:-1]
                elif event.key == pygame.K_SPACE:
                    prompt += ' '
                elif event.key == pygame.K_DELETE:
                    prompt = ''
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
                    prompt += pygame.key.name(event.key)

    mouse_x, mouse_y = pygame.mouse.get_pos()
    if pygame.mouse.get_pressed()[0] == True: # left click
        if not mouse_left_pressed:
            mouse_left_pressed = True
            if mouse_x < sideview_w and mouse_y < sideview_h:
                active_cell_col = mouse_x // 64
                active_cell_row = mouse_y // 64
        if mouse_x > sideview_w:
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
        if mouse_x > mainview_x and mouse_y > mainview_y and mouse_x < mainview_w and mouse_y < mainview_h:
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

    screen.fill('#101010')

    ############################################################################
    # draw mainview
    ############################################################################

    # draw grid
    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            w = 64*camera_scale
            h = 64*camera_scale
            x = mainview_x + w*j + camera_x
            y = mainview_y + h*i + camera_y
            pygame.draw.rect(
                screen, '#303030', 
                pygame.Rect(
                    x,
                    y, 
                    w,
                    h,
                ), 1
            )
    # draw images
    '''
    if reload_images_map:
        reload_images_map = False
        for i in range(level_map_row_num):
            for j in range(level_map_col_num):
                tile = level_map[i][j]
                if tile != {}:
                    img_filepath = tile['img_filepath']
                    img = pygame.image.load(img_filepath)
                    img = pygame.transform.scale(img, (64, 64))
                    tile['img'] = img

    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            tile = level_map[i][j]
            if tile != {}:
                if tile['img_filepath'] != '':
                    screen.blit(
                        tile['img'], 
                        (
                            camera_x + tile['x']*camera_scale, 
                            camera_y + tile['y']*camera_scale,
                        )
                    )
    '''
    '''
    for row_index in range(level_map_row_num):
        for col_index in range(level_map_col_num):
            img = sprites_layer_1[row_index][col_index]
            if img != None:
                x = sideview_w + col_index*cell_size
                y = row_index*cell_size
                screen.blit(
                    img, 
                    (
                        camera_x + x*camera_scale, 
                        camera_y + y*camera_scale,
                    )
                )
    '''

    for i in range(level_map_row_num):
        for j in range(level_map_col_num):
            img = sprites_layer_1[i][j]
            if img != None:
                w = 64*camera_scale
                h = 64*camera_scale
                x = mainview_x + w*j + camera_x
                y = mainview_y + h*i + camera_y
                screen.blit(img, (x, y))
            img = sprites_layer_2[i][j]
            if img != None:
                w = 64*camera_scale
                h = 64*camera_scale
                x = mainview_x + w*j + camera_x
                y = mainview_y + h*i + camera_y
                screen.blit(img, (x, y))

    '''
    for row_index in range(level_map_row_num):
        for col_index in range(level_map_col_num):
            img = sprites_layer_2[row_index][col_index]
            if img != None:
                x = sideview_w + col_index*cell_size
                y = row_index*cell_size
                screen.blit(
                    img, 
                    (
                        camera_x + x*camera_scale, 
                        camera_y + y*camera_scale,
                    )
                )
    '''

    # draw sideview
    pygame.draw.rect(screen, '#202020', pygame.Rect(0, 0, sideview_w, sideview_h))
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, '#303030', pygame.Rect(j*64+1, i*64+1, 64-1, 64-1))
    for i in range(4):
        for j in range(4):
            asset_filepath = assets_icons[i*4+j]['asset_filepath']
            if asset_filepath != '':
                screen.blit(assets_icons[i*4+j]['img'], (j*64, i*64))
    for i in range(4):
        for j in range(4):
            if active_cell_row == i and active_cell_col == j:
                pygame.draw.rect(screen, '#ffffff', pygame.Rect(j*64+1, i*64+1, 64-1, 64-1), 1)

    
    pygame.font.init()

    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(prompt, False, (255, 255, 255))
    screen.blit(text_surface, (0, 600))

    font = pygame.font.SysFont('Arial', 16)
    row_index, col_index = get_cell_hover_index()
    text_surface = font.render(f'x: {col_index} - y: {row_index}', False, (255, 255, 255))
    screen.blit(text_surface, (0, 500))


    pygame.display.flip()

pygame.quit()
