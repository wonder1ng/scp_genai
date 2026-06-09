from diffusers import FluxPipeline
from dotenv import load_dotenv
import torch, time, os
from diffusers import StableDiffusionPipeline

model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,   
    torch_dtype=torch.float32
)

pipe.to("cuda")

prompt = """
ultra realistic photo of a korean girl,
cinematic lighting,
highly detailed,
8k,
professional photography
"""
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

start = time.time()

image = pipe(
    prompt,
    guidance_scale=0.0,
    num_inference_steps=4,
    height=768,
    width=768,
).images[0]

def full_path(filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), filename)

image.save(full_path("flux_output.png"))

print(f"done : {time.time()-start:.1f} sec")