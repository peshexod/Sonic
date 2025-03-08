import asyncio
import base64
import os
import shutil
import tempfile
from argparse import Namespace
from pydub import AudioSegment
import json
from aiogram import Bot, types

async def generator_handler(job):
    try:
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
        #run_pipline(args)
        async with Bot(token=args.bot_token) as bot:
            message = await bot.send_video_note(args.user_id, types.FSInputFile(args.output_path))
            file_id = message.video_note.file_id
        # Clean up temporary files
        try:
            shutil.rmtree(args.temp_dir, ignore_errors=True)
            #print(f"Cleaned up temporary directory: {args.temp_dir}")
        except Exception as cleanup_error:
            print(f"Error cleaning up temporary files: {str(cleanup_error)}")
        return {
            "output": {
                "output_file_id": file_id,
            }
        }
    except Exception as e:
        return {
            "output": {
                "error": str(e)
            }
        }
            
if __name__ == "__main__":
    # Load job data from local test file
    with open("test_job.txt", "r") as file:
        job = json.load(file)
        #print(f"Loaded test job: {job}")
    asyncio.run(generator_handler(job))