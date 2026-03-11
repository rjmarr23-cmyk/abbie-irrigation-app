import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Abbies Irrigation Website",
    layout="wide"
)

# --------------------------
# Custom Styling
# --------------------------

st.markdown("""
<style>

.main-title {
    text-align:center;
    font-size:40px;
    color:#2f6f3e;
    font-weight:bold;
}

.banner {
    background:#2f6f3e;
    color:white;
    padding:15px;
    border-radius:10px;
    text-align:center;
    font-size:22px;
}

.card {
    background:#f7fbf7;
    padding:15px;
    border-radius:10px;
    border:1px solid #ddd;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌱 Abbies Irrigation Website</div>', unsafe_allow_html=True)

st.write("Upload your weather data and receive irrigation recommendations.")

# --------------------------
# Upload CSV
# --------------------------

uploaded_file = st.file_uploader("Upload irrigation CSV", type=["csv"])

if uploaded_file is None:
    st.warning("Please upload a CSV file to begin.")
    st.stop()

df = pd.read_csv(uploaded_file)

# --------------------------
# Data preparation
# --------------------------

df["Date"] = pd.to_datetime(
    df["Year"].astype(str) + "-" +
    df["Month"].astype(str) + "-" +
    df["Date"].astype(str)
)

df["Temp_Avg"] = (df["Temperature_High_F"] + df["Temperature_Low_F"]) / 2

df["Precip_Cum"] = df["Precipitation_inches"].cumsum()
df["ET_Cum"] = df["ET_inches"].cumsum()

# --------------------------
# Irrigation logic
# --------------------------

MAD = 1.0
max_irrigation = 1.0

df["Irrigation_daily"] = 0
df["Irrigation_Cum"] = 0

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

# --------------------------
# Sidebar
# --------------------------

st.sidebar.header("Control Panel")

month = st.sidebar.selectbox(
    "Select Month",
    df["Month"].unique()
)

month_df = df[df["Month"] == month]

day = st.sidebar.selectbox(
    "Select Day",
    month_df["Date"].dt.day.unique()
)

day_data = month_df[month_df["Date"].dt.day == day].iloc[0]

# --------------------------
# Weather summary
# --------------------------

col1,col2,col3 = st.columns(3)

col1.metric("ET (inches)", round(day_data["ET_inches"],2))
col2.metric("Rain (inches)", round(day_data["Precipitation_inches"],2))
col3.metric("Average Temp", round(day_data["Temp_Avg"],1))

# --------------------------
# Recommendation banner
# --------------------------

if day_data["Irrigation_daily"] > 0:

    st.markdown(
        f'<div class="banner">Apply {day_data["Irrigation_daily"]:.2f} inches of irrigation today</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div class="banner">No irrigation needed today</div>',
        unsafe_allow_html=True
    )

# --------------------------
# Graph 1
# --------------------------

st.subheader("Daily Rain vs ET")

fig, ax = plt.subplots()

ax.bar(df.index, df["Precipitation_inches"], label="Rain")
ax.plot(df.index, df["ET_inches"], label="ET")

ax.legend()

st.pyplot(fig)

# --------------------------
# Graph 2
# --------------------------

st.subheader("Cumulative Water Balance")

fig2, ax2 = plt.subplots()

ax2.plot(df.index, df["Water_Cum"], label="Rain + Irrigation")
ax2.plot(df.index, df["ET_Cum"], label="Cumulative ET")

ax2.legend()

st.pyplot(fig2)

# --------------------------
# Data Table
# --------------------------

st.subheader("Dataset")

st.dataframe(df)
