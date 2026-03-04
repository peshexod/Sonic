from .telegram_sender import send_to_telegram
from .vk_sender import upload_video_to_vk
from .storage_sender import upload_to_storage

__all__ = [
    'send_to_telegram',
    'upload_video_to_vk',
    'upload_to_storage',
]
