import utils 

vault = f'/home/ubuntu/vault'

pipe = None
bg_model = None

#############################################################################
# ;ai
#############################################################################
def bg_remove(row_active, col_active, assets_pack):
    import torch
    from PIL import Image
    from torchvision import transforms
    import matplotlib.pyplot as plt
    from transformers import AutoModelForImageSegmentation

    global bg_model
    image_index = row_active*5+col_active
    index = utils.format_id(image_index)
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
    asset_filepath = f'assets/{assets_pack}/images/{index}.png'
    image = Image.open(asset_filepath)
    input_images = transform_image(image).unsqueeze(0).to('cuda')
    # Prediction
    with torch.no_grad():
        preds = bg_model(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)
    return image

def bg_remove_new(image):
    import torch
    from PIL import Image
    from torchvision import transforms
    import matplotlib.pyplot as plt
    from transformers import AutoModelForImageSegmentation

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
    input_images = transform_image(image).unsqueeze(0).to('cuda')
    # Prediction
    with torch.no_grad():
        preds = bg_model(input_images)[-1].sigmoid().cpu()
    pred = preds[0].squeeze()
    pred_pil = transforms.ToPILImage()(pred)
    mask = pred_pil.resize(image.size)
    image.putalpha(mask)
    return image

def gen_image(prompt):
    import torch
    from diffusers import StableDiffusionXLPipeline
    from diffusers import StableDiffusionPipeline
    from diffusers import DPMSolverMultistepScheduler

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
        prompt=prompt, 
        cross_attention_kwargs={'scale': 1}, 
        width=1024, 
        height=1024, 
        num_inference_steps=20, 
        guidance_scale=7.0
    ).images[0]
    return image

