import feedparser
from typing import Dict, List, Any
import pandas as pd
from structlog import get_logger

logger = get_logger()


my_feed = {
    'Коммерсант::Экономика': 'https://www.kommersant.ru/RSS/section-economics.xml',
    'Главная книга::Бухгалтерия': 'http://glavkniga.ru/rss/yandexnews',
    'Главбух::Бухгалтерия': 'http://www.glavbukh.ru/rss/news.xml',
    'Консультант бухгалтерам::Бухгалтерия': 'https://www.consultant.ru/rss/db.xml',
    'Консультант юристам::Юристы': 'https://www.consultant.ru/rss/nw.xml',
    'Консультант горячие новости::Бухгалтерия': 'https://www.consultant.ru/rss/fd.xml',
    'Консультант Москва::Бухгалтерия': 'https://www.consultant.ru/rss/md.xml',
    'Консультант МО::Бухгалтерия': 'https://www.consultant.ru/rss/ow.xml',
    'РБК::Экономика': 'https://rssexport.rbc.ru/rbcnews/news/30/full.rss',
    'BFM: breaking news::Экономика': 'https://www.bfm.ru/news.rss?container_breaking=8',
    'BFM: Макроэкономика::Экономика': 'https://www.bfm.ru/news.rss?rubric=19',
    'BFM: Финансы::Экономика': 'https://www.bfm.ru/news.rss?rubric=28',
    'BFM: ИТ::Экономика': 'https://www.bfm.ru/news.rss?tag=1399',
    'BFM: Право::Юристы': 'https://www.bfm.ru/news.rss?rubric=4889',
    'Клерк::Бухгалтерия': 'https://www.klerk.ru/export/news.rss',
    'Финам: новости компаний::Экономика': 'https://www.finam.ru/analysis/conews/rsspoint/',
    'Финам: новости мировых рынков::Экономика': 'https://www.finam.ru/international/advanced/rsspoint/',
    'Финам: новости и комментарии::Экономика': 'https://www.finam.ru/analysis/nslent/rsspoint/',
    'Банки.ру::Экономика': 'http://www.banki.ru/xml/news.rss',
    'ЦБ: новости::Юристы': 'http://www.cbr.ru/rss/eventrss',
    'ЦБ: пресс-релизы::Юристы': 'http://www.cbr.ru/rss/RssPress',
    'Минфин::Экономика': 'https://minfin.gov.ru/rss_news',
    'Минпромторг/Минэк: Документы::Экономика': 'http://government.ru/docs/rss/',
    'Бух.ру::Бухгалтерия': 'https://buh.ru/rss/?chanel=news',
    'Гарант::Бухгалтерия': 'http://www.garant.ru/rss/',
    'Минтруд::Бухгалтерия':  'https://mintrud.gov.ru/news/rss/official',
    'Право.ру::Юристы': 'https://pravo.ru/rss/',
    'Правительство::Бухгалтерия': 'http://government.ru/all/rss/',
}


def check_url(url_feed: str):
    return feedparser.parse(url_feed)


def get_headlines(url_feed: str) -> List[str]:
    lenta = check_url(url_feed)
    headlines = [item_of_news['title'] for item_of_news in lenta['items']]
    return headlines


def get_descriptions(url_feed: str) -> List[str]:
    lenta = check_url(url_feed)
    descriptions = [item_of_news['description'] for item_of_news in lenta['items']]
    return descriptions


def get_links(url_feed: str) -> List[str]:
    lenta = check_url(url_feed)
    links = [item_of_news['link'] for item_of_news in lenta['items']]
    return links


def get_dates(url_feed: str) -> List[str]:
    lenta = check_url(url_feed)
    dates = [item_of_news['published'] for item_of_news in lenta['items']]
    return dates


def get_rss_news(feed: Dict[str, str]) -> List[Dict[str, str]]:
    records = []
    for key, url in feed.items():
        source, label = key.split('::')
        logger.info("Starting to parce", source=source)
        all_headlines = get_headlines(url)
        all_descriptions = get_descriptions(url)
        all_links = get_links(url)
        all_dates = get_dates(url)

        for head, desc, link, dt in zip(all_headlines, all_descriptions, all_links, all_dates):
            record = {
                'source': source,
                'label': label,
                'headline': head,
                'description': desc,
                'link': link,
                'date': dt
            }
            records.append(record)
    return records

