import asyncio
import random
from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from apscheduler.triggers.interval import IntervalTrigger
from loguru import logger

from common.utils.config_reader import Config
from common.utils.scheduler import scheduler


async def send_messages_task(client: discord.Client):
    job = scheduler.get_job("send_messages_task")

    config = Config()  # type: ignore

    helpers_channel = await client.fetch_channel(config.target_helpers_channel_id)
    agitation_message = await helpers_channel.fetch_message(config.channel_message_id)

    for server_name, channel_ids in config.channels.items():
        logger.info(f"Sending messaging to: {server_name}")
        for channel_id in channel_ids:
            channel = client.get_channel(channel_id)

            if channel is None:
                logger.warning(f"Channel {server_name}(ID: {channel_id}) not found!")
                continue

            try:
                await channel.send(agitation_message.content)
            except (discord.Forbidden, discord.NotFound, discord.HTTPException, ValueError, TypeError) as e:
                logger.warning(f"Failed to send message to {server_name}(ID: {channel_id}): {e}")
            else:
                logger.info(f"Sent message to {server_name}(ID: {channel_id})")

            delay = random.randint(5, 15)
            await asyncio.sleep(delay)

    if job:
        trigger = IntervalTrigger(
            hours=6,
            jitter=3600,
            start_date=datetime.now(ZoneInfo("Europe/Moscow"))
        )
        job.reschedule(trigger=trigger)
