# Hướng Dẫn Chạy Lab Day 24: MedViet Data Governance

Tài liệu này hướng dẫn cách vận hành hệ thống Quản trị dữ liệu và Bảo mật sau khi đã hoàn thiện code.

---

## 🛠 1. Chuẩn bị môi trường (Setup)

Mở terminal tại thư mục `medviet-governance/` và thực hiện các lệnh sau:

```bash
# 1. Cài đặt các thư viện từ requirements.txt
pip install -r requirements.txt

# 2. Tải mô hình ngôn ngữ tiếng Việt (Bắt buộc cho Spacy 3.6)
python -m spacy download vi_core_news_lg
```

---

## 📂 2. Khởi tạo dữ liệu (Data Generation)

Trước khi chạy hệ thống, bạn cần tạo tập dữ liệu bệnh nhân giả lập chứa thông tin nhạy cảm (PII).

```bash
python scripts/generate_data.py
```
*   **Kết quả:** File `data/raw/patients_raw.csv` sẽ được tạo ra với 200 bản ghi.
*   **📸 Chụp ảnh:** Chụp màn hình terminal báo "Generated 200 patient records" để làm bằng chứng bước 1.

---

## 🧪 3. Kiểm tra tính năng ẩn danh (Testing)

Chạy Unit Test để đảm bảo bộ lọc PII hoạt động chính xác và đạt tỷ lệ nhận diện > 95%.

```bash
pytest tests/test_pii.py -v
```
*   **Kết quả:** Tất cả các test case (CCCD, Phone, Email detection) phải hiển thị `PASSED`.
*   **📸 Chụp ảnh:** Chụp màn hình kết quả Test màu xanh để làm bằng chứng bước 3.

---

## 🌐 4. Khởi chạy API và Kiểm tra phân quyền (RBAC)

### 4.1. Khởi chạy Server
```bash
uvicorn src.api.main:app --reload
```
Server sẽ chạy tại: `http://localhost:8000`

### 4.2. Kiểm tra truy cập (Dùng Postman hoặc Curl)

**Trường hợp 1: Admin (Alice) truy cập dữ liệu thô (Thành công)**
```bash
curl -H "Authorization: Bearer token-alice" http://localhost:8000/api/patients/raw
```

**Trường hợp 2: ML Engineer (Bob) truy cập dữ liệu thô (Bị chặn - 403)**
```bash
curl -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/raw
```
*   **📸 Chụp ảnh:** Chụp màn hình lỗi `403 Forbidden` khi Bob truy cập dữ liệu thô.

**Trường hợp 3: ML Engineer (Bob) truy cập dữ liệu đã ẩn danh (Thành công)**
```bash
curl -H "Authorization: Bearer token-bob" http://localhost:8000/api/patients/anonymized
```

---

## 🔐 5. Kiểm tra Mã hóa (Encryption)

Để kiểm tra module mã hóa Envelope Encryption hoạt động đúng:

1. Mở Python shell: `python`
2. Chạy đoạn code sau:
```python
from src.encryption.vault import SimpleVault
vault = SimpleVault()
encrypted = vault.encrypt_data("Dữ liệu tuyệt mật")
print(encrypted)
decrypted = vault.decrypt_data(encrypted)
print(f"Dữ liệu giải mã: {decrypted}")
```
*   **📸 Chụp ảnh:** Chụp kết quả giải mã khớp với dữ liệu gốc.

---

## ✅ 6. Kiểm định chất lượng (Data Quality)

Chạy script validation để kiểm tra dữ liệu ẩn danh có vi phạm quy tắc nào không.

```bash
python -c "from src.quality.validation import validate_anonymized_data; print(validate_anonymized_data('data/raw/patients_raw.csv'))"
```
*   **📸 Chụp ảnh:** Chụp kết quả trả về `{'success': True, ...}`.

---

## 📝 Tổng kết danh sách bằng chứng cần nộp
Lưu tất cả ảnh vào thư mục `medviet-governance/evidence/`:
1. `step1_data.png` (Data Generation)
2. `step2_tests.png` (Pytest results)
3. `step3_rbac_alice.png` (Admin access success)
4. `step4_rbac_bob_403.png` (ML Engineer access denied)
5. `step5_encryption.png` (Vault test results)
6. `step6_validation.png` (Quality check results)
