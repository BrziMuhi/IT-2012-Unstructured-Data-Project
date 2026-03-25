from src.extraction.pdf_extractor import extract_pdf

data = extract_pdf("data/raw/pdf/Week4Lab.pdf")

for page in data:
    print(page["metadata"])
    print(page["content"][:200])
    
    print("TABLES:")
    print(page["tables"])   
    print("-" * 50)