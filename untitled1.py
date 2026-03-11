import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Abbies Irrigation Website",
    page_icon="💧",
    layout="wide"
)

# -----------------------
# Page style
# -----------------------
st.markdown("""
<style>

body {
    background-color:#f4f1ea;
}

.header {
    background-color:#8b6f47;
    padding:20px;
    border-radius:10px;
    color:white;
    text-align:center;
    font-size:32px;
    font-weight:bold;
}

.subtext {
    text-align:center;
    color:#333;
    margin-bottom:20px;
}

.metric-box {
    background:white;
    padding:15px;
    border-radius:10px;
    border:1px solid #ddd;
}

.section {
    background:white;
    padding:20px;
    border-radius:10px;
    margin-top:15px;
    border:1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header">💧 Abbies Irrigation Website</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Simple irrigation scheduling dashboard</div>', unsafe_allow_html=True)

# -----------------------
# Upload CSV
# -----------------------

st.subheader("Upload Weather Data")

uploaded_file = st.file_uploader("Upload irrigation CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Upload a CSV file to begin")
    st.stop()

# -----------------------
# Required columns
# -----------------------

required_columns = [
    "Year",
    "Month",
    "Date",
    "Temperature_High_F",
    "Temperature_Low_F",
    "Precipitation_inches",
    "ET_inches"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.stop()

# -----------------------
# Data cleanup
# -----------------------

df["Date"] = pd.to_datetime(
    df["Year"].astype(str) + "-" +
    df["Month"].astype(str) + "-" +
    df["Date"].astype(str)
)

df["Month_Name"] = df["Date"].dt.strftime("%B")
df["Day"] = df["Date"].dt.day

df["Temp_Avg"] = (df["Temperature_High_F"] + df["Temperature_Low_F"]) / 2

df["Precip_Cum"] = df["Precipitation_inches"].cumsum()
df["ET_Cum"] = df["ET_inches"].cumsum()

# -----------------------
# Irrigation logic
# -----------------------

MAD = 1.0
max_irrigation = 1.0

df["Irrigation_daily"] = 0.0
df["Irrigation_Cum"] = 0.0

deficit = 0

for i in range(len(df)):

    deficit += df.loc[i,"ET_inches"] - df.loc[i,"Precipitation_inches"]

    if deficit > MAD:

        irrigation = min(deficit, max_irrigation)

        df.loc[i,"Irrigation_daily"] = irrigation

        deficit -= irrigation

    if i > 0:
        df.loc[i,"Irrigation_Cum"] = df.loc[i-1,"Irrigation_Cum"] + df.loc[i,"Irrigation_daily"]
    else:
        df.loc[i,"Irrigation_Cum"] = df.loc[i,"Irrigation_daily"]

df["Water_Cum"] = df["Precip_Cum"] + df["Irrigation_Cum"]

# -----------------------
# Sidebar filters
# -----------------------

st.sidebar.header("Controls")

month = st.sidebar.selectbox(
    "Select Month",
    df["Month_Name"].unique()
)

month_df = df[df["Month_Name"] == month]

day = st.sidebar.selectbox(
    "Select Day",
    month_df["Day"].unique()
)

day_data = month_df[month_df["Day"] == day].iloc[0]

# -----------------------
# Summary
# -----------------------

col1,col2,col3,col4 = st.columns(4)

col1.metric("Date",f"{month} {day}")
col2.metric("ET",f"{day_data['ET_inches']:.2f} in")
col3.metric("Rain",f"{day_data['Precipitation_inches']:.2f} in")
col4.metric("Irrigation",f"{day_data['Irrigation_daily']:.2f} in")

# -----------------------
# Recommendation
# -----------------------

st.markdown('<div class="section">', unsafe_allow_html=True)

st.subheader("Irrigation Recommendation")

if day_data["Irrigation_daily"] > 0:

    st.success(
        f"Apply {day_data['Irrigation_daily']:.2f} inches of irrigation."
    )

else:

    st.info(
        "No irrigation required today."
    )

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------
# Graphs
# -----------------------

with st.expander("Weather + ET Trends"):

    fig,ax = plt.subplots()

    ax.bar(df.index, df["Precipitation_inches"], label="Rain")
    ax.plot(df.index, df["ET_inches"], label="ET")

    ax.set_ylabel("Inches")
    ax.legend()

    st.pyplot(fig)

with st.expander("Water Supply vs ET"):

    fig2,ax2 = plt.subplots()

    ax2.plot(df.index, df["Water_Cum"], label="Rain + Irrigation")
    ax2.plot(df.index, df["ET_Cum"], label="Cumulative ET")

    ax2.legend()

    st.pyplot(fig2)

# -----------------------
# Data table
# -----------------------

with st.expander("View Data Table"):

    st.dataframe(df)
