import discord
from loguru import logger

from scheduler_setup import init_scheduler

class DiscordClient(discord.Client):
    async def on_ready(self):
        await init_scheduler(self)
        logger.info(f'Logged on as {self.user}')


d_client = DiscordClient()