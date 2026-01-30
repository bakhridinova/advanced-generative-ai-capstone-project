# Use the official PyTorch image with CUDA support
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install torch==2.0.1 torchvision==0.15.2 --index-url https://download.pytorch.org/whl/cu117
RUN pip install diffusers==0.20.2 huggingface_hub==0.16.4 accelerate==0.23.0 transformers==4.33.3 safetensors

# Copy the project files into the container
COPY . /app

# Set the default command to run the script
CMD ["python", "generate.py"]