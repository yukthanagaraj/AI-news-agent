import os
import base64
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from agents.llm_client import client, IMAGE_MODEL
from agents.history_manager import get_used_visual_concepts, remember_visual_concept


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)


def generate_image(image_prompt: str):
    """
    Generates one unique image for every article using OpenAI,
    uploads it to Cloudinary, and returns the Cloudinary URL.

    The article-specific `image_prompt` (from the writer agent) is
    treated as the PRIMARY content — it names the actual visual
    elements of THIS article's thesis. The wrapper below only adds
    quality/format/avoid constraints; it must never override or
    dilute the specific scene with a fixed generic template, or every
    article ends up looking like the same stock illustration.
    """

    recent_concepts = get_used_visual_concepts()[-5:]
    avoid_block = ""
    if recent_concepts:
        avoid_block = (
            "\n\nRecently used visual concepts — do NOT repeat these "
            "compositions, color emphasis, or focal subject; this scene "
            "must look and feel distinctly different from each of them:\n"
            + "\n".join(f"- {c}" for c in recent_concepts)
        )

    enhanced_prompt = f"""
Create a premium editorial illustration for a high-end enterprise AI publication — the cover image of a business technology magazine.

The scene, composition, and focal point below are SPECIFIC to this article's thesis. Follow them precisely rather than defaulting to a generic executive-with-dashboard scene:

{image_prompt}

Style requirements:
- Premium editorial digital illustration, semi-flat, sophisticated corporate aesthetic
- Landscape 16:9, one strong visual focal point, balanced and spacious composition, depth and perspective
- Refined corporate palette — vary the dominant hue to match this article's specific scene (navy, slate, warm orange, deep teal, muted green, etc. as appropriate) rather than defaulting to blue every time
- Soft cinematic lighting, natural shadows, professional atmosphere
- High-end magazine quality, rich detail, minimal visual clutter

CRITICAL — TEXT PROHIBITION:
Absolutely NO text, letters, numbers, words, labels, captions, logos, or watermarks anywhere in the image, including on signage, panels, screens, badges, icons, or any surface within the scene. Do not attempt to render any word, acronym, or label, even a short or generic one (e.g. do not write "COST," "AUDIT," "DATA" or similar words on any element). If you would normally label a panel, icon, or diagram element with a word, instead represent it with an abstract shape, icon, color coding, or symbol with NO characters at all. This is a strict constraint, not a stylistic preference — any rendered text is a failure of this image.

Additional avoid list: no humanoid robots, no floating AI brains, no glowing hologram overload, no UI screenshots or readable dashboards, no cyberpunk or sci-fi movie aesthetics, no stock-photo-style people.
{avoid_block}
"""

    print("Generating image with OpenAI...")

    response = client.images.generate(
        model=IMAGE_MODEL,
        prompt=enhanced_prompt,
        size="1536x1024",
    )

    image_bytes = base64.b64decode(response.data[0].b64_json)

    temp_file = "temp_image.png"

    with open(temp_file, "wb") as f:
        f.write(image_bytes)

    print("Uploading image to Cloudinary...")

    upload_result = cloudinary.uploader.upload(
        temp_file,
        folder="ai-news-blog",
        overwrite=False,
        unique_filename=True,
    )

    os.remove(temp_file)

    print("Image uploaded successfully.")

    remember_visual_concept(image_prompt)

    return upload_result["secure_url"]