from pydantic import BaseModel


class NewsRecord(BaseModel):
    source: str
    label: str
    headline: str
    description: str
    link: str
    date: int
