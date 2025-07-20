import azure.functions as func
from PIL import Image
import requests
from io import BytesIO
import os

def main(input: dict) -> dict:
    response = requests.get(input["blob_url"])
    img = Image.open(BytesIO(response.content))
    
    metadata = {
        "file_name": os.path.basename(input["blob_url"]),
        "file_size_kb": len(response.content) / 1024,
        "width": img.width,
        "height": img.height,
        "format": img.format
    }
    return metadata
