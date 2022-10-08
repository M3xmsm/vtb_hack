from typing import Dict, List, Any
from vtb_hack.backend.ch_client import ClickHouse


ch_client = ClickHouse('prod_cluster')


def get_news_records_by_label(label: str, limit: int = 100) -> List[Dict[str, Any]]:
    q = f"""
        SELECT *
        FROM news.rcc_news
        WHERE label = '{label}'
        ORDER BY date DESC
        LIMIT {limit}
    """
    records = ch_client.select_as_records(q)
    return records
