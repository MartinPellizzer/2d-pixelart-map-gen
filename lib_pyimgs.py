def pyimg_load(pygame, pyimgs, asset_json):
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

def pyimg_by_filepath(pyimgs, image_filepath):
    pyimg = {} 
    for pyimg_cur in pyimgs:
        if pyimg_cur['image_filepath'] == image_filepath:
            pyimg = pyimg_cur
            break
    return pyimg

