import base64
import os
import tempfile
from argparse import Namespace
from pydub import AudioSegment
import json

def generator_handler(job):
    # Parse input data
    job_input = job["input"]
    audio_input = job_input.get("audio_input", {})
    image_input = job_input.get("image_input", {})

    # Create temp directory for files
    temp_dir = tempfile.mkdtemp()

    # Save base64 image to file
    image_data = image_input.get("base64", "")
    image_filename = image_input.get("filename", "input.jpg")
    image_path = os.path.join(temp_dir, image_filename)
    with open(image_path, "wb") as f:
        f.write(base64.b64decode(image_data))
    print(image_path)
    # Save base64 audio to file
    audio_data = audio_input.get("base64", "")
    audio_filename = audio_input.get("filename", "input.wav")
    audio_path = os.path.join(temp_dir, audio_filename)
    with open(audio_path, "wb") as f:
        f.write(base64.b64decode(audio_data))
    
    # Convert audio from mp3 to wav if needed
    if audio_filename.lower().endswith('.mp3'):
        try:
            mp3_path = audio_path
            audio_path = os.path.join(temp_dir, os.path.splitext(audio_filename)[0] + '.wav')
            AudioSegment.from_mp3(mp3_path).export(audio_path, format="wav")
            print(f"Converted MP3 to WAV: {audio_path}")
        except ImportError:
            print("Warning: pydub not installed. MP3 to WAV conversion failed.")
        except Exception as e:
            print(f"Error converting MP3 to WAV: {str(e)}")
            
if __name__ == "__main__":
    # Load job data from local test file
    with open("test_job.txt", "r") as file:
        job = json.load(file)
        print(f"Loaded test job: {job}")
    generator_handler(job)