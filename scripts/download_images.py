import os
import requests
from PIL import Image
from io import BytesIO

def download_and_save_image(url, filename, size=(800, 600)):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        # Resize while maintaining aspect ratio
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save with quality optimization
        img.save(filename, 'JPEG', quality=85, optimize=True)
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {str(e)}")

# Create media directory if it doesn't exist
media_dir = 'media/menu_items'
os.makedirs(media_dir, exist_ok=True)

# Dictionary of menu items and their image URLs
menu_images = {
    'pesarattu.jpg': 'https://example.com/pesarattu.jpg',
    'upma.jpg': 'https://example.com/upma.jpg',
    'idli-podi.jpg': 'https://example.com/idli-podi.jpg',
    'punugulu.jpg': 'https://example.com/punugulu.jpg',
    'attu.jpg': 'https://example.com/attu.jpg',
    'mysore-bonda.jpg': 'https://example.com/mysore-bonda.jpg'
}

# Download and process each image
for filename, url in menu_images.items():
    output_path = os.path.join(media_dir, filename)
    if not os.path.exists(output_path):
        download_and_save_image(url, output_path)
