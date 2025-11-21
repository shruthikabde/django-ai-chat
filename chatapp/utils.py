import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID", "meta-llama/Llama-3.2-3B-Instruct")


def generate_hf_reply(user_text: str, username: str) -> str:
    """
    Use Hugging Face Router (OpenAI compatible) to get a chat completion.
    Primary language = English.
    User can change language by mentioning it (e.g. 'change language to Hindi').
    """
    if not HF_API_TOKEN:
        return "No Hugging Face API key found. Please set HF_API_TOKEN in .env."

    url = "https://router.huggingface.co/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # ---------- Language logic ----------
    user_text_lower = user_text.lower()

    # default language
    language = "English"

    if "telugu" in user_text_lower:
        language = "Telugu"
    elif "hindi" in user_text_lower:
        language = "Hindi"
    elif "french" in user_text_lower:
        language = "French"
    elif "spanish" in user_text_lower:
        language = "Spanish"
    # you can add more languages here if you want

    system_content = (
        "You are a friendly AI assistant. "
        f"The user's name is {username}. "
        "Your primary language is English, "
        f"but for this conversation you must reply ONLY in {language}. "
        "Do not mix any other language. "
        "Keep responses short, clear, friendly and helpful."
    )

    messages = [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_text,
        },
    ]

    payload = {
        "model": HF_MODEL_ID,      # model id from .env
        "messages": messages,
        "max_tokens": 200,
        "temperature": 0.7,
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        # OpenAI-style response: choices[0].message.content
        try:
            reply = data["choices"][0]["message"]["content"].strip()
            return reply
        except Exception:
            return f"Unexpected response format: {data}"

    except Exception as e:
        return f"Error contacting model: {e}"
