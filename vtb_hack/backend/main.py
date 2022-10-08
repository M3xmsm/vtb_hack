from typing import Dict, List, Any
from vtb_hack.backend.ch_client import ClickHouse


ch_client = ClickHouse('prod_cluster')


def get_news_records(label: str, limit: int = 100) -> List[Dict[str, Any]]:
    q = f"""
        SELECT *
        FROM news.rcc_news
        WHERE label = '{label}'
        ORDER BY date DESC
        LIMIT {limit}
    """
    records = ch_client.select_as_records(q)
    return records


if __name__ == "__main__":
    records = get_news_records('Юристы')
    print(records[0])
