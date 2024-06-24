from clip_model import encode_query
from keyword_search import keyword_search
import pinecone
import os

# Initialize Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))
index = pinecone.Index("product-index")


async def search_products(query, top_k=10):
    # Encode the query using CLIP
    query_vector = encode_query(query)

    # Perform semantic search
    semantic_results = index.query(query_vector, top_k=top_k)

    # Perform keyword search
    keyword_results = keyword_search(query, top_k=top_k)

    # Combine results
    combined_results = combine_results(semantic_results, keyword_results, top_k)

    return combined_results


def combine_results(semantic_results, keyword_results, top_k):
    # Combine and deduplicate results
    combined = {str(res["id"]): res for res in semantic_results["matches"]}
    combined.update({str(res["id"]): res for res in keyword_results})

    # Sort by score (if semantic results have a score, otherwise just merge)
    if "score" in semantic_results["matches"][0]:
        sorted_results = sorted(
            combined.values(), key=lambda x: x.get("score", 0), reverse=True
        )
    else:
        sorted_results = list(combined.values())

    return sorted_results[:top_k]
