from clickhouse_driver import Client
from pathlib import Path
from typing import List, Dict, Any
import vtb_hack

package_dir = Path(vtb_hack.__file__).parent.parent.absolute()


CLUSTERS: dict = {
    'prod_cluster': {
        'host': 'rc1a-b425jm4ulkoxruwo.mdb.yandexcloud.net',
        'port': 9440,
        'user': 'admin',
        'password': 'q1w2e3r4',
        'ca_certs': package_dir / 'YandexCA.pem',
        'secure': True
    }
}


class ClickHouse:
    def __init__(self, cluster_name: str):
        self.db_client = Client(
            host=CLUSTERS[cluster_name]['host'],
            user=CLUSTERS[cluster_name]['user'],
            password=CLUSTERS[cluster_name]['password'],
            port=CLUSTERS[cluster_name]['port'],
            ca_certs=CLUSTERS[cluster_name].get('ca_certs', None),
            secure=CLUSTERS[cluster_name].get('secure', False),
            settings={
                'max_execution_time': 180,
                'max_memory_usage': 16_000_000_000,
            }
        )

    def select_as_records(self, query: str) -> List[Dict[str, Any]]:
        data, column_types = self.db_client.execute(
            query, with_column_types=True
        )
        column_names = [column[0] for column in column_types]
        data_prepared = [
            {k: v for k, v in zip(column_names, record)}
            for record in data
        ]
        return data_prepared

    def execute(self, query: str, **kwargs):
        data = self.db_client.execute(query, **kwargs)
        return data
