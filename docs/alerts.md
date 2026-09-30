# Template Alert và Runbook

Mỗi alert phải dựa trên triệu chứng người dùng hoặc SLO, không dựa trực tiếp vào tên implementation nội bộ.

## Alert mẫu để tham khảo

Ví dụ dưới đây minh họa mức độ cụ thể cần có. Học viên không cần copy nguyên, nhưng ba alert trong bài nộp nên rõ ràng tương tự: điều kiện là gì, kéo dài bao lâu, ảnh hưởng tới user ra sao và người trực cần kiểm tra gì trước.

- Tên: `HighLatencyP95`
- Severity: `warning`
- Duration: `5m`
- Kênh thông báo: Slack `#k4-l3b-alerts`
- SLI/SLO liên quan: latency P95 của `response_sent.latency_ms`
- Điều kiện và thời gian duy trì: `p95(latency_ms) > 3000ms` trong 5 phút
- Ảnh hưởng tới người dùng: người dùng phải chờ lâu hơn trước khi nhận câu trả lời
- Ba bước kiểm tra đầu tiên:
  1. Mở dashboard latency để xác nhận P95/P99 và khoảng thời gian tăng.
  2. Lọc `data/logs.jsonl` trong khoảng đó, lấy một `correlation_id` có `latency_ms` cao.
  3. Mở trace cùng `correlation_id` trên Langfuse, so sánh các span chính để xác định bước nào bất thường.
- Mitigation tạm thời: dựa trên evidence thực tế để rollback prompt, khôi phục cấu hình liên quan, tắt practice scenario hoặc giảm tải khi demo.
- Owner: `student-<MSSV>`

## Alert 1 — HighLatencyP95

- Severity: warning; duy trì 5 phút; Slack `#k4-l3b-alerts`; owner `student-oncall`.
- Điều kiện: P95 `response_sent.latency_ms` > 3000 ms trong 5 phút.
- Ảnh hưởng: người dùng đợi lâu hơn trước khi nhận câu trả lời.
- Kiểm tra: xác nhận P95/P99 theo time range; lọc log để lấy correlation ID chậm; mở trace tương ứng và so sánh retrieval/generation.
- Mitigation: rollback prompt nếu generation tăng bất thường; nếu retrieval chậm, khôi phục cấu hình nguồn dữ liệu theo evidence.

## Alert 2 — ElevatedErrorRate

- Severity: critical; duy trì 3 phút; Slack `#k4-l3b-alerts`; owner `student-oncall`.
- Điều kiện: tỷ lệ `request_failed / request_received` > 2% trong 3 phút.
- Ảnh hưởng: một phần request không trả được câu trả lời.
- Kiểm tra: xác nhận error rate và error type; lấy correlation ID từ `request_failed`; mở trace để xem span lỗi đầu tiên.
- Mitigation: khôi phục thành phần/cấu hình lỗi đã xác định; nếu lỗi retrieval diện rộng, tạm dùng fallback theo quy trình vận hành.

## Alert 3 — LowRetrievalSuccess

- Severity: warning; duy trì 5 phút; Slack `#k4-l3b-alerts`; owner `student-oncall`.
- Điều kiện: tỷ lệ `tool_success` của retrieval < 90% trong 5 phút.
- Ảnh hưởng: câu trả lời có thể thiếu ngữ cảnh phù hợp.
- Kiểm tra: xem panel errors/retrieval; lọc log theo `tool_name=retrieval`; mở trace và kiểm tra retrieval span.
- Mitigation: khôi phục nguồn/config retrieval đã biết là tốt; theo dõi retrieval success trước khi đóng incident.
