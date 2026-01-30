from diffusers import AutoPipelineForImage2Image
import torch
from diffusers.utils import load_image
import os

# Load the model
pipeline = AutoPipelineForImage2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True
)
pipeline.enable_model_cpu_offload()
pipeline.enable_xformers_memory_efficient_attention()

# Define the input images and prompts
media = [
    {
        "input_image": "input/book_cover.png",
        "prompt": "A realistic book cover with castle and night sky. The design features a small princess with her back to the viewer, looking towards a castle under a starry sky. The focus is solely on the book cover itself, with no surrounding background.",
        "output_image": "output/book_cover.png"
    },
    {
        "input_image": "input/dvd_cover.png",
        "prompt": "A DVD cover for fairies. The design should be focused solely on the DVD cover with no background",
        "output_image": "output/dvd_cover.png"
    },
    {
        "input_image": "input/album_cover.png",
        "prompt": "An album cover that features a guitar amidst clouds, with a sky blue color scheme. The image should be focused solely on the album cover with no background",
        "output_image": "output/album_cover.png"
    }
]

# Ensure the output directory exists
os.makedirs("output", exist_ok=True)

# Generate images
for item in media:
    print(f"Processing: {item['input_image']}")
    init_image = load_image(item["input_image"])
    generated_image = pipeline(
        item["prompt"],
        image=init_image,
        strength=0.8,  # Adjust strength for creativity
        guidance_scale=7.5  # Adjust guidance scale for prompt adherence
    ).images[0]
    generated_image.save(item["output_image"])
    print(f"Saved: {item['output_image']}")