import base64
from aiogram import Bot, types


async def send_to_telegram(bot_token: str, user_id: str, video_path: str) -> str:
    """
    Send video file to Telegram user.
    
    Args:
        bot_token: Telegram bot token
        user_id: Telegram user ID
        video_path: Path to video file
        
    Returns:
        file_id: Telegram file ID
    """
    async with Bot(token=bot_token) as bot:
        message = await bot.send_video_note(
            user_id, 
            types.FSInputFile(video_path)
        )
        return message.video_note.file_id
