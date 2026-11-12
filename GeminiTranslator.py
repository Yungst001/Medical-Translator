import os
import re
from google import genai


def clean_text(text):
    # FDA data can sometimes arrive as a list.
    if isinstance(text, list):
        text = " ".join(text)

    # Remove extra spaces and line breaks.
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def translate_drug_info(drug_name, fda_text):
    clean_info = clean_text(fda_text)

    prompt = f"""
Explain this drug information in simple English.

Drug name: {drug_name}
Information: {clean_info}

Include:
- What it is used for
- How to take it
- Warnings
- Common side effects

Do not give personal medical advice.
"""

    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception:
        return clean_info