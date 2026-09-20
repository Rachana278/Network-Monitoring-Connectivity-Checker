import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Network Monitoring Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Network Monitoring Dashboard")
st.write("Real-time network connectivity and performance monitoring")

df = pd.read_csv("network_log.csv")

# Dashboard metrics
total_checks = len(df)
hosts_up = len(df[df["Status"] == "UP"])
hosts_down = len(df[df["Status"] == "DOWN"])

col1, col2, col3 = st.columns(3)

col1.metric("Total Checks", total_checks)
col2.metric("Hosts UP", hosts_up)
col3.metric("Hosts DOWN", hosts_down)

st.subheader("Network Monitoring Data")

st.dataframe(df, width="stretch")

st.subheader("📊 Latency Trend by Host")

latency_data = df[df["Status"] == "UP"].copy()

latency_data["Latency"] = pd.to_numeric(
    latency_data["Latency"],
    errors="coerce"
)

latency_data["Timestamp"] = pd.to_datetime(
    latency_data["Timestamp"]
)

latency_data = latency_data.dropna(subset=["Latency"])

st.line_chart(
    latency_data,
    x="Timestamp",
    y="Latency",
    color="Host"
)

st.subheader("📉 Packet Loss by Host")

packet_data = df[df["Status"] == "UP"].copy()

packet_data["Packet Loss"] = pd.to_numeric(
    packet_data["Packet Loss"],
    errors="coerce"
)

packet_data["Timestamp"] = pd.to_datetime(
    packet_data["Timestamp"]
)

packet_data = packet_data.dropna(subset=["Packet Loss"])

st.line_chart(
    packet_data,
    x="Timestamp",
    y="Packet Loss",
    color="Host"
)