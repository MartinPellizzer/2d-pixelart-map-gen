import utils 

vault = f'/home/ubuntu/vault'

pipe = None
bg_model = None

#############################################################################
# ;ai
#############################################################################
'''
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
'''

def gen_image(row_active, col_active, assets_pack, prompt):
    import torch
    from diffusers import StableDiffusionXLPipeline
    from diffusers import StableDiffusionPipeline
    from diffusers import DPMSolverMultistepScheduler

    from PIL import Image
    from torchvision import transforms
    import matplotlib.pyplot as plt
    from transformers import AutoModelForImageSegmentation

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
    image_index = row_active*5+col_active
    image_index = utils.format_id(image_index)
    image.save(f'assets/{assets_pack}/{image_index}.png')
