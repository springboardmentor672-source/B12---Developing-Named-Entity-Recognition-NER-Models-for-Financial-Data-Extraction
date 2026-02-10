import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Run once if not already downloaded
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# ---------------- LOAD TEXT ----------------
with open("output.md", "r", encoding="utf-8") as f:
    text = f.read()

# ---------------- ORIGINAL TEXT ----------------
print("\nORIGINAL TEXT:")
print(text[:500], "...") # show first part only

# ---------------- CLEANING ----------------
cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip().lower()
print("\nCLEANED TEXT:")
print(cleaned_text[:500], "...")

# ---------------- TOKENIZATION ----------------
tokens = word_tokenize(cleaned_text)

print("\nTOKENIZED TEXT:")
print(tokens[:20], "...")

# ---------------- STOP WORD REMOVAL ----------------
stop_words = set(stopwords.words('english'))
filtered_tokens = [w for w in tokens if w not in stop_words]

print("\nSTOP WORDS REMOVED:")
print(" ".join(filtered_tokens[:30]), "...")

# ---------------- STEMMING ----------------
stemmer = PorterStemmer()
stemmed = [stemmer.stem(w) for w in filtered_tokens]

print("\nSTEMMED TEXT:")
print(" ".join(stemmed[:30]), "...")

# ---------------- LEMMATIZATION ----------------
lemmatizer = WordNetLemmatizer()
lemmatized = [lemmatizer.lemmatize(w) for w in filtered_tokens]

print("\nLEMMATIZED TEXT:")
print(" ".join(lemmatized[:30]), "...")