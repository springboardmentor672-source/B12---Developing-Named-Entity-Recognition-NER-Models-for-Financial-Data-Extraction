import re

def extract_entities(text: str):
    entities = {
        "COMPANY": [],
        "MONEY": [],
        "PERCENTAGE": [],
        "DATE": []
    }

    companies = re.findall(r'\b[A-Z][a-zA-Z]+ (Inc|Ltd|Corporation|Company)\b', text)
    entities["COMPANY"] = companies

    money = re.findall(r'\$\d+(?:\.\d+)?\s?(billion|million)?', text)
    entities["MONEY"] = money

    percentages = re.findall(r'\d+%', text)
    entities["PERCENTAGE"] = percentages

    dates = re.findall(
        r'\b(?:Jan|Feb|March|April|May|June|July|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}',
        text
    )
    entities["DATE"] = dates

    return entities
