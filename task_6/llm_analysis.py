import os
from google import genai

class LLMAnalyst:
    def __init__(self, api_key):
        # Initialize the new GenAI client
        self.client = genai.Client(api_key=api_key)
        # Using the fast Flash model
        self.model_id = 'gemini-2.5-flash'

    def generate_insight(self, text):
        """Sends text to Gemini and asks for an Investment Memo."""
        
        # Gemini can handle A LOT of text, so we can pass up to 30,000 characters safely
        truncated_text = text[:30000]

        print("   > 🧠 Sending text to Google Gemini...")

        # The Prompt (The instructions for the AI)
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

        # Call the API using the new SDK syntax
        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"❌ LLM Error: {str(e)}"

    def save_report(self, insights, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write("# 🧠 AI Investment Memo\n")
            f.write(f"**Model:** Google Gemini\n\n")
            f.write(insights)
        print(f"✅ AI Report saved to: {filename}")

# --- STANDALONE RUNNER ---
if __name__ == "__main__":
    # 1. PASTE YOUR NEW GOOGLE API KEY HERE (Keep the quotes!)
    GEMINI_KEY = "PASTE YOUR NEW GOOGLE API KEY HERE"
    
    # 2. Define File Paths 
    input_file = os.path.join("output", "earnings.txt")
    output_file = os.path.join("output", "earnings_memo.md")

    # 3. Check and Run
    if os.path.exists(input_file):
        print(f"📂 Found data file: {input_file}")
        
        # Read the file
        with open(input_file, "r", encoding="utf-8") as f:
            text_content = f.read()
            
        # Run Analysis
        analyst = LLMAnalyst(GEMINI_KEY)
        insight = analyst.generate_insight(text_content)
        
        # Save the report
        analyst.save_report(insight, output_file)
        
        # Print it to the console so you can see it immediately
        print("\n==================================================")
        print("                GENERATED MEMO                    ")
        print("==================================================")
        print(insight)
        print("==================================================")
    else:
        print(f"❌ Error: Could not find '{input_file}'")
        print("   Make sure you have run the conversion step at least once.")