import azure.functions as func
from PIL import Image
import requests
from io import BytesIO
import os
import traceback

def main(input: dict) -> dict:
    try:
        response = requests.get(input["blob_url"])
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        metadata = {
            "file_name": os.path.basename(input["blob_url"]),
            "file_size_kb": round(len(response.content) / 1024, 2),
            "width": img.width,
            "height": img.height,
            "format": img.format
        }
        return metadata

    except Exception as e:
        return {
            "error": True,
            "message": str(e),
            "trace": traceback.format_exc()
        }
