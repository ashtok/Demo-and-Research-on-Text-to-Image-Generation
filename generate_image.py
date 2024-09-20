import transformers
from diffusers import DiffusionPipeline
from diffusers.utils import pt_to_pil
import torch

# Ensure you are using the correct version of PyTorch and other dependencies
print("PyTorch version:", torch.__version__)
print("Transformers version:", transformers.__version__)

# List of 25 captions
captions = [
    "A realistic photo of a polar bear wearing a red scarf, ice skating on a frozen lake.",
]

# Stage 1
stage_1 = DiffusionPipeline.from_pretrained("DeepFloyd/IF-I-XL-v1.0", variant="fp16", torch_dtype=torch.float16)
stage_1.enable_xformers_memory_efficient_attention()  # Keep this if torch.__version__ < 2.0.0
stage_1.enable_model_cpu_offload()

# Stage 2
stage_2 = DiffusionPipeline.from_pretrained(
    "DeepFloyd/IF-II-L-v1.0", text_encoder=None, variant="fp16", torch_dtype=torch.float16
)
stage_2.enable_xformers_memory_efficient_attention()  # Keep this if torch.__version__ < 2.0.0
stage_2.enable_model_cpu_offload()

# Stage 3
safety_modules = {"feature_extractor": stage_1.feature_extractor, "safety_checker": stage_1.safety_checker}
stage_3 = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler", **safety_modules, torch_dtype=torch.float16)
stage_3.enable_xformers_memory_efficient_attention()  # Keep this if torch.__version__ < 2.0.0
stage_3.enable_model_cpu_offload()

# Manual seed for reproducibility
generator = torch.manual_seed(0)

# Loop through each caption
for idx, prompt in enumerate(captions):
    print(f"Generating image for prompt {idx+1}: {prompt}")

    # Text embeds
    prompt_embeds, negative_embeds = stage_1.encode_prompt(prompt)

    # Stage 1
    image = stage_1(prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
    pt_to_pil(image)[0].save(f"./caption_{idx+1}_stage_I.png")

    # Stage 2
    image = stage_2(
        image=image, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt"
    ).images
    pt_to_pil(image)[0].save(f"./caption_{idx+1}_stage_II.png")

    # Stage 3
    image = stage_3(prompt=prompt, image=image, generator=generator, noise_level=100).images
    image[0].save(f"./caption_{idx+1}_stage_III.png")

print("Image generation completed for all captions.")
