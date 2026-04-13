from src.extraction.word_extractor import extract_word

data = extract_word("data/raw/word/Week4Lab.docx")

for doc in data:
    print(doc["metadata"])
    print(doc["content"][:300])
    print("TABLES:")
    print(doc["tables"])
    print("-" * 50)