import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Abbies Irrigation Website",
    page_icon="🌻",
    layout="wide"
)

# ---------- Title ----------
st.title("🌻 Abbies Irrigation Website 💧")
st.write("Upload weather data to get irrigation recommendations.")

# ---------- Upload CSV ----------
uploaded_file = st.file_uploader("Upload irrigation CSV", type=["csv"])

if uploaded_file is None:
    st.info("Please upload a CSV file to begin.")
    st.stop()

df = pd.read_csv(uploaded_file)

# ---------- Data Preparation ----------
df["Date_full"] = pd.to_datetime(
    df["Year"].astype(str) + "-" +
    df["Month"].astype(str) + "-" +
    df["Date"].astype(str),
    errors="coerce"
)

df["Temp_Avg"] = (df["Temperature_High_F"] + df["Temperature_Low_F"]) / 2

df["Precip_Cum"] = df["Precipitation_inches"].cumsum()
df["ET_Cum"] = df["ET_inches"].cumsum()

# ---------- Irrigation Logic ----------
MAD = 1.0
max_irrigation = 1.0

df["Irrigation_daily"] = 0
df["Irrigation_Cum"] = 0

deficit = 0

for i in range(len(df)):

    deficit += df.loc[i, "ET_inches"] - df.loc[i, "Precipitation_inches"]

    if deficit > MAD:

        irrigation = min(deficit, max_irrigation)

        df.loc[i, "Irrigation_daily"] = irrigation

        deficit -= irrigation

    if i > 0:
        df.loc[i, "Irrigation_Cum"] = df.loc[i-1, "Irrigation_Cum"] + df.loc[i, "Irrigation_daily"]
    else:
        df.loc[i, "Irrigation_Cum"] = df.loc[i, "Irrigation_daily"]

df["Water_Cum"] = df["Precip_Cum"] + df["Irrigation_Cum"]

# ---------- Sidebar Controls ----------
st.sidebar.header("Dashboard Controls")

month = st.sidebar.selectbox(
    "Select Month",
    df["Month"].unique()
)

month_df = df[df["Month"] == month]

day = st.sidebar.selectbox(
    "Select Day",
    month_df["Date"].unique()
)

day_data = month_df[month_df["Date"] == day].iloc[0]

# ---------- Metrics ----------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Day", day)
col2.metric("ET", f"{day_data['ET_inches']:.2f} in")
col3.metric("Rain", f"{day_data['Precipitation_inches']:.2f} in")
col4.metric("Irrigation", f"{day_data['Irrigation_daily']:.2f} in")

# ---------- Recommendation ----------
st.subheader("Irrigation Recommendation")

if day_data["Irrigation_daily"] > 0:
    st.success(f"Apply {day_data['Irrigation_daily']:.2f} inches of irrigation today.")
else:
    st.info("No irrigation needed today.")

# ---------- Graph 1 ----------
st.subheader("Daily Rain vs ET")

fig, ax = plt.subplots()

ax.bar(df.index, df["Precipitation_inches"], label="Rain")
ax.plot(df.index, df["ET_inches"], label="ET")

ax.legend()

st.pyplot(fig)

# ---------- Graph 2 ----------
st.subheader("Cumulative Water Balance")

fig2, ax2 = plt.subplots()

ax2.plot(df.index, df["Water_Cum"], label="Rain + Irrigation")
ax2.plot(df.index, df["ET_Cum"], label="Cumulative ET")

ax2.legend()

st.pyplot(fig2)

# ---------- Data Table ----------
st.subheader("Dataset")

st.dataframe(df)
