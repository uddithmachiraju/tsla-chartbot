import requests
import google.generativeai as genai

class GeminiAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = genai.GenerativeModel("gemini-pro")

    def query(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"prompt": prompt, "max_tokens": 150}
        response = requests.post(self.endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("answer", "No answer returned")
        else:
            return f"Error: {response.status_code} - {response.text}"
