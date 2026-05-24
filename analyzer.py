import anthropic
import base64
from prompts import SYSTEM_PROMPT

client = anthropic.Anthropic()

def encode_image(image_bytes):
    return base64.standard_b64encode(image_bytes).decode("utf-8")

def analyze_chart(image_bytes, question=None):
    image_data = encode_image(image_bytes)
    user_content = [
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_data,
            },
        },
        {
            "type": "text",
            "text": question or "Analyse ce graphique et donne-moi un signal de trading."
        }
    ]
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}]
    )
    return response.content[0].text
