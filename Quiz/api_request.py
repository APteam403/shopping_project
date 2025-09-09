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