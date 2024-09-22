import transformers
from diffusers import DiffusionPipeline
from diffusers.utils import pt_to_pil
import torch

# Ensure you are using the correct version of PyTorch and other dependencies
print("PyTorch version:", torch.__version__)
print("Transformers version:", transformers.__version__)

# Initialize DeepFloyd IF pipelines (Stage 1, Stage 2, Stage 3)
stage_1 = DiffusionPipeline.from_pretrained("DeepFloyd/IF-I-XL-v1.0", variant="fp16", torch_dtype=torch.float16)
stage_1.enable_xformers_memory_efficient_attention()
stage_1.enable_model_cpu_offload()

stage_2 = DiffusionPipeline.from_pretrained(
    "DeepFloyd/IF-II-L-v1.0", text_encoder=None, variant="fp16", torch_dtype=torch.float16
)
stage_2.enable_xformers_memory_efficient_attention()
stage_2.enable_model_cpu_offload()

safety_modules = {"feature_extractor": stage_1.feature_extractor, "safety_checker": stage_1.safety_checker}
stage_3 = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-x4-upscaler", **safety_modules, torch_dtype=torch.float16)
stage_3.enable_xformers_memory_efficient_attention()
stage_3.enable_model_cpu_offload()

# Manual seed for reproducibility
generator = torch.manual_seed(0)

def generate_real_images(prompt):
    # Encode prompt
    prompt_embeds, negative_embeds = stage_1.encode_prompt(prompt)

    # Stage 1: Generate 64x64 image
    image = stage_1(prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
    base_image = pt_to_pil(image)[0]

    # Stage 2: Generate 256x256 image
    image = stage_2(image=image, prompt_embeds=prompt_embeds, negative_prompt_embeds=negative_embeds, generator=generator, output_type="pt").images
    medium_image = pt_to_pil(image)[0]

    # Stage 3: Generate 1024x1024 image
    large_image = stage_3(prompt=prompt, image=image, generator=generator, noise_level=100).images[0]

    # Save all images to temporary files
    base_image_path = f"./temp_generated_base_image.png"  # 64x64 image (temporary)
    medium_image_path = f"./temp_generated_medium_image.png"  # 256x256 image (temporary)
    large_image_path = f"./temp_generated_large_image.png"  # 1024x1024 image (temporary)

    base_image.save(base_image_path)
    medium_image.save(medium_image_path)
    large_image.save(large_image_path)

    return base_image_path, medium_image_path, large_image_path
