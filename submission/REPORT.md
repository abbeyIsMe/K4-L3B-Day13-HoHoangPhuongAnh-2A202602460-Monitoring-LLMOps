# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Hồ Hoàng Phương Anh
- **MSSV:** 2A202602460
- **Lớp:** K4-L3B
- **Repository URL:** 
- **Commit SHA cuối:**
- **Challenge ID:**
- **Tên project Langfuse cá nhân:** `day13-k4-l3b-<MSSV>`

## 2. Evidence index

Chưa có runtime evidence trong workspace; chỉ điền link sau khi tự chạy workload và chụp kết quả của project cá nhân. Không dùng ảnh placeholder để thay thế evidence.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | Chờ chạy ở commit cuối |
| Log validator | Chờ chạy sau khi tạo log mới |
| Dashboard validator | Chờ chạy |
| Structured log | Chờ chụp log runtime đã scrub |
| PII redaction | Chờ chụp kiểm chứng runtime |
| Trace list | Chờ tạo trace trong project Langfuse cá nhân |
| Trace waterfall | Chờ tạo trace trong project Langfuse cá nhân |
| Trace metadata | Chờ tạo trace trong project Langfuse cá nhân |
| Prompt versions | Chờ tạo prompt v1/v2 trong project cá nhân |
| Prompt rollback | Chờ thực hiện rollback label production |
| Dashboard runtime | Chờ dựng dashboard có dữ liệu |
| Incident metric | Chờ challenge chính thức của Lab Coach |
| Incident log | Chờ challenge chính thức của Lab Coach |
| Incident trace | Chờ challenge chính thức của Lab Coach |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 100/100 | Chưa đo | 83 records, 0 missing required fields, 0 missing enrichment, 40 unique correlation IDs, 0 PII leaks |
| `validate_dashboard.py` | 6/6 panel | Chưa đo | Tất cả 6 panel trong dashboard contract đều hợp lệ |
| `pytest` | 21 passed, 1 failed | Chưa đo | 1 test fail liên quan `RecordingLangfuseClient` và v4 Observation API |
| Số traces hợp lệ | Chưa đo | Chưa đo | Chưa xác nhận trace trên Langfuse |
| Số PII leak | 0 | Chưa đo | Theo `validate_logs.py` |
| Latency P95 / TTFT P95 | Chưa đo | Chưa đo | Chưa có metric P95 |
| Retrieval success rate | Chưa đo | Chưa đo | Chưa có metric baseline |

## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** Middleware nhận `x-request-id` đúng dạng `req-<8-hex>`, nếu không hợp lệ thì sinh ID mới; bind vào structlog context và trả qua response header.
- **Các metadata được ghi vào structured log:** `user_id_hash`, `session_id`, `feature`, `model`, `env` cùng `correlation_id`.
- **Cách bảo đảm PII được scrub trước khi ghi:** `scrub_event` chạy trước file writer/JSON renderer và duyệt đệ quy string trong event; preview prompt/answer dùng `summarize_text`.
- **Cách kiểm chứng kết quả:** Chưa chạy; cần gửi email/điện thoại/CCCD/thẻ mẫu qua log thử, kiểm tra JSONL không còn giá trị nguyên văn và chụp evidence.

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:**
- **Cấu trúc root/retrieval/generation observations:** Root `lab-agent-run` chứa child `retrieval` (retriever) và `llm-generation` (generation); generation cập nhật model, prompt preview đã scrub, token usage và cost.
- **Cách nối trace với log:**
- **Prompt name:**
- **Version/label baseline:**
- **Version/label candidate:**
- **Trace ID của mỗi version:**
- **Cách promote và rollback `production`:**

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:**
- **SLO và lý do chọn:** `fast_successful_requests`: 99.5% request phải thành công trong 3000 ms theo cửa sổ 28 ngày; cần đối chiếu ngưỡng latency với baseline thực tế trước khi chốt.
- **Cách tính error budget:** 100% - 99.5% = 0.5%; với 10,000 request trong cửa sổ, tối đa 50 request không đạt điều kiện SLO.
- **Ba alert và runbook tương ứng:** HighLatencyP95 (5 phút), ElevatedErrorRate (3 phút), LowRetrievalSuccess (5 phút); chi tiết tại `docs/alerts.md`. Thay owner `student-<MSSV>` bằng MSSV của mình trước khi nộp.

> Ví dụ cách viết error budget: "SLO 99.5% trong 28 ngày nghĩa là error budget 0.5%. Nếu workload có 10,000 request thì tối đa 50 request được phép lỗi hoặc chậm hơn ngưỡng SLO."

## 7. Điều tra challenge

- **Challenge ID:**
- **Khoảng thời gian điều tra:**
- **Triệu chứng từ metrics:**
- **Log line và correlation ID liên quan:**
- **Trace ID và span gây ảnh hưởng:**
- **Root cause:**
- **Fix action:**
- **Preventive measure:**

> Gợi ý cách viết ngắn, không thay cho evidence thực tế: "Metric cho thấy `[latency/error/cost/quality]` bất thường trong `[khoảng thời gian]`. Log line `[event]` có `correlation_id=[...]` đại diện cho request bị ảnh hưởng. Trace cùng `correlation_id` cho thấy span `[retrieval/generation/prompt/tool]` có dấu hiệu `[chậm/lỗi/token tăng]`. Root cause là `[nguyên nhân suy ra từ evidence]`. Fix action là `[hành động khôi phục]`; preventive measure là `[alert/runbook/test/guardrail để ngăn tái diễn]`."

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:**
- **Một lỗi/blocker đã gặp:**
- **Cách tìm nguyên nhân và xử lý:**
- **Cách hiểu luồng Metrics → Logs → Traces:**
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**
- **Điều quan trọng nhất đã học:**
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:**

## 9. Checklist trước khi nộp

- [ ] Kết quả và evidence thuộc commit SHA cuối.
- [ ] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [ ] Incident evidence nối đúng metric → log → trace.
- [ ] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ ] Repository chạy lại được theo README.
- [ ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [ ] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
