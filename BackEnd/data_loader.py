import json
import requests
from io import BytesIO
import clip
import torch
from PIL import Image
import meilisearch
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="your-pinecone-api-key")

if "product-index" not in pc.list_indexes().names():
    pc.create_index(
        name="product-index",
        dimension=512,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2"),
    )

index = pc.Index("product-index")

client = meilisearch.Client("http://127.0.0.1:7700")
meili_index = client.index("products")

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

client = meilisearch.Client("http://127.0.0.1:7700")
meili_index = client.index("products")

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)


def encode_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    image_input = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy().tolist()[0]


def load_data(data_path):
    with open(data_path) as f:
        data = json.load(f)
    return data


def populate_databases(data_path):
    data = load_data(data_path)
    documents = []

    for item in data:
        image_vector = encode_image(item["images"][0])

        index.upsert([(str(item["id"]), image_vector)])


        document = item
        documents.append(document)

    meili_index.add_documents(documents)


if __name__ == "__main__":
    populate_databases("./products.json")
