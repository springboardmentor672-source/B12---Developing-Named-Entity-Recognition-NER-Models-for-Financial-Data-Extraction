# STEP 1: Read input text
with open("input.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("Original Text:\n")
print(text[:500])  # show only first 500 characters

import re

# Remove page numbers (example: "Page 1")
text = re.sub(r'Page\s+\d+', '', text)

# Remove extra spaces and new lines
text = re.sub(r'\s+', ' ', text)

# Remove junk characters but keep financial symbols
text = re.sub(r'[^a-zA-Z0-9$%/. ]', '', text)

print("\nCleaned Text:\n")
print(text[:500])

from nltk.tokenize import word_tokenize

tokens = word_tokenize(text)

print("\nTokens:\n")
print(tokens[:30])

from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

filtered_tokens = [
    word for word in tokens
    if word.lower() not in stop_words
]

print("\nAfter Stop Words Removal:\n")
print(filtered_tokens[:30])

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

stemmed_words = [stemmer.stem(word) for word in filtered_tokens]

print("\nStemmed Words:\n")
print(stemmed_words[:30])

import spacy

nlp = spacy.load("en_core_web_sm")

doc = nlp(" ".join(filtered_tokens))
lemmatized_words = [token.lemma_ for token in doc]

print("\nLemmatized Words:\n")
print(lemmatized_words[:30])