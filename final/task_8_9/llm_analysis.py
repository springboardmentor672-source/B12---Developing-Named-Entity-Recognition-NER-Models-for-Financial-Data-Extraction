from google import genai

class LLMAnalyst:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.5-flash'

    def generate_insight(self, text):
        truncated_text = text[:30000]
        prompt = f"""
        You are a senior financial analyst. Analyze the provided earnings call transcript.
        Format your response exactly like this:
        
        ### 🚀 Strategic Initiatives (What are they building?)
        * [Point 1]
        * [Point 2]
        * [Point 3]

        ### ⚠️ Key Risks & Headwinds (What is going wrong?)
        * [Point 1]
        * [Point 2]
        * [Point 3]

        ### ⚖️ Analyst Verdict
        [One concise sentence conclusion: Bullish, Bearish, or Neutral and why]

        ---
        TEXT TO ANALYZE:
        {truncated_text}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"❌ LLM Error: {str(e)}"