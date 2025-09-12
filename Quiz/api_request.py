import os
import json
import requests
from django.conf import settings
from requests.exceptions import RequestException

def send_api_to_openrouter(prompt):
    try:
        response = requests.post(
            settings.OPENROUTER_API_ENDPOINT,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a skin care recommendation assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 800
            },
            timeout=20
        )
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        return {
            "error": str(e),
            "status_code": getattr(e.response, 'status_code', None)
        }

def send_image_to_openrouter(prompt, image_url):
    
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY_2}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openrouter/sonoma-sky-alpha",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ],
    }

    response = requests.post(settings.OPENROUTER_API_ENDPOINT, headers=headers, data=json.dumps(payload))

    try:
        data = response.json()
    except json.JSONDecodeError:
        raise Exception(f"OpenRouter API did not return JSON: {response.text}")

    if "error" in data:
        raise Exception(f"OpenRouter API error: {data['error']}")

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        raise Exception(f"Unexpected API response format: {json.dumps(data, indent=2)}")