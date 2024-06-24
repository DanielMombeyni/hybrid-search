from fastapi import FastAPI, Query
from pydantic import BaseModel
from search import search_products

app = FastAPI()


class SearchQuery(BaseModel):
    query: str
    top_k: int = 10


@app.post("/search")
async def search(query: SearchQuery):
    results = await search_products(query.query, query.top_k)
    return results
