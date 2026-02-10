import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)


with open("td.md", "r", encoding="utf-8") as f:
    text = f.read()

# Text cleaning
text = re.sub(r'Page\s+\d+', '', text)
text = re.sub(r'[^\w\s\$%\/]', '', text)
text = re.sub(r'\s+', ' ', text).strip()

# Tokenization
tokens = word_tokenize(text)

# Stop word removal
stop_words = set(stopwords.words('english'))
filtered_tokens = [w for w in tokens if w.lower() not in stop_words]

# Stemming
stemmer = PorterStemmer()
stemmed_tokens = [stemmer.stem(w) for w in filtered_tokens]

# Lemmatization
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(w) for w in filtered_tokens]

# Save output
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("CLEANED TEXT:\n")
    f.write(text + "\n\n")

    f.write("TOKENS:\n")
    f.write(str(tokens) + "\n\n")

    f.write("AFTER STOP WORD REMOVAL:\n")
    f.write(str(filtered_tokens) + "\n\n")

    f.write("STEMMING RESULT:\n")
    f.write(str(stemmed_tokens) + "\n\n")

    f.write("LEMMATIZATION RESULT:\n")
    f.write(str(lemmatized_tokens) + "\n")

print("Task executed successfully.")