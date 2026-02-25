import os
import json
from google import genai
from google.genai import types

class ReceiptAnalyzer:
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.5-flash'

    def process_receipt(self, text):
        """Extracts structured financial data from raw receipt text."""
        print("   > 🧾 Processing receipt data...")

        prompt = f"""
        You are the backend extraction engine for a personal financial manager. 
        Read the following raw text from a receipt and extract the transaction details.
        
        Analyze this text:
        {text[:10000]}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=types.Schema(
                        type="OBJECT",
                        properties={
                            "merchant_name": {"type": "STRING", "description": "Name of the store or service"},
                            "customer_name": {"type": "STRING", "description": "Name of the customer, if available"},
                            "transaction_date": {"type": "STRING", "description": "Date in YYYY-MM-DD format if possible"},
                            "total_amount": {"type": "NUMBER", "description": "The final total charged including taxes"},
                            "currency": {"type": "STRING", "description": "Currency code like USD, EUR, INR"},
                            "expense_category": {
                                "type": "STRING", 
                                "description": "Categorize strictly as: Groceries, Utilities, Entertainment, Dining, Transport, Education, or Other"
                            },
                            "line_items": {
                                "type": "ARRAY",
                                "items": {
                                    "type": "OBJECT",
                                    "properties": {
                                        "item_name": {"type": "STRING"},
                                        "price": {"type": "NUMBER"}
                                    }
                                }
                            }
                        },
                        required=["merchant_name", "total_amount", "expense_category", "currency"]
                    )
                )
            )
            return json.loads(response.text)
            
        except Exception as e:
            return {"error": f"LLM Processing Failed: {str(e)}"}

    def save_to_markdown(self, data, filename):
        """Formats the extracted JSON data into a clean Markdown report."""
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🧾 Expense Extraction Report\n\n")
            
            # Handle potential API errors gracefully
            if "error" in data:
                f.write(f"**Status:** ❌ Failed\n\n")
                f.write(f"**Error Details:** {data['error']}\n")
                print(f"❌ Error saved to: {filename}")
                return
                
            f.write(f"**Status:** ✅ Success\n\n")
            
            # 1. Write the Summary Section
            f.write(f"## 🏪 Transaction Details\n")
            f.write(f"* **Merchant:** {data.get('merchant_name', 'N/A')}\n")
            f.write(f"* **Customer:** {data.get('customer_name', 'N/A')}\n")
            f.write(f"* **Date:** {data.get('transaction_date', 'N/A')}\n")
            f.write(f"* **Category:** {data.get('expense_category', 'N/A')}\n")
            f.write(f"* **Total Amount:** {data.get('currency', '')} {data.get('total_amount', 0.0)}\n\n")
            
            # 2. Write the Line Items Table
            f.write(f"## 🛒 Line Items\n")
            f.write("| Item Name | Price |\n")
            f.write("|---|---|\n")
            for item in data.get('line_items', []):
                name = item.get('item_name', 'Unknown')
                price = item.get('price', 0.0)
                f.write(f"| {name} | {price} |\n")
            
            # 3. Append the Raw JSON for debugging/database reference
            f.write(f"\n## 💻 Raw JSON Output\n")
            f.write("```json\n")
            f.write(json.dumps(data, indent=2) + "\n")
            f.write("```\n")
            
        print(f"📄 Markdown report successfully saved to: {filename}")


# --- STANDALONE RUNNER ---
if __name__ == "__main__":
    # 1. Setup API Key and Paths
    GEMINI_KEY = "AIzaSyAfV3FehDcX92um_HI83oS9OuCLvXpOkpc"
    output_filepath = os.path.join("output", "receipt_log_001.md")
    
    analyzer = ReceiptAnalyzer(GEMINI_KEY)
    
    # 2. Embedded Sample Receipt
    raw_receipt_text = """
    ========================================
             FRESH MART SUPERSTORE
             Kattakkada, Kerala
    ========================================
    Date: 2026-02-24
    Time: 18:45
    Customer: Abin J Antony

    ITEMS:
    1x Organic Rice (5kg)          INR 350.00
    2x Toned Milk (1L)             INR 100.00
    1x Python Crash Course Book    INR 850.00
    1x Nescafé Classic (100g)      INR 150.00

    ----------------------------------------
    Subtotal:                     INR 1450.00
    Tax (GST 5%):                   INR 72.50
    ----------------------------------------
    TOTAL:                        INR 1522.50
    ========================================
    Paid via UPI
    Thank you for shopping with us!
    """

    # 3. Process the text
    result = analyzer.process_receipt(raw_receipt_text)
    
    # 4. Save to Markdown
    analyzer.save_to_markdown(result, output_filepath)