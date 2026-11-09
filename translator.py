import os
import re
from google import genai


def clean_fda_text(text: str) -> str:
    if not text:
        return "No information was provided."

    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def make_plain_english(drug_name: str, fda_text: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return clean_fda_text(fda_text)  # app still works if AI is unavailable

    cleaned_text = clean_fda_text(fda_text)

    prompt = f"""
Drug name: {drug_name}

Official FDA text:
{cleaned_text[:12000]}

Return only these headings:
What it is used for
How to take it
Important warnings
Common side effects
When to get medical help
"""

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text or cleaned_text
    except Exception:
        return cleaned_text