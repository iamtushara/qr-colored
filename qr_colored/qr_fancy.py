"""fancy qr code generation"""

import warnings

import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline  # pyright: ignore

from qr_colored.tools import check_torch_version
from qr_colored.qr_simple import generate_qrcode


warnings.filterwarnings('ignore')
check_torch_version()


controlnet = ControlNetModel.from_pretrained(
    'DionTimmer/controlnet_qrcode-control_v1p_sd15',
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    'runwayml/stable-diffusion-v1-5',
    controlnet=controlnet,
    # torch_dtype=torch.float16,
    safety_checker=None,
).to('cuda')
pipe.enable_xformers_memory_efficient_attention()

qr_image = generate_qrcode("Tushar Anand is a Data Scientist!")
qr_image.save("qr-code-image-generated.png")  # pyright: ignore
