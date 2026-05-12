import spacy
from src.pii.detector import build_vietnamese_analyzer, detect_pii

analyzer = build_vietnamese_analyzer()
texts = [
    "Tôi là Nguyễn Văn A",
    "Số điện thoại: 0912345678",
    "CCCD: 012345678901",
    "Email: test@gmail.com"
]

for text in texts:
    results = detect_pii(text, analyzer)
    print(f"Text: {text}")
    for res in results:
        print(f" - Found {res.entity_type} at {res.start}-{res.end} with score {res.score}")
