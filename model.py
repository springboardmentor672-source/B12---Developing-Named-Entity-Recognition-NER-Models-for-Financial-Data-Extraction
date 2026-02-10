from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

model_name = "dslim/bert-base-NER"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

finance_ner = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)
import spacy

nlp_general = spacy.load("en_core_web_trf")
def combined_ner(text):
    results = []

    # ---- General NER (spaCy) ----
    doc = nlp_general(text)
    for ent in doc.ents:
        results.append({
            "text": ent.text,
            "label": ent.label_,
            "source": "general"
        })

    # ---- Financial NER (FinBERT) ----
    fin_ents = finance_ner(text)
    for ent in fin_ents:
        results.append({
            "text": ent["word"],
            "label": ent["entity_group"],
            "source": "financial"
        })

    return results
text = """Dear Shareholders, it is with great pride and deep gratitude that 
I present to you the Annual Report for the financial year 2024–25, 
a year of strong performance, strategic transformation, anddeepened 
trust with all our stakeholders. This was not just a year of numbers,
 but of meaningful progress as we continued to shape Jana Small Finance 
 Bank into a future-ready, purpose-driven institution.Delivering Growth
   with Purpose In a dynamic and often uncertain economic environment, 
   your Bank delivered resilient and wellrounded performance. Our success 
   was powered by disciplined execution, innovation rooted in customer needs,
     and a continued commitment to financial inclusion. FY 2024–25 marked 
     another significant step in our journey of purposeful growth, where
       performance and purpose walked hand in hand. We ended the year with 
       a gross loan portfolio of `29,545 crore, with secured loans growing
         steadily to comprise 70% of the book. Our presence deepened across
           India with 802 branches now serving over 42 lakh active customers in
             23 states and 2 Union Territories."""


entities = combined_ner(text)

for e in entities:
    print(e)
