from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="A futuristic AI newsroom"
)

response.generated_images[0].image.save(
    "test.png"
)

print("SUCCESS")
