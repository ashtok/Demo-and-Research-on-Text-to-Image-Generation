import os
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.cors import CORSMiddleware
from generate_image import generate_real_images  # Import the image generation function

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, adjust this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS)
    allow_headers=["*"],  # Allow all headers
)

# Directory to store generated images
IMAGE_DIR = "generated_images"
FINAL_IMAGE_DIR = "final_generated_images"
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(FINAL_IMAGE_DIR, exist_ok=True)


class ImageRequest(BaseModel):
    prompt: str


# Generate images using DeepFloyd IF model
def generate_images(prompt):
    # Generate the images using the generate_real_images function
    base_image, medium_image, large_image = generate_real_images(prompt)

    # Save the 64x64 and 256x256 images in "generated_images"
    base_image_path = os.path.join(IMAGE_DIR, f"{uuid.uuid4()}_64x64.png")
    medium_image_path = os.path.join(IMAGE_DIR, f"{uuid.uuid4()}_256x256.png")

    # Save the 1024x1024 image in "final_generated_images"
    large_image_path = os.path.join(FINAL_IMAGE_DIR, f"{uuid.uuid4()}_1024x1024.png")

    # Move or copy the generated files to the appropriate directories
    os.rename(base_image, base_image_path)
    os.rename(medium_image, medium_image_path)
    os.rename(large_image, large_image_path)

    return base_image_path, medium_image_path, large_image_path


@app.post("/generate_image")
async def generate_image(request: ImageRequest):
    try:
        # Generate images based on the prompt
        base_image, medium_image, large_image = generate_images(request.prompt)

        return JSONResponse({
            "base_image": os.path.basename(base_image),
            "medium_image": os.path.basename(medium_image),
            "large_image": os.path.basename(large_image)
        })
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.get("/{image_path}")
async def get_image(image_path: str):
    image_file = os.path.join(IMAGE_DIR, image_path)

    # If the image isn't found in IMAGE_DIR, check FINAL_IMAGE_DIR
    if not os.path.exists(image_file):
        image_file = os.path.join(FINAL_IMAGE_DIR, image_path)

    if os.path.exists(image_file):
        return FileResponse(image_file)
    return JSONResponse(content={"error": "File not found"}, status_code=404)
