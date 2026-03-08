from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger

from common.tasks.send_messages_task import send_messages_task
from common.utils.scheduler import scheduler


async def init_scheduler(client):
    scheduler.add_job(
        send_messages_task,
        "interval",
        id="send_messages_task",
        hours=6,
        jitter=3600, # случайная задержка в 1 час, дабы не палиться, что это бот
        max_instances=1, # Всего 1 инстанс, дабы не было параллельных запусков
        next_run_time=datetime.now(ZoneInfo("Europe/Moscow")), # Первое сообщение шлем сразу при запуске скрипта.
        coalesce=True,
        args=[client]
    )

    logger.info("Init scheduler successfully")
    scheduler.start()
