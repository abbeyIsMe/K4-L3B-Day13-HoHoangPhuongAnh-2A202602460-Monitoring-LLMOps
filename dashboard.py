import json
from pathlib import Path

import pandas as pd
import streamlit as st


LOG_FILE = Path("data/logs.jsonl")


def load_logs():
    records = []

    with LOG_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    return pd.DataFrame(records)
st.set_page_config(
    page_title="K4-L3B Day 13 Monitoring & LLMOps",
    layout="wide",
)

st.title("K4-L3B Day 13 Monitoring & LLMOps")
st.caption("Monitoring dashboard — data source: data/logs.jsonl")

df = load_logs()

if df.empty:
    st.warning("No log data found.")
    st.stop()

df["timestamp"] = pd.to_datetime(df["ts"], utc=True)

# Default time range: last 60 minutes
latest_time = df["timestamp"].max()
start_time = latest_time - pd.Timedelta(minutes=60)

df = df[df["timestamp"] >= start_time].copy()

st.info(
    f"Time range: {start_time.strftime('%Y-%m-%d %H:%M UTC')} "
    f"→ {latest_time.strftime('%Y-%m-%d %H:%M UTC')} | "
    "Refresh: 30 seconds"
)
st.subheader("1. Latency percentiles and TTFT")

response_logs = df[df["event"] == "response_sent"].copy()

if not response_logs.empty:
    latency_p50 = response_logs["latency_ms"].quantile(0.50)
    latency_p95 = response_logs["latency_ms"].quantile(0.95)
    latency_p99 = response_logs["latency_ms"].quantile(0.99)
    ttft_p95 = response_logs["ttft_ms"].quantile(0.95)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("P50 Latency", f"{latency_p50:.0f} ms")
    col2.metric("P95 Latency", f"{latency_p95:.0f} ms")
    col3.metric("P99 Latency", f"{latency_p99:.0f} ms")
    col4.metric("TTFT P95", f"{ttft_p95:.0f} ms")

    latency_chart = pd.DataFrame(
        {
            "Percentile": ["P50", "P95", "P99"],
            "Latency (ms)": [
                latency_p50,
                latency_p95,
                latency_p99,
            ],
        }
    ).set_index("Percentile")

    st.bar_chart(latency_chart)

    st.caption("SLO threshold: P95 latency ≤ 3000 ms")
else:
    st.warning("No response_sent data in the selected time range.")
st.subheader("2. Request traffic")

request_logs = df[df["event"] == "request_received"].copy()

if not request_logs.empty:
    request_count = len(request_logs)
    rate_per_minute = request_count / 60

    col1, col2 = st.columns(2)

    col1.metric("Total Requests", request_count)
    col2.metric("Requests / Minute", f"{rate_per_minute:.2f}")

    traffic_by_minute = (
        request_logs
        .set_index("timestamp")
        .resample("1min")
        .size()
        .rename("Requests")
    )

    st.line_chart(traffic_by_minute)

    st.caption("SLO threshold: request rate ≥ 1 request/minute")
else:
    st.warning("No request_received data in the selected time range.")

st.subheader("3. Error rate and retrieval success")

received = df[df["event"] == "request_received"]
failed = df[df["event"] == "request_failed"]

if not received.empty:
    error_rate = (len(failed) / len(received)) * 100

    tool_logs = df[df["tool_success"].notna()].copy()

    if not tool_logs.empty:
        retrieval_success = (
            tool_logs["tool_success"].astype(bool).mean() * 100
        )
    else:
        retrieval_success = 0

    col1, col2 = st.columns(2)

    col1.metric("Error Rate", f"{error_rate:.2f}%")
    col2.metric("Retrieval Success", f"{retrieval_success:.2f}%")

    if not failed.empty and "error_type" in failed.columns:
        error_breakdown = (
            failed["error_type"]
            .fillna("unknown")
            .value_counts()
            .rename("Errors")
        )

        st.write("Error breakdown")
        st.bar_chart(error_breakdown)

    st.caption("SLO threshold: error rate ≤ 2%")
else:
    st.warning("No request_received data in the selected time range.")
st.subheader("4. Cost over time")

cost_logs = df[df["event"] == "response_sent"].copy()

if not cost_logs.empty:
    total_cost = cost_logs["cost_usd"].sum()

    st.metric("Total Cost", f"${total_cost:.4f}")

    cost_by_minute = (
        cost_logs
        .set_index("timestamp")["cost_usd"]
        .resample("1min")
        .sum()
        .rename("Cost (USD)")
    )

    st.line_chart(cost_by_minute)

    st.caption("SLO threshold: total cost ≤ $2.50")
else:
    st.warning("No response_sent data in the selected time range.")
st.subheader("5. Input and output tokens")

token_logs = df[df["event"] == "response_sent"].copy()

if not token_logs.empty:
    total_input = token_logs["tokens_in"].sum()
    total_output = token_logs["tokens_out"].sum()

    col1, col2 = st.columns(2)

    col1.metric("Input Tokens", f"{total_input:,.0f}")
    col2.metric("Output Tokens", f"{total_output:,.0f}")

    token_chart = pd.DataFrame(
        {
            "Token Type": ["Input", "Output"],
            "Tokens": [total_input, total_output],
        }
    ).set_index("Token Type")

    st.bar_chart(token_chart)

    st.caption("SLO threshold: total tokens ≤ 50,000")
else:
    st.warning("No response_sent data in the selected time range.")
st.subheader("6. Quality proxy")

quality_logs = df[df["event"] == "response_sent"].copy()

if not quality_logs.empty:
    quality_mean = quality_logs["quality_score"].mean()

    st.metric("Average Quality Score", f"{quality_mean:.2f}")

    quality_chart = (
        quality_logs
        .set_index("timestamp")["quality_score"]
        .rename("Quality Score")
    )

    st.line_chart(quality_chart)

    st.caption("SLO threshold: quality score ≥ 0.75")
else:
    st.warning("No response_sent data in the selected time range.")
