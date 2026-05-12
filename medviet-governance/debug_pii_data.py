import pandas as pd
from src.pii.detector import build_vietnamese_analyzer, detect_pii

analyzer = build_vietnamese_analyzer()
df = pd.read_csv("data/raw/patients_raw.csv").head(50)
pii_columns = ["ho_ten", "cccd", "so_dien_thoai", "email"]

for col in pii_columns:
    print(f"\n--- Checking column: {col} ---")
    detected_count = 0
    for value in df[col].astype(str):
        results = detect_pii(value, analyzer)
        if len(results) > 0:
            detected_count += 1
        else:
            print(f"FAILED to detect PII in: {value}")
    print(f"Col {col}: {detected_count}/{len(df)} detected.")
