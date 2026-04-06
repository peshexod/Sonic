from typing import Optional
from pydantic import BaseModel, Field


class AudioInput(BaseModel):
    base64: str
    filename: str = "input.wav"


class ImageInput(BaseModel):
    base64: str
    filename: str = "input.jpg"


class TelegramConfig(BaseModel):
    bot_token: str
    user_id: str


class VKConfig(BaseModel):
    group_token: str
    user_id: str


class StorageConfig(BaseModel):
    endpoint: str
    bucket: str
    access_key: str
    secret_key: str


class SonicRequest(BaseModel):
    audio_input: AudioInput
    image_input: ImageInput
    crop: bool = False
    dynamic_scale: float = 1.0
    inference_steps: int = Field(default=20, ge=10, le=50)
    telegram: Optional[TelegramConfig] = None
    vk: Optional[VKConfig] = None
    storage: Optional[StorageConfig] = None


class SonicResponse(BaseModel):
    telegram_file_id: Optional[str] = None
    vk_message_id: Optional[str] = None
    storage_url: Optional[str] = None
    base64: Optional[str] = None
    error: Optional[str] = None
