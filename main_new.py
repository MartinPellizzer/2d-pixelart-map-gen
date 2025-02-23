import copy
import pygame

window_w = 1920
window_h = 1080

tile_size = 32

assets_icons_clean = {
    'row_num': 15,
    'col_num': 5,
    'icon_size': 64,
    'row_active': 0,
    'col_active': 0,
    'icons': [],
}

assets_icons = copy.deepcopy(assets_icons_clean)

#######################################
# ;frames
#######################################
camera = {
    'x': 0,
    'y': 0,
    'zoom': 4,
}

frame_assets_tabs = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': 30,
}

frame_assets_icons = {
    'x': 0,
    'y': frame_assets_tabs['h'],
    'w': assets_icons['icon_size'] * assets_icons['col_num'],
    'h': assets_icons['icon_size'] * assets_icons['row_num'],
}

left_frame = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': window_h,
}

right_frame = {
    'x': 0,
    'y': 0,
    'w': 320,
    'h': window_h,
}
right_frame['x'] = window_w - right_frame['w']

central_frame = {
    'x': left_frame['w'],
    'y': 0,
    'w': window_h - left_frame['w'] - right_frame['w'],
    'h': window_h,
}

#######################################
# ;map+img
#######################################
images_pygame = []

def add_image_pygame(path):
    global images_pygame
    found = False
    for image_pygame in images_pygame:
        if image_pygame['path'] == path:
            found = True
            break
    if not found:
        images_pygame.append({
            'path': path, 
            'img': pygame.image.load(path),
        })

level_map = {
    'row_num': 7,
    'col_num': 7,
    'tiles': []
}
for i in range(level_map['row_num']):
    row = []
    for j in range(level_map['col_num']):
        row.append(None)
    level_map['tiles'].append(row)
        
level_map['tiles'][0][0] = 'assets/characters/succubus.png'
level_map['tiles'][0][1] = 'assets/characters/zombie.png'
level_map['tiles'][0][2] = 'assets/characters/hellhound.png'
level_map['tiles'][1][0] = 'assets/characters/pharoh.png'
level_map['tiles'][1][1] = 'assets/characters/harpy.png'
level_map['tiles'][1][2] = 'assets/characters/slime.png'
add_image_pygame('assets/characters/succubus.png')
add_image_pygame('assets/characters/zombie.png')
add_image_pygame('assets/characters/hellhound.png')
add_image_pygame('assets/characters/pharoh.png')
add_image_pygame('assets/characters/harpy.png')
add_image_pygame('assets/characters/slime.png')


def clear_asset_pack():
    global assets_icons
    assets_icons = copy.deepcopy(assets_icons_clean)
    for i in range(assets_icons['row_num']):
        row = []
        for j in range(assets_icons['col_num']):
            row.append(None)
        assets_icons['icons'].append(row)
        
def load_asset_pack_characters():
    global assets_icons
    clear_asset_pack()
    assets_icons['icons'][0][0] = 'assets/characters/succubus.png'
    assets_icons['icons'][0][1] = 'assets/characters/zombie.png'
    assets_icons['icons'][0][2] = 'assets/characters/hellhound.png'
    assets_icons['icons'][0][3] = 'assets/characters/pharoh.png'
    assets_icons['icons'][0][4] = 'assets/characters/harpy.png'
    assets_icons['icons'][1][0] = 'assets/characters/slime.png'
    add_image_pygame('assets/characters/succubus.png')
    add_image_pygame('assets/characters/zombie.png')
    add_image_pygame('assets/characters/hellhound.png')
    add_image_pygame('assets/characters/pharoh.png')
    add_image_pygame('assets/characters/harpy.png')
    add_image_pygame('assets/characters/slime.png')

def load_asset_pack_textures():
    global assets_icons
    clear_asset_pack()
    assets_icons['icons'][0][0] = 'assets/textures/grass.png'
    add_image_pygame('assets/textures/grass.png')

clear_asset_pack()
# load_asset_pack_characters()
# load_asset_pack_textures()
print(assets_icons)

#######################################################
# ;pygame
#######################################################
pygame.init()

screen = pygame.display.set_mode([window_w, window_h])

# ;jump
def draw_left_frame_tabs():
    font = pygame.font.SysFont('Arial', 16)
    x = frame_assets_tabs['x']
    y = frame_assets_tabs['y']
    w = frame_assets_tabs['w']
    h = frame_assets_tabs['h']
    pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)
    tab_i = -1
    tab_w = 80
    for tab_i in range(2):
        x = frame_assets_tabs['x'] + tab_w*tab_i
        y = frame_assets_tabs['y']
        pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, tab_w, h), 1)
        text_surface = font.render(f'pack {tab_i}', False, (255, 255, 255))
        screen.blit(text_surface, (x + 10, y + 5))

def draw_left_frame_icons():
    # draw icons background
    for row_num in range(assets_icons['row_num']):
        for col_num in range(assets_icons['col_num']):
            # background
            x = frame_assets_icons['x'] + assets_icons['icon_size']*col_num + 1
            y = frame_assets_icons['y'] + assets_icons['icon_size']*row_num + 1
            w = assets_icons['icon_size'] - 1
            h = assets_icons['icon_size'] - 1
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h))
    # draw icons images
    for i in range(assets_icons['row_num']):
        for j in range(assets_icons['col_num']):
            img_path = assets_icons['icons'][i][j]
            if img_path != None:
                img = None
                for obj in images_pygame:
                    if obj['path'] == img_path:
                        img = obj['img']
                        break
                img = pygame.transform.scale(img, (assets_icons['icon_size'], assets_icons['icon_size']))
                x = frame_assets_icons['x'] + assets_icons['icon_size']*j
                y = frame_assets_icons['y'] + assets_icons['icon_size']*i
                screen.blit(img, (x, y))
    # draw icons outline active cell
    for row_num in range(assets_icons['row_num']):
        for col_num in range(assets_icons['col_num']):
            if row_num == assets_icons['row_active'] and col_num == assets_icons['col_active']:
                x = frame_assets_icons['x'] + assets_icons['icon_size']*col_num + 1
                y = frame_assets_icons['y'] + assets_icons['icon_size']*row_num + 1
                w = assets_icons['icon_size'] - 1
                h = assets_icons['icon_size'] - 1
                pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1,)
    # outline frame icons
    x = frame_assets_icons['x']
    y = frame_assets_icons['y']
    w = frame_assets_icons['w']
    h = frame_assets_icons['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h,), 1,)

def draw_left_frame():
    pygame.draw.rect(
        screen, '#202020', 
        pygame.Rect(frame_assets_icons['x'], frame_assets_icons['y'], frame_assets_icons['w'], frame_assets_icons['h'])
    )
    draw_left_frame_tabs()
    draw_left_frame_icons()
    x = left_frame['x']
    y = left_frame['y']
    w = left_frame['w']
    h = left_frame['h']
    pygame.draw.rect(screen, '#ffffff', pygame.Rect(x, y, w, h), 1)

def draw_map_grid():
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera['zoom']
            h = tile_size*camera['zoom']
            x = central_frame['x'] + w*j + camera['x']
            y = central_frame['y'] + h*i + camera['y']
            pygame.draw.rect(screen, '#303030', pygame.Rect(x, y, w, h,), 1,)

    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            img_path = level_map['tiles'][i][j]
            if img_path != None:
                img = None
                for obj in images_pygame:
                    if obj['path'] == img_path:
                        img = obj['img']
                        break
                img = pygame.transform.scale(img, (w, h))
                w = tile_size*camera['zoom']
                h = tile_size*camera['zoom']
                x = central_frame['x'] + w*j + camera['x']
                y = central_frame['y'] + h*i + camera['y']
                screen.blit(img, (x, y))

    font = pygame.font.SysFont('Arial', 24)
    for i in range(level_map['row_num']):
        for j in range(level_map['col_num']):
            w = tile_size*camera['zoom']
            h = tile_size*camera['zoom']
            x = central_frame['x'] + w*j + camera['x']
            y = central_frame['y'] + h*i + camera['y']
            text_surface = font.render(f'{i} - {j}', False, (255, 0, 255))
            screen.blit(text_surface, (x, y))

def draw_main():
    # window bg
    screen.fill('#101010')
    # left frame
    draw_left_frame()
    # central frame
    draw_map_grid()
    ## debug
    pygame.display.flip()

mouse = {
    'x': 0,
    'y': 0,
    'left_click_old': -1,
    'left_click_cur': 0,
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse['x'], mouse['y'] = pygame.mouse.get_pos()
    mouse['left_click_cur'] = pygame.mouse.get_pressed()[0]

    if mouse['left_click_cur'] == True: # left mouse button clicked
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']
            # check if clicked an asset tab
            x1 = left_frame['x']
            y1 = left_frame['y']
            x2 = left_frame['x'] + left_frame['w']
            y2 = left_frame['y'] + left_frame['h']
            if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                print('left frame')
                x1 = frame_assets_tabs['x']
                y1 = frame_assets_tabs['y']
                x2 = frame_assets_tabs['x'] + frame_assets_tabs['w']
                y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
                if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                    print('    frame assets tabs')
                    x1 = frame_assets_tabs['x'] + 80*0
                    y1 = frame_assets_tabs['y']
                    x2 = frame_assets_tabs['x'] + 80*0 + 80
                    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
                    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                        print('        frame assets tab 1')
                        load_asset_pack_characters()
                    x1 = frame_assets_tabs['x'] + 80*1
                    y1 = frame_assets_tabs['y']
                    x2 = frame_assets_tabs['x'] + 80*1 + 80
                    y2 = frame_assets_tabs['y'] + frame_assets_tabs['h']
                    if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                        print('        frame assets tab 2')
                        load_asset_pack_textures()
                print('left frame')
                x1 = frame_assets_icons['x']
                y1 = frame_assets_icons['y']
                x2 = frame_assets_icons['x'] + frame_assets_icons['w']
                y2 = frame_assets_icons['y'] + frame_assets_icons['h']
                if mouse['x'] >= x1 and mouse['y'] >= y1 and mouse['x'] < x2 and mouse['y'] < y2:
                    print('    frame assets icons')
                    col_index = (mouse['x'] - frame_assets_icons['x']) // assets_icons['icon_size']
                    print(col_index)
                    assets_icons['col_active'] = col_index
                    row_index = (mouse['y'] - frame_assets_icons['y']) // assets_icons['icon_size']
                    print(row_index)
                    assets_icons['row_active'] = row_index
    else: # left mouse button released
        if mouse['left_click_old'] != mouse['left_click_cur']:
            mouse['left_click_old'] = mouse['left_click_cur']

    draw_main()

pygame.quit()
