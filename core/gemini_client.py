import requests
# Import the centralized config object instead of yaml and os
from utils.config_loader import config

class GeminiClient:
    # The __init__ method is now much simpler
    def __init__(self):
        # Access the pre-loaded and processed config directly
        gemini_config = config['gemini']
        self.api_key = gemini_config['api_key']
        self.base_url = gemini_config['base_url']

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY could not be resolved. Check your .env file and config.yaml.")

        self.model = "gemini-1.5-flash"
        self.url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"

    # The generate_answer method remains unchanged
    def generate_answer(self, query: str, context: str, history: list = None) -> str:
        contents = []
        
        if history:
            for user_query, bot_answer in history:
                contents.append({"role": "user", "parts": [{"text": user_query}]})
                contents.append({"role": "model", "parts": [{"text": bot_answer}]})

        user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
        contents.append({"role": "user", "parts": [{"text": user_prompt}]})

        headers = {"Content-Type": "application/json"}
        payload = {"contents": contents}
        
        response = requests.post(self.url, headers=headers, json=payload)
        
        if response.status_code == 200:
            try:
                resp = response.json()
                return resp["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError) as e:
                raise Exception(f"Gemini API response parse error: {e}")
        else:
            raise Exception(f"Gemini API error: {response.status_code} {response.text}")