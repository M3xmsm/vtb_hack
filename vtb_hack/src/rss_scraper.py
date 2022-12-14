import feedparser
from typing import Dict, List, Tuple
from structlog import get_logger
from pydantic import ValidationError

from vtb_hack.src.data_models.schemas import NewsRecord
from vtb_hack.backend.ch_client import ClickHouse

logger = get_logger()

def get_news(url_feed: str) -> Tuple[List[str], ...]:
    feed = feedparser.parse(url_feed)
    headlines = [item_of_news['title'] for item_of_news in feed['items']]
    descriptions = [item_of_news['description'] for item_of_news in feed['items']]
    links = [item_of_news['link'] for item_of_news in feed['items']]
    dates = [item_of_news['published'] for item_of_news in feed['items']]
    return headlines, descriptions, links, dates


def get_rss_news(feed: Dict[str, str]) -> List[Dict[str, str]]:
    records = []
    for key, url in feed.items():
        source, label = key.split('::')
        logger.info("Starting to parce", source=source)
        headlines, descriptions, links, dates = get_news(url)

        for head, desc, link, dt in zip(headlines, descriptions, links, dates):
            try:
                record = {
                    'source': source,
                    'label': label,
                    'headline': head,
                    'description': desc,
                    'link': link,
                    'date': dt
                }
                NewsRecord.parse_obj(record)
                records.append(record)
            except ValidationError:
                logger.error('Validation error')
            except Exception as e:
                logger.critical('Unknown error', ex=str(e))
    return records


if __name__ == "__main__":
    my_feed = {
        'Коммерсант::Экономика': 'https://www.kommersant.ru/RSS/section-economics.xml',
        'Главная книга::Бухгалтерия': 'http://glavkniga.ru/rss/yandexnews',
        'Главбух::Бухгалтерия': 'http://www.glavbukh.ru/rss/news.xml',
        'Консультант бухгалтерам::Бухгалтерия': 'https://www.consultant.ru/rss/db.xml',
        'Консультант юристам::Юристы': 'https://www.consultant.ru/rss/nw.xml',
        'Консультант горячие новости::Бухгалтерия': 'https://www.consultant.ru/rss/fd.xml',
        'Консультант Москва::Бухгалтерия': 'https://www.consultant.ru/rss/md.xml',
        'Консультант МО::Бухгалтерия': 'https://www.consultant.ru/rss/ow.xml',
        'BFM: Макроэкономика::Экономика': 'https://www.bfm.ru/news.rss?rubric=19',
        'BFM: Финансы::Экономика': 'https://www.bfm.ru/news.rss?rubric=28',
        'BFM: ИТ::Экономика': 'https://www.bfm.ru/news.rss?tag=1399',
        'BFM: Право::Юристы': 'https://www.bfm.ru/news.rss?rubric=4889',
        'Клерк::Бухгалтерия': 'https://www.klerk.ru/export/news.rss',
        'ЦБ: новости::Юристы': 'http://www.cbr.ru/rss/eventrss',
        'ЦБ: пресс-релизы::Юристы': 'http://www.cbr.ru/rss/RssPress',
        'Минфин::Экономика': 'https://minfin.gov.ru/rss_news',
        'Минпромторг/Минэк: Документы::Экономика': 'http://government.ru/docs/rss/',
        'Бух.ру::Бухгалтерия': 'https://buh.ru/rss/?chanel=news',
        'Гарант::Бухгалтерия': 'http://www.garant.ru/rss/',
        'Минтруд::Бухгалтерия': 'https://mintrud.gov.ru/news/rss/official',
        'Право.ру::Юристы': 'https://pravo.ru/rss/',
    }

    records = get_rss_news(my_feed)
    ch_client = ClickHouse('prod_cluster')
    ch_client.insert('news.rcc_news', records)
