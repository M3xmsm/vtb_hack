from vtb_hack.backend.backbone import get_news_records_by_label


if __name__ == "__main__":
    records = get_news_records_by_label('Юристы')
    print(records)
