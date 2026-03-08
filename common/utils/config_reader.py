from pathlib import Path
from typing import Dict, List

from environs import Env
from pydantic.v1 import BaseSettings, validator

BASE_DIR = Path(__file__).parent

env = Env()
env.read_env(f'{BASE_DIR}/.env')

class Config(BaseSettings):
    client_token: str
    channels: Dict[str, List[int]]
    target_helpers_channel_id: int
    channel_message_id: int

    class Config:
        env_file = '../../.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

    @validator("channels", pre=True)
    def parse_channels(cls, v):
        """
            Преобразует строку 'id1,id2' в список [id1, id2]
        """
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        elif isinstance(v, dict):
            # для вложенных серверов
            return {k: [int(i.strip()) for i in lst.split(",")] for k, lst in v.items()}
        return v
