# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 Envelope Encryption (Vault) | ✅ Done | Infra Team |
| Audit logging | FastAPI Middleware + API access logs | ✅ Done | Platform Team |
| Breach detection | Prometheus Metrics + Grafana Alerts | ✅ Done | Security Team |

## F. Giải pháp kỹ thuật cho các phần còn thiếu:
1. **Audit logging:** Triển khai Middleware trong FastAPI để ghi lại nhật ký (logs) cho mọi request đến API, bao gồm: `user_id`, `role`, `endpoint`, `action`, `timestamp` và `status_code`. Dữ liệu logs được lưu trữ tập trung tại hệ thống ELK Stack hoặc CloudWatch để phục vụ truy vết.
2. **Breach detection:** Sử dụng Prometheus để theo dõi các metrics như tỷ lệ lỗi 403 (Truy cập bị chặn) tăng đột biến hoặc lưu lượng truy cập bất thường. Thiết lập cảnh báo (Alertmanager) gửi thông báo ngay lập tức qua Slack/Email cho Security Team khi phát hiện dấu hiệu tấn công hoặc rò rỉ dữ liệu.
3. **Encryption:** Sử dụng mô hình Envelope Encryption với Master Key (KEK) quản lý trong Vault và Data Key (DEK) được tạo mới cho mỗi bản ghi dữ liệu, đảm bảo dữ liệu nhạy cảm luôn được bảo vệ ở trạng thái nghỉ (At-rest).
