import os
import json
import requests
from django.conf import settings
from requests.exceptions import RequestException

def send_api_to_openrouter(prompt):
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
                ],
            }
        ],
    }

    response = requests.post(settings.OPENROUTER_API_ENDPOINT, headers=headers, data=json.dumps(payload))

    try:
        data = response.json()
        return data
    except json.JSONDecodeError:
        raise Exception(f"OpenRouter API did not return JSON: {response.text}")

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