import torch
import clip
from PIL import Image
import requests
from io import BytesIO


device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def encode_query(query):
    """
    Encodes a text query into a vector using CLIP.
    """
    text = clip.tokenize([query]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(text)
    return text_features.cpu().numpy().tolist()[0]

def encode_image(image_url):
    """
    Encodes an image from a URL into a vector using CLIP.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    image_input = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        image_features = model.encode_image(image_input)
    return image_features.cpu().numpy().tolist()[0]
