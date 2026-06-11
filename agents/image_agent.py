from google import genai
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_image(image_prompt):

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=image_prompt
    )

    image = response.generated_images[0].image

    temp_file = "generated_image.png"

    image.save(temp_file)

    upload_result = cloudinary.uploader.upload(
        temp_file,
        folder="ai-news-blog"
    )

    os.remove(temp_file)

    return upload_result["secure_url"]