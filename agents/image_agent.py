import os
import requests
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


def generate_image(category):

    image_urls = {
        "Customer Service AI": "https://images.unsplash.com/photo-1551434678-e076c223a692",
        "Enterprise AI": "https://images.unsplash.com/photo-1497366754035-f200968a6e72",
        "Healthcare AI": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1f",
        "Robotics": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e",
        "Future of Work": "https://images.unsplash.com/photo-1522071820081-009f0129c71c",
        "Sustainable Technology": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e",
    }

    image_url = image_urls.get(
        category,
        "https://images.unsplash.com/photo-1677442136019-21780ecad995"
    )

    temp_file = "temp_image.jpg"

    response = requests.get(image_url)

    with open(temp_file, "wb") as f:
        f.write(response.content)

    upload_result = cloudinary.uploader.upload(
        temp_file,
        folder="ai-news-blog"
    )

    os.remove(temp_file)

    return upload_result["secure_url"]