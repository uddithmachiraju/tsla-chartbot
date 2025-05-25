import google.generativeai as genai

class GeminiAgent:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("models/gemini-1.5-flash-latest")

    def query(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text
