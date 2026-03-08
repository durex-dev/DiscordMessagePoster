from pathlib import Path
from typing import Dict, List, Union
import sys
from environs import Env
from pydantic.v1 import BaseSettings, validator

def get_base_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

base_path = get_base_path()
env_paths = [
    base_path / '.env',
    Path.cwd() / '.env',
    Path(__file__).parent.parent / '.env',
]

env = Env()
env_file_loaded = False

for env_path in env_paths:
    if env_path.exists():
        env.read_env(str(env_path))
        print(f"Loaded .env from: {env_path}")
        env_file_loaded = True
        break

if not env_file_loaded:
    print(f"Warning: .env file not found in any of: {[str(p) for p in env_paths]}")
    env.read_env()

class Config(BaseSettings):
    client_token: str
    channels: Dict[str, List[int]]
    target_helpers_channel_id: int
    channel_message_id: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
        case_sensitive = False

    @validator("channels", pre=True)
    def parse_channels(cls, v: Union[str, Dict]) -> Union[Dict[str, List[int]], List[int]]:
        """
            Преобразует строку 'id1,id2' в список [id1, id2]
        """
        if isinstance(v, str):
            # Если это строка - возвращаем список
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        elif isinstance(v, dict):
            # для вложенных серверов
            result = {}
            for k, lst in v.items():
                if isinstance(lst, str):
                    result[k] = [int(i.strip()) for i in lst.split(",") if i.strip()]
                else:
                    result[k] = lst
            return result
        return v