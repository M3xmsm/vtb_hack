from typing import Dict, List, Any
from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware

from vtb_hack.backend.backbone import get_news_records_by_label


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/news/get/{label}")
async def get_news_by_label(
    label: str = Path(..., regex="^[а-яА-Я]+$")
) -> Dict[str, Any]:
    news_records = get_news_records_by_label(label)
    return news_records
