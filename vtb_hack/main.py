from typing import List, Dict, Any
from telethon.sync import TelegramClient
from structlog import get_logger
import datetime


logger = get_logger()


async def get_messages(
    tg_client: TelegramClient,
    tg_channel: str,
    batch_size: int,
    from_date: datetime.datetime
) -> List[Dict[str, Any]]:
    offset_id = 0
    all_messages = []
    async with tg_client:
        channel = await tg_client.get_entity(tg_channel)
        while True:
            messages_iterator = tg_client.iter_messages(channel, offset_date=from_date, offset_id=offset_id,
                                                        limit=batch_size, reverse=True)
            messages = [m.to_dict() async for m in messages_iterator]
            if not messages:
                break
            logger.info(
                f"Parsed messages",
                tg_chanel=tg_channel,
                from_msg_id=messages[0]['id'],
                to_msg_id=messages[-1]['id'],
                count=len(messages)
            )
            offset_id = messages[-1]['id']
            all_messages += messages
    return all_messages


if __name__ == "__main__":
    api_id = 1
    api_hash = '1'
    session_name = 'parse_jobs'

    tg_client = TelegramClient(session_name, api_id, api_hash)
    tg_client.start()

    messages = await get_messages(
        tg_client,
        'https://t.me/hh_vacancy_development',
        100,
        datetime.datetime(2022, 9, 1, tzinfo=datetime.timezone.utc)
    )

    print(messages[0])
