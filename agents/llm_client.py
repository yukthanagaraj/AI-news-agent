from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    timeout=300.0,
    max_retries=5,
)

MODEL_NAME = "gpt-4o-mini"
IMAGE_MODEL = "gpt-image-1"