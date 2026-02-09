import re
import os

class PurePythonNLP:
    def __init__(self):
        # 1. Define our own "Stop Words" list (Common words to ignore)
        self.stop_words = {
            "the", "of", "and", "to", "in", "a", "is", "for", "on", "with", 
            "as", "by", "at", "it", "that", "from", "are", "was", "be", "or"
        }
        
        # 2. Define a small Dictionary for Lemmatization (The "Smart" Map)
        # In a real app, this would be a huge database. Here we map key financial terms.
        self.lemma_dict = {
            "revenues": "revenue",
            "operating": "operate",
            "investing": "invest",
            "quarterly": "quarter",
            "companies": "company",
            "generated": "generate",
            "losses": "loss",
            "customers": "customer",
            "started": "start"
        }

    def clean_text(self, text):
        """
        Removes junk but PRESERVES financial symbols: $, %, /, .
        """
        # Remove Page numbers
        text = re.sub(r'\n\d+\n', ' ', text)
        
        # Keep letters, numbers, spaces, and $, %, /, .
        cleaned = re.sub(r'[^a-zA-Z0-9\s$%/.]', '', text)
        
        # Collapse spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    def tokenize(self, text):
        """Splits text into words using standard logic."""
        return text.split()

    def remove_stopwords(self, tokens):
        """Filters out the boring words."""
        return [w for w in tokens if w.lower() not in self.stop_words]

    # --- THE COMPARISON TOOLS ---

    def simple_stemmer(self, word):
        """
        STEMMING (The Chopper): 
        Blindly chops off common endings like 'ing', 'ed', 's'.
        """
        word = word.lower()
        if word.endswith("ing"): return word[:-3]
        if word.endswith("ed"):  return word[:-2]
        if word.endswith("s") and not word.endswith("ss"):   return word[:-1]
        if word.endswith("ly"):  return word[:-2]
        return word

    def simple_lemmatizer(self, word):
        """
        LEMMATIZATION (The Dictionary):
        Looks up the word in our list to find the meaningful root.
        """
        clean_word = word.lower()
        # Return the dictionary match, OR the original word if not found
        return self.lemma_dict.get(clean_word, clean_word)

    def run_comparison(self, tokens):
        results = []
        for word in tokens:
            stem = self.simple_stemmer(word)
            lemma = self.simple_lemmatizer(word)
            results.append((word, stem, lemma))
        return results

# --- EXECUTION ---
if __name__ == "__main__":
    # 1. Load File
    input_path = "output/earnings.txt"
    
    if not os.path.exists(input_path):
        print(f"❌ Error: File not found at {input_path}")
    else:
        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

        nlp = PurePythonNLP()

        # 2. Clean & Tokenize
        print(f"--- 1. Processing Text ---")
        cleaned = nlp.clean_text(raw_text)
        tokens = nlp.tokenize(cleaned)
        filtered_tokens = nlp.remove_stopwords(tokens)
        
        print(f"Raw Tokens: {len(tokens)}")
        print(f"After Stop Words: {len(filtered_tokens)}")

        # 3. Compare Stemming vs Lemmatization
        print(f"\n--- 2. Comparison Test (Stemming vs Lemmatization) ---")
        print(f"{'ORIGINAL':<15} | {'STEMMING (Chopping)':<20} | {'LEMMATIZATION (Dictionary)':<20}")
        print("-" * 65)

        # We grab a slice of words that usually show interesting differences
        comparison_data = nlp.run_comparison(filtered_tokens)
        
        # We verify we have enough words, then show a slice
        start_index = 20 if len(comparison_data) > 20 else 0
        end_index = start_index + 15
        
        for orig, stem, lemma in comparison_data[start_index:end_index]:
            print(f"{orig:<15} | {stem:<20} | {lemma:<20}")
            
        print("-" * 65)
        print("\nOBSERVATION:")
        print("1. Stemming chops blindly (e.g., 'Quarterly' -> 'Quarter').")
        print("2. Lemmatization uses knowledge (e.g., 'Revenues' -> 'Revenue').")
        print("   Notice how symbols ($102.3) remained safe because of our cleaning rules!")