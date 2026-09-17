from __future__ import annotations

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="FinGuard", page_icon="F", layout="wide", initial_sidebar_state="expanded")

try:
    from finguard.data import build_demo_data
    from finguard.graph import build_identity_graph, graph_plot_data, shared_identity_summary
    from finguard.risk import explain_transaction, score_transactions
except Exception as error:
    st.error("FinGuard could not load its analysis modules.")
    st.code(f"{type(error).__name__}: {error}")
    st.info("Check that the dependencies in requirements.txt are installed, then restart the Streamlit app.")
    st.stop()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root { --ink:#10231d; --muted:#52635b; --mint:#b9ed4b; --paper:#eef2eb; --line:#cbd7cc; --red:#c83d35; --cream:#ffffff; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; color: var(--ink) !important; }
.stApp { background: radial-gradient(circle at 90% 0%, #dcebc9 0, var(--paper) 34rem); }
[data-testid="stAppViewContainer"] { color:var(--ink); }
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li, [data-testid="stMarkdownContainer"] span { color:var(--ink); }
[data-testid="stCaptionContainer"] p { color:var(--muted) !important; }
[data-testid="stMetric"] { color:var(--ink) !important; min-width:0; }
[data-testid="stSidebar"] { background: #18231f; }
[data-testid="stSidebar"] * { color: #f4f5ef !important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color:#aabbb0 !important; }
[data-testid="stSidebar"] [data-testid="stRadio"] label { padding:9px 10px; border-radius:6px; }
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:#26352f; }
[data-testid="stMetric"] { background:var(--cream); border:1px solid var(--line); border-radius:8px; padding:18px; box-shadow:0 6px 20px rgba(21,32,29,.04); }
[data-testid="stMetricLabel"] { color:var(--muted) !important; }
[data-testid="stMetricValue"] { color:var(--ink) !important; font-family:'Space Mono', monospace; font-size:1.6rem; white-space:nowrap; }
.alert { background:#18231f; color:#f4f5ef; border-left:5px solid var(--mint); padding:18px 20px; border-radius:7px; margin:10px 0 20px; }
.alert strong { color:var(--mint); font-family:'Space Mono', monospace; }
.risk-high { color:#d94b3e; font-weight:700; }
.mono { font-family:'Space Mono', monospace; }
.eyebrow { color:#718077; font-family:'Space Mono', monospace; font-size:.72rem; letter-spacing:.08em; text-transform:uppercase; }
.page-lead { max-width:820px; margin:0 0 16px; }
.page-lead h1 { font-size:clamp(2rem, 3.5vw, 3rem); letter-spacing:-.03em; margin:.2rem 0 .35rem; }
.page-lead p { color:var(--muted); font-size:1rem; margin-bottom:.4rem; }
.section-kicker { border-top:1px solid var(--line); padding-top:18px; margin-top:28px; }
.control-bar { margin:0 0 20px; }
.control-bar label, .control-bar p { color:var(--ink) !important; }
.stSelectbox label, .stSlider label { color:var(--ink) !important; font-weight:700; }
.stSelectbox [data-baseweb="select"] > div { background:#ffffff; color:var(--ink); border-color:#9db48e; }
.stSelectbox [data-baseweb="select"] span { color:var(--ink) !important; }
.stButton > button { border:1px solid #9db48e; color:var(--ink) !important; background:#ffffff; font-weight:700; }
.stButton > button p, .stButton > button span { color:var(--ink) !important; }
.stButton > button:hover { border-color:#10231d; color:#10231d !important; background:#dff1c4; }
.stButton > button:hover p, .stButton > button:hover span { color:#10231d !important; }
[data-testid="stSidebar"] .stButton > button { color:#10231d !important; background:#b9ed4b; border-color:#b9ed4b; }
[data-testid="stSidebar"] .stButton > button p, [data-testid="stSidebar"] .stButton > button span { color:#10231d !important; }
[data-testid="stSidebar"] .stButton > button:hover { background:#d8f79a; border-color:#d8f79a; }
[data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:8px; }
</style>
""", unsafe_allow_html=True)

if "transactions" not in st.session_state:
    try:
        st.session_state.transactions = score_transactions(build_demo_data())
    except Exception as error:
        st.error("FinGuard could not generate the demo transaction stream.")
        st.code(f"{type(error).__name__}: {error}")
        st.info("Reload the app after confirming the installed pandas and numpy versions.")
        st.stop()
data = st.session_state.transactions

if "risk_floor" not in st.session_state:
    st.session_state.risk_floor = 0

with st.sidebar:
    st.markdown("# FINGUARD")
    st.caption("Financial risk operations")
    st.divider()
    page = st.radio("Workspace", ["Overview", "Investigations", "Identity network", "Data observatory"], label_visibility="collapsed")
    st.divider()
    st.markdown("**Data sources**")
    for source in data["source"].unique():
        st.caption(f"{source}  ·  {int((data['source'] == source).sum()):,} records")
    if st.button("Replay transaction stream", use_container_width=True):
        st.session_state.transactions = score_transactions(build_demo_data(seed=st.session_state.get("seed", 42) + 1))
        st.session_state.seed = st.session_state.get("seed", 42) + 1
        st.rerun()

st.markdown('<div class="page-lead"><div class="eyebrow">FinGuard / live environment</div><h1>See the signal before it becomes a loss.</h1><p>Multi-source transaction monitoring with behavioral context, explainable risk, and identity investigation.</p></div>', unsafe_allow_html=True)

if page == "Overview":
    st.markdown('<div class="control-bar">', unsafe_allow_html=True)
    filter_left, filter_right = st.columns([1, 1])
    with filter_left:
        source_filter = st.selectbox("Focus source", ["All sources", *sorted(data["source"].unique())], label_visibility="visible")
    with filter_right:
        risk_floor = st.slider("Minimum risk", 0, 90, st.session_state.risk_floor, 10)
    st.markdown('</div>', unsafe_allow_html=True)
    view_data = data[(data["risk_score"] >= risk_floor) & ((data["source"] == source_filter) if source_filter != "All sources" else True)]
    critical = int((data["risk_score"] >= 80).sum())
    suspicious = int((data["risk_score"] >= 60).sum())
    amount_at_risk = data.loc[data["risk_score"] >= 60, "amount"].sum()
    networks = len(shared_identity_summary(data))
    cols = st.columns(4)
    cols[0].metric("Transactions analyzed", f"{len(data):,}")
    cols[1].metric("Suspicious transactions", f"{suspicious:,}")
    cols[2].metric("Critical alerts", f"{critical:,}")
    cols[3].metric("Amount at risk", f"₹{amount_at_risk/100000:.1f}L")
    st.markdown(f'<div class="alert"><strong>LIVE MONITOR</strong> &nbsp; {critical} critical alerts require investigation across {networks} shared-identity links.</div>', unsafe_allow_html=True)
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown('<div class="section-kicker"><div class="eyebrow">01 / operating picture</div><h3>Risk distribution</h3></div>', unsafe_allow_html=True)
        distribution = view_data["risk_level"].value_counts().rename_axis("risk_level").reset_index(name="transactions")
        risk_figure = px.bar(distribution, x="risk_level", y="transactions", color="risk_level", color_discrete_map={"LOW":"#9bcf66", "MEDIUM":"#f1c75b", "HIGH":"#e98957", "CRITICAL":"#d94b3e"})
        risk_figure.update_layout(height=270, margin={"l": 0, "r": 0, "t": 8, "b": 0})
        st.plotly_chart(risk_figure, use_container_width=True, config={"displayModeBar": False})
    with right:
        st.subheader("Source mix")
        source_mix = view_data["source"].value_counts().rename_axis("source").reset_index(name="transactions")
        source_figure = px.pie(source_mix, names="source", values="transactions", hole=.58, color_discrete_sequence=["#18231f", "#64756d", "#a7b6a1", "#d2ddc9", "#c8f169"])
        source_figure.update_layout(height=270, margin={"l": 0, "r": 0, "t": 8, "b": 0}, legend={"font": {"size": 10}})
        st.plotly_chart(source_figure, use_container_width=True, config={"displayModeBar": False})
    st.markdown('<div class="section-kicker"><div class="eyebrow">02 / incoming stream</div><h3>Live transaction feed</h3></div>', unsafe_allow_html=True)
    feed = view_data[["timestamp", "transaction_id", "source", "user_id", "amount", "risk_score", "risk_level", "status"]].head(14).copy()
    feed["timestamp"] = feed["timestamp"].dt.strftime("%H:%M:%S")
    feed["amount"] = feed["amount"].map(lambda value: f"₹{value:,.0f}")
    st.dataframe(feed, use_container_width=True, hide_index=True, column_config={"risk_score": st.column_config.ProgressColumn("Risk", min_value=0, max_value=100, format="%d")})

elif page == "Investigations":
    st.markdown('<div class="eyebrow">01 / case management</div><h2>Investigation queue</h2>', unsafe_allow_html=True)
    queue = data[data["risk_score"] >= 60].sort_values("risk_score", ascending=False)
    selected_id = st.selectbox("Select transaction", queue["transaction_id"].tolist(), label_visibility="collapsed")
    selected = queue[queue["transaction_id"] == selected_id].iloc[0]
    left, right = st.columns([1, 1.25])
    with left:
        st.markdown(f"### `{selected['transaction_id']}`")
        st.metric("Risk score", f"{selected['risk_score']}/100", selected["risk_level"])
        st.markdown(f"**{selected['status']}**  ·  {selected['source']}")
        st.markdown(f"**Amount**  ₹{selected['amount']:,.2f}")
        st.markdown(f"**User**  `{selected['user_id']}`  ·  **Time**  {selected['timestamp']:%d %b %H:%M}")
        st.markdown(f"**Location**  {selected['location']}  ·  **Device**  `{selected['device_id']}`")
        st.markdown(f"<div class='alert'>{selected['explanation']}</div>", unsafe_allow_html=True)
    with right:
        st.markdown("### Why this was flagged")
        for signal in explain_transaction(selected):
            color = {"high":"#d94b3e", "medium":"#cf9b18", "low":"#6a8f67"}[signal["severity"]]
            st.markdown(f"<div style='border-bottom:1px solid #dfe3d9;padding:12px 0'><b>{signal['name']}</b><span style='float:right;color:{color}'>{signal['detail']}</span></div>", unsafe_allow_html=True)
        history = data[data["user_id"] == selected["user_id"]].sort_values("timestamp").tail(12)
        st.markdown("### User transaction history")
        st.plotly_chart(px.scatter(history, x="timestamp", y="amount", color="risk_level", size="risk_score", hover_data=["merchant_id", "location"]), use_container_width=True, config={"displayModeBar": False})

elif page == "Identity network":
    st.markdown('<div class="eyebrow">01 / relationship analysis</div><h2>Identity network</h2>', unsafe_allow_html=True)
    shared = shared_identity_summary(data)
    st.caption("Shared devices are used as an investigation pivot. This is a prototype graph signal, not proof of coordinated fraud.")
    if shared.empty:
        st.info("No shared identities in the current stream.")
    else:
        device = st.selectbox("Shared device", shared["device_id"].tolist(), label_visibility="collapsed")
        pivot = data[data["device_id"] == device]
        graph = build_identity_graph(pivot)
        st.metric("Accounts linked", f"{pivot['user_id'].nunique()}")
        st.dataframe(pivot[["user_id", "device_id", "merchant_id", "amount", "risk_score", "risk_level"]], use_container_width=True, hide_index=True)
        nodes, edges = graph_plot_data(graph)
        figure = go.Figure()
        for edge in edges.itertuples(index=False):
            figure.add_trace(go.Scatter(x=edge.x, y=edge.y, mode="lines", line={"color": "#c9d2c5", "width": 1}, hoverinfo="skip", showlegend=False))
        colors = {"user": "#18231f", "device": "#c8f169", "merchant": "#e98957"}
        for kind, group in nodes.groupby("type"):
            figure.add_trace(go.Scatter(
                x=group["x"], y=group["y"], mode="markers+text", text=group["label"], textposition="top center",
                name=kind.title(), marker={"size": 16, "color": colors[kind], "line": {"color": "#18231f", "width": 1}},
                hovertemplate="%{text}<extra>" + kind.title() + "</extra>",
            ))
        figure.update_layout(height=460, margin={"l": 0, "r": 0, "t": 10, "b": 0}, plot_bgcolor="#f4f5ef", paper_bgcolor="#f4f5ef", xaxis={"visible": False}, yaxis={"visible": False}, legend={"orientation": "h"})
        st.plotly_chart(figure, use_container_width=True, config={"displayModeBar": False})
        st.caption(f"Graph contains {graph.number_of_nodes()} identity nodes and {graph.number_of_edges()} relationships for `{device}`.")

else:
    st.markdown('<div class="eyebrow">01 / data inventory</div><h2>Data observatory</h2>', unsafe_allow_html=True)
    st.caption("A source-aware view of the synthetic multi-dataset layer powering this prototype.")
    source_summary = data.groupby("source").agg(
        records=("transaction_id", "count"),
        suspicious=("risk_score", lambda values: int((values >= 60).sum())),
        average_amount=("amount", "mean"),
        fraud_labels=("is_fraud", "sum"),
    ).reset_index().sort_values("records", ascending=False)
    cols = st.columns(3)
    cols[0].metric("Source profiles", len(source_summary))
    cols[1].metric("Records in stream", f"{len(data):,}")
    cols[2].metric("Fraud labels", f"{int(data['is_fraud'].sum()):,}")
    st.markdown('<div class="section-kicker"><div class="eyebrow">02 / source health</div><h3>Unified transaction layer</h3></div>', unsafe_allow_html=True)
    display = source_summary.copy()
    display["average_amount"] = display["average_amount"].map(lambda value: f"₹{value:,.0f}")
    st.dataframe(display, use_container_width=True, hide_index=True, column_config={"records": "Records", "suspicious": "Suspicious", "average_amount": "Average amount", "fraud_labels": "Synthetic fraud labels"})
    st.markdown('<div class="section-kicker"><div class="eyebrow">03 / volume by source</div><h3>Where the stream comes from</h3></div>', unsafe_allow_html=True)
    st.plotly_chart(px.bar(source_summary, x="source", y="records", color="suspicious", color_continuous_scale=["#dfe8d7", "#18231f"]), use_container_width=True, config={"displayModeBar": False})
