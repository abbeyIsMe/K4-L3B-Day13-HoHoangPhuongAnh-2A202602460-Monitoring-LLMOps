# Báo cáo cá nhân — K4-L3B Day 13 Monitoring & LLMOps

> Mỗi học viên hoàn thiện một file duy nhất này. Khi dẫn evidence, dùng đường dẫn tương đối, ví dụ `evidence/07-trace-waterfall.png`.

## 1. Thông tin học viên

- **Họ và tên:** Hồ Hoàng Phương Anh
- **MSSV:** 2A202602460
- **Lớp:** K4-L3B
- **Repository URL:** https://github.com/abbeyIsMe/K4-L3B-Day13-HoHoangPhuongAnh-2A202602460-Monitoring-LLMOps
- **Commit SHA cuối:** e3f3fb6c2d3b0dc7d2981c56919046ffbc84beaa
- **Challenge ID:** day13-k4-l3b-monitoring-llmops-v1
- **Tên project Langfuse cá nhân:** day13-k4-l3b-2A202602460

## 2. Evidence index

Chưa có runtime evidence trong workspace; chỉ điền link sau khi tự chạy workload và chụp kết quả của project cá nhân. Không dùng ảnh placeholder để thay thế evidence.

| Evidence | Đường dẫn |
|---|---|
| Pytest cuối | 01-pytest.png |
| Log validator | 02-log-validator.png |
| Dashboard validator | 03-dashboard-validator.png |
| Structured log | 04-structured-log.png |
| PII redaction | 05-pii-redaction.png |
| Trace list | 06-trace-list.png |
| Trace waterfall | 07-trace-waterfall.png |
| Trace metadata | 08a-trace-metadata.png, 08b-generation-details.png |
| Prompt versions | 09-prompt-versions.png |
| Prompt rollback | 10a-prompt-v2-trace.png, 10b-prompt-rollback.png|
| Dashboard runtime | 11a-dashboard-overview-top, 11b-dashboard-overview-bottom |
| Incident metric | 12-incident-metric |
| Incident log | 13-incident-log |
| Incident trace | 14-incident-trace-waterfall |

## 3. Kết quả kỹ thuật

| Nội dung | Baseline | Kết quả cuối | Nhận xét |
|---|---|---|---|
| `validate_logs.py` | 0 | 100/100 | 89 records, 0 missing fields, 0 missing enrichment, 36 correlation IDs, 0 PII leaks |
| `validate_dashboard.py` | 6/6 panel | 6/6 | 6 panel trong dashboard contract đều oke |
| `pytest` | 21 passed, 1 failed | 22 pased | 22 passed in 5.01s |
| Số traces hợp lệ | -- | >= 10 | CCó root trace lab-agent-run trong langfuse |
| Số PII leak | 0 | 0 | Đã kiểm tra bằng validator và runtime evidence |
| Latency P95 / TTFT P95 | 0 | 100% | Không có retrieval failure trong dữ liệu dashboard |
| Retrieval success rate | 6 | 6/6 | Latency, Traffic, Errors, Cost, Tokens, Quality |


## 4. Logging và PII

- **Cách tạo/nhận và truyền correlation ID:** nhận từ x-request-id; nếu không hợp lệ thì hệ thống tự tạo ID mới
- **Các metadata được ghi vào structured log:** `user_id_hash, session_id, feature, model, env, correlation_id
- **Cách bảo đảm PII được scrub trước khi ghi:** được scrub trước khi ghi log
- **Cách kiểm chứng kết quả:** email, số điện thoại, CCCD và số thẻ

## 5. Tracing và prompt versioning

- **Cách xác nhận traces do chính tôi tạo trong project cá nhân:** Kiểm tra trong Langfuse project day13-k4-l3b-2A202602460, với root observation lab-agent-run và các trace có correlation_id của project.
- **Cấu trúc root/retrieval/generation observations:** lab-agent-run → retrieval + llm-generation
- **Cách nối trace với log:** Dùng chung correlation_id giữa log và trace
- **Prompt name:** day13-chat
- **Version/label baseline:** v1/production
- **Version/label candidate:** v2/candidate, sau đó save, promote lên production
- **Trace ID của mỗi version:** v1: 7b2fd78fe44946f561bf92ca33ce7f21, v2: f07977bb905bc5ecc8ae1c0c03fc8e72
- **Cách promote và rollback `production`:** Promote v2 lên production, kiểm tra trace, sau đó rollback production về v1

## 6. Dashboard, SLO và alerts

- **Dashboard và sáu panel:** đọc dữ liệu từ data/logs.jsonl
- **SLO và lý do chọn:** 99.5% request thành công và latency ≤ 3000 ms
- **Cách tính error budget:** 0.5%, tương đương tối đa 50 requests không đạt SLO trên 10,000 requests
- **Ba alert và runbook tương ứng:** HighLatencyP95, ElevatedErrorRate, LowRetrievalSuccess

> Ví dụ cách viết error budget: "SLO 99.5% trong 28 ngày nghĩa là error budget 0.5%. Nếu workload có 10,000 request thì tối đa 50 request được phép lỗi hoặc chậm hơn ngưỡng SLO."

## 7. Điều tra challenge

- **Challenge ID:** day13-k4-l3b-monitoring-llmops-v1
- **Khoảng thời gian điều tra:** Khi chạy workload sau khi bật incident rag_slow trong 30/09
- **Triệu chứng từ metrics:** Latency tăng lên khoảng 2.67–2.70s, vượt threshold 2000 ms
- **Log line và correlation ID liên quan:** response_sent, correlation_id=req-aa5dd8e3, latency 2668 ms
- **Trace ID và span gây ảnh hưởng:** Trace 605bd2de8d0d20f938912de5b9217acf; span retrieval mất khoảng 2.50s
- **Root cause:** Retrieval path bị chậm
- **Fix action:** Tắt incident và đưa hệ thống về trạng thái bình thường, sau đó kiểm tra lại bằng workload và validators
- **Preventive measure:** Theo dõi P95/P99, alert latency và retrieval success, dùng correlation_id để điều tra nhanh

> Gợi ý cách viết ngắn, không thay cho evidence thực tế: "Metric cho thấy `[latency/error/cost/quality]` bất thường trong `[khoảng thời gian]`. Log line `[event]` có `correlation_id=[...]` đại diện cho request bị ảnh hưởng. Trace cùng `correlation_id` cho thấy span `[retrieval/generation/prompt/tool]` có dấu hiệu `[chậm/lỗi/token tăng]`. Root cause là `[nguyên nhân suy ra từ evidence]`. Fix action là `[hành động khôi phục]`; preventive measure là `[alert/runbook/test/guardrail để ngăn tái diễn]`."

## 8. Giải thích và tự đánh giá

- **Một quyết định kỹ thuật quan trọng và lý do:** Sử dụng 1 correlation_id request, logs và traces giúp trace request cụ thể thay vì phải đoán từ nhiều nguồn dữ liệu
- **Một lỗi/blocker đã gặp:** một test không tương thích với Langfuse v4 Observation API. Sau khi sửa, toàn bộ test pass
- **Cách tìm nguyên nhân và xử lý:** Metrics → Logs → Traces
- **Cách hiểu luồng Metrics → Logs → Traces:** Metrics cho biết vấn đề, logs xác định request, traces xác định nguyên nhân cụ thể
- **Vai trò của prompt version, token/cost, SLO hoặc rollback trong vận hành LLM:**giúp biết production đang dùng prompt nào và hỗ trợ rollback
- **Điều quan trọng nhất đã học:** Có thể kết hợp Metrics rồi Logs đén Traces để tìm nguyên nhân của một incident thay vì chỉ nhìn vào một nguồn dữ liệu
- **Hạn chế hoặc phần chưa hoàn thành, nếu có:** Quality score hiện là proxy, chưa phải đánh giá chất lượng thủ công đầy đủ

## 9. Checklist trước khi nộp

- [x] Kết quả và evidence thuộc commit SHA cuối.
- [x] Tất cả ảnh/output mở được bằng đường dẫn tương đối.
- [x ] Incident evidence nối đúng metric → log → trace.
- [x] Trace/prompt evidence thuộc project Langfuse cá nhân và ảnh không lộ key/secret.
- [ x] Repository chạy lại được theo README.
- [x ] Không có secret, API key, PII thô hoặc evidence của người khác/lớp khác.
- [x] URL repo và commit SHA cuối đã được nộp trên LMS/Codelabs.
