import logging
import io
import requests
from PIL import Image

# This activity function extracts metadata from an image.
def main(input_data: dict) -> dict:
    logging.info(f"ExtractImageMetadata activity function started. Input: {input_data}")

    blob_uri = input_data.get("blob_uri")
    file_name = input_data.get("file_name")

    if not blob_uri:
        raise ValueError("Blob URI not provided for metadata extraction.")

    try:
        # Download the image from the blob URI
        response = requests.get(blob_uri)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Use Pillow to open the image from bytes
        image_bytes = io.BytesIO(response.content)
        img = Image.open(image_bytes)

        # Extract metadata
        file_size_kb = len(response.content) / 1024
        width, height = img.size
        image_format = img.format

        metadata = {
            "FileName": file_name,
            "FileSizeKB": round(file_size_kb, 2),
            "Width": width,
            "Height": height,
            "ImageFormat": image_format
        }
        logging.info(f"Successfully extracted metadata for {file_name}: {metadata}")
        return metadata

    except requests.exceptions.RequestException as e:
        logging.error(f"Error downloading image from {blob_uri}: {e}")
        raise
    except Image.UnidentifiedImageError:
        logging.error(f"Cannot identify image file from {blob_uri}. It might be corrupted or an unsupported format.")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during metadata extraction for {file_name}: {e}")
        raise

