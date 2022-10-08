CREATE TABLE news.rcc_news
(
    source String
    , label String
    , headline String
    , description String
    , link String
    , date DateTime('UTC')
)
ENGINE = ReplacingMergeTree
ORDER BY (label, source, link, headline, date, cityHash64(link))
PARTITION BY label
SAMPLE BY cityHash64(link)

