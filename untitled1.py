import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Abbies Irrigation Website",
    page_icon="🌈",
    layout="wide"
)

# --------------------------
# Custom styling
# --------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom, #fdf6ec, #eef8f0);
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 800;
    color: #2e6f40;
    margin-bottom: 0.2rem;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 1.5rem;
}

.pretty-box {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 1rem;
}

.rec-good {
    background: linear-gradient(90deg, #86efac, #d9f99d);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #14532d;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.rec-warn {
    background: linear-gradient(90deg, #67e8f9, #bfdbfe);
    padding: 18px;
    border-radius: 18px;
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: #1e3a8a;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.small-note {
    text-align: center;
    color: #4b5563;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌻 Abbies Irrigation Website 💧</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A fun little dashboard for checking rainfall, ET, and irrigation needs</div>', unsafe_allow_html=True)

# --------------------------
# Upload CSV
# --------------------------
st.markdown('<div class="pretty-box">', unsafe_allow_html=True)
st.subheader("📂 Upload Your Irrigation File")
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_fil_
