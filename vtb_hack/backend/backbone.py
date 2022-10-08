from typing import Dict, List, Any
import random
from vtb_hack.backend.ch_client import ClickHouse


ch_client = ClickHouse('prod_cluster')


def get_news_records_by_label(label: str, limit: int = 10, sample_size: int = 3) -> List[Dict[str, Any]]:
    q = f"""
        SELECT *
        FROM news.rcc_news
        WHERE label = '{label}'
        ORDER BY date DESC
        LIMIT {limit}
    """
    records = ch_client.select_as_records(q)
    sampled = random.sample(records, k=sample_size)
    return sampled
