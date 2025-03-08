FROM python:3.11

WORKDIR /app
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libglib2.0-0 libgl1-mesa-dev -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN if [ ! -d checkpoints ]; then \
    huggingface-cli download LeonJoe13/Sonic --local-dir checkpoints; \
    huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt --local-dir checkpoints/stable-video-diffusion-img2vid-xt; \
    huggingface-cli download openai/whisper-tiny --local-dir checkpoints/whisper-tiny; \
    fi

CMD ["python", "worker.py"]