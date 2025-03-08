FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN if [ ! -d checkpoints ]; then \
    huggingface-cli download LeonJoe13/Sonic --local-dir checkpoints; \
    huggingface-cli download stabilityai/stable-video-diffusion-img2vid-xt --local-dir checkpoints/stable-video-diffusion-img2vid-xt; \
    huggingface-cli download openai/whisper-tiny --local-dir checkpoints/whisper-tiny; \
    fi

CMD ["python", "worker.py"]