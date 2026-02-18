import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def write_paragraph(f, data, words_per_line=18):
    for i in range(0, len(data), words_per_line):
        f.write(" ".join(data[i:i+words_per_line]) + "\n")
    f.write("\n")
    
# ---------input file------------------
with open("output.md", "r", encoding="utf-8") as f:
    text = f.read()
    
# ------------TEXT CLEANING---------------
text = re.sub(r'Page\s+\d+', '', text)
text = re.sub(r'\s+', ' ', text)
text = re.sub(r'[^a-zA-Z0-9$%/.\s]', '', text)
print("\n--- CLEANED TEXT SAMPLE ---")
print(text[:300])

# ----------TOKENIZATION-----------------
tokens = word_tokenize(text)
print("\n--- TOKENS SAMPLE ---")
print(tokens[:30])

# -------------STOP WORD REMOVAL--------------
stop_words = set(stopwords.words('english'))
filtered_tokens = [w for w in tokens if w.lower() not in stop_words]
print("\n--- FILTERED TOKENS SAMPLE ---")
print(filtered_tokens[:30])

# -----------STEMMING----------------
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(w) for w in filtered_tokens]
print("\n--- STEMMED TOKENS SAMPLE ---")
print(stemmed_tokens[:30])

# -----------LEMMATIZATION----------------
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(w) for w in filtered_tokens]
print("\n--- LEMMATIZED TOKENS SAMPLE ---")
print(lemmatized_tokens[:30])

# ------------COMPARISON TEST---------------
comparison_lines = []
for i in range(min(50, len(filtered_tokens))):
    line = f"{filtered_tokens[i]} -> Stem: {stemmed_tokens[i]} | Lemma: {lemmatized_tokens[i]}"
    comparison_lines.append(line)
print("\n--- COMPARISON SAMPLE ---")
for line in comparison_lines[:10]:
    print(line)
# ----------- OUTPUT FILES----------------
outputs = {
    "cleaned_text.txt": text,
    "tokens.txt": "\n".join(tokens),
    "filtered_tokens.txt": "\n".join(filtered_tokens),
    "stemmed_tokens.txt": "\n".join(stemmed_tokens),
    "lemmatized_tokens.txt": "\n".join(lemmatized_tokens),
    "comparison.txt": "\n".join(comparison_lines)
}
for filename, content in outputs.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

with open("final_output_new.txt", "w", encoding="utf-8") as f:
    f.write("===== CLEANED TEXT =====\n\n")
    f.write(text)
    f.write("\n\n")
    f.write("===== TOKENS =====\n\n")
    f.write(" ".join(tokens))
    f.write("\n\n")
    f.write("===== FILTERED TOKENS =====\n\n")
    f.write(" ".join(filtered_tokens))
    f.write("\n\n")
    f.write("===== STEMMED TOKENS =====\n\n")
    f.write(" ".join(stemmed_tokens))
    f.write("\n\n")
    f.write("===== LEMMATIZED TOKENS =====\n\n")
    f.write(" ".join(lemmatized_tokens))
    f.write("\n\n")
    f.write("===== STEMMING vs LEMMATIZATION COMPARISON =====\n\n")
    f.write(" ".join(comparison_lines))  
    f.write("\n")
print("\nALL TASKS COMPLETED SUCCESSFULLY!")
