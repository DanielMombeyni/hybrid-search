import meilisearch
import os

# Initialize MeiliSearch client
client = meilisearch.Client(os.getenv("MEILISEARCH_URL", "http://127.0.0.1:7700"))
index = client.index("products")

def keyword_search(query, top_k=10):
    # Perform the search in MeiliSearch
    search_result = index.search(query, {'limit': top_k})
    return search_result['hits']
