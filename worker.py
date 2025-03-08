import asyncio
import runpod
from sonic import Sonic
import base64
import os
import tempfile
from argparse import Namespace
from pydub import AudioSegment
from aiogram import Bot, types
import shutil

pipe = Sonic(0)

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
    # Create output path
    output_path = os.path.join(temp_dir, "output.mp4")

    # Create args namespace for compatibility with existing code
    args = Namespace(
        image_path=image_path,
        audio_path=audio_path,
        output_path=output_path,
        bot_token=job_input.get("bot_token", None),
        user_id=job_input.get("user_id", None),
        crop=job_input.get("crop", False),
        dynamic_scale=job_input.get("dynamic_scale", 1.0),
        temp_dir=temp_dir
    )
    if args.bot_token is None or args.user_id is None:
            return {
                "output": {
                    "error": "Bot token or user ID not provided"
                }
            }
    run_pipline(args)
    
def run_pipline(args):
    try:
        face_info = pipe.preprocess(args.image_path, expand_ratio=0.5)
        print(face_info)
        if face_info['face_num'] >= 0:
            if args.crop:
                crop_image_path = args.image_path + '.crop.png'
                pipe.crop_image(args.image_path, crop_image_path, face_info['crop_bbox'])
                args.image_path = crop_image_path
            os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
            pipe.process(args.image_path, args.audio_path, args.output_path, min_resolution=512, inference_steps=25, dynamic_scale=args.dynamic_scale)
            bot = Bot(token=args.bot_token)
            if args.user_id:
                message: types.Message = asyncio.run(bot.send_video_note(args.user_id, types.InputFile(args.output_path)))
                file_id = message.video_note.file_id
            # Clean up temporary files
            try:
                shutil.rmtree(args.temp_dir, ignore_errors=True)
                print(f"Cleaned up temporary directory: {args.temp_dir}")
            except Exception as cleanup_error:
                print(f"Error cleaning up temporary files: {str(cleanup_error)}")
            return {
                "output": {
                    "output_file_id": file_id,
                }
            }
        return {
            "output": {
                "error": "No face detected"
            }
        }
    except Exception as e:
        bot = Bot(token=args.bot_token)
        asyncio.run(bot.send_message(args.user_id, str(e)))

runpod.serverless.start(
    {
        "handler": generator_handler,  # Required
        #"return_aggregate_stream": True,  # Optional, results available via /run
    }
)