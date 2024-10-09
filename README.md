# Text-to-Image Generation Using Parti, Imagen, and DeepFloyd IF

## 1. Introduction
This project explores the field of **text-to-image generation**, where images are generated from natural language descriptions using advanced AI models. This capability has various applications in art, design, advertising, and accessibility.

In this project, we experiment with three state-of-the-art text-to-image models:
- **Parti** (Pathways Autoregressive Text-to-Image Model)
- **Imagen** (Google’s Text-to-Image Diffusion Model)
- **DeepFloyd IF** 

We focus on creating a working demo with **DeepFloyd IF** for text-to-image generation and display the results on a web interface.

## 2. Project Goals
- Explore and compare the capabilities of **Parti**, **Imagen**, and **DeepFloyd IF** for text-to-image generation.
- Implement a **web interface** for generating images from user-provided text prompts.
- Analyze the models in terms of image quality, usability, and resource efficiency.

## 3. Models Explored

### 1. Parti (Pathways Autoregressive Text-to-Image Model)
- **Methodology:** Autoregressive, using a Vision Transformer (ViT) and VQGAN tokenizer to generate images token by token.
- **Challenges:** Pretrained weights were unavailable, making it difficult to produce meaningful results. The integration process was complex, and documentation was incomplete.

### 2. Imagen (Google’s Text-to-Image Diffusion Model)
- **Methodology:** Diffusion-based, combining photorealism with deep language understanding.
- **Challenges:** We faced issues with missing pretrained models and noisy outputs. Additionally, poor community support made it difficult to implement successfully.

### 3. DeepFloyd IF
- **Methodology:** Open-source, diffusion-based model with a modular, progressive upscaling process.
- **Strengths:** Provided pretrained weights, detailed documentation, and a well-structured architecture for generating images at resolutions of 64x64, 256x256, and 1024x1024 pixels. DeepFloyd IF was successfully implemented in our project.

## 4. Approach and Challenges

### 4.1 Parti Model
- **Challenges:**
  - Lack of pretrained weights hindered progress.
  - Complex workflow with Vision Transformer integration and VQGAN tokenizer.
  - Incomplete and unclear documentation.

### 4.2 Imagen Model
- **Challenges:**
  - Missing pretrained models.
  - Noisy outputs.
  - Poor community support and incomplete documentation.

### 4.3 DeepFloyd IF Model
- **Solution:**
  - Pretrained weights available for immediate use.
  - Integrated easily with **Hugging Face Diffusers**.
  - Modular architecture enables cascading image generation from 64x64 to 1024x1024 pixels, providing high-quality images.

## 5. Web Implementation
We developed a **web interface** to demonstrate the functionality of **DeepFloyd IF**:
- **Frontend:** Built with HTML, CSS, and JavaScript for a smooth user experience.
- **Backend:** Accepts user-generated text prompts, processes them through the DeepFloyd IF model, and returns images.
- **Deployment:** The entire image generation process completes within two minutes.

## 6. Installation and Setup

1. **Clone the repository.**
2. **Login to Hugging Face**:
   - Ensure you have a Hugging Face account and are logged in.
   - Accept the license on the [DeepFloyd/IF-I-XL-v1.0 model card](https://huggingface.co/DeepFloyd/IF-I-XL-v1.0).

3. **Login Locally**:
   - Install Hugging Face Hub: `pip install huggingface_hub --upgrade`
   - Run the following in a Python shell:

     ```python
     from huggingface_hub import login
     login()
     ```
   - Enter your Hugging Face Hub access token.

4. **Install Dependencies**:
   - Install Diffusers and related packages:  
     `pip install diffusers accelerate transformers safetensors`

5. **Now we can run the Model Locally**.


## 7. Running the Web Interface

1. Ensure that the **DeepFloyd IF model** is installed and configured.
2. Activate the environment in terminal as repo location.
3. ```
   source deepfloyd_env/bin/activate
   ```
4. Start the server.
5. ```uvicorn app:app --reload```
6. Open a new terminal and start the ngrok service. **Do not close this terminal**.
7. ```ngrok http 8000```
8. Copy the ngrok forwarding URL.
9. Replace the URL in the following variable in the index.html file:
10. ```const ngrokUrl = 'https://cd93-132-187-245-44.ngrok-free.app/';```
11. Open your index.html file in a web browser. Enter a text prompt, and the generated images will be displayed within approximately 2 minutes.
12. If the image does not appear on the first attempt, click on the image link (shown below the promt box) to allow access to the image via ngrok in your browser.
13. **Note:** The generation time may exceed 2 minutes depending on GPU resource availability. It typically takes less than 2 minutes on a NVIDIA GPU with 16 GB of VRAM.

## 8. Conclusion

This project explored text-to-image generation using three advanced models: **Parti**, **Imagen**, and **DeepFloyd IF**. While Parti and Imagen had implementation challenges, DeepFloyd IF proved to be a robust solution, providing high-quality images and an easy-to-use web interface.

## 9. Future Work

- Explore more text-to-image models and optimize the image generation process for faster execution.
- Further improve memory efficiency and speed of the **DeepFloyd IF** model.

## 10. References

- [DeepFloyd IF Repository](https://github.com/deep-floyd/IF)
- [Parti](https://github.com/lucidrains/parti-pytorch)
- [Imagen](https://github.com/lucidrains/imagen-pytorch)
- [MinImagen Repository](https://github.com/AssemblyAI-Community/MinImagen)
- Parti Paper: [Scaling Autoregressive Models for Content-Rich Text-to-Image Generation](https://doi.org/10.48550/arXiv.2206.10789)
- Imagen Paper: [Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding](https://doi.org/10.48550/arXiv.2205.11487)
