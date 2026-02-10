import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy

nltk.download("punkt")
nltk.download("stopwords")

nlp = spacy.load("en_core_web_sm")

with open("input.txt", "r", encoding="utf-8") as f:
    data = f.read()

print(data[:500])

data = re.sub(r'Page\s+\d+', '', data)
data = re.sub(r'\s+', ' ', data)
data = re.sub(r'[^A-Za-z0-9$%/. ]', '', data)

print(data[:500])

tokens = word_tokenize(data)

stop_words = set(stopwords.words("english"))
filtered = [t for t in tokens if t.lower() not in stop_words]

stemmer = PorterStemmer()
stemmed = [stemmer.stem(t) for t in filtered]

doc = nlp(" ".join(filtered))
lemmatized = [token.lemma_ for token in doc]

print(tokens[:30])
print(filtered[:30])
print(stemmed[:30])
print(lemmatized[:30])

