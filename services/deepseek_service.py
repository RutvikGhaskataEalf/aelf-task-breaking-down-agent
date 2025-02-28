import requests
from config import deepseek_api_key, deepseek_endpoint

def fetch_deepseek_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "api-key": deepseek_api_key
    }
    payload = {
        "messages": [{"role": "system", "content": "You are a highly skilled assistant."}, {"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False
    }
    response = requests.post(f"{deepseek_endpoint}/chat/completions?api-version=2024-02-15-preview",
                             headers=headers,
                             json=payload)
    return response.json()