import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Cooling Tower AI", layout="centered")

# ===== TITLE =====
st.markdown("""
<h2 style='text-align: center; color: #00C9A7;'>
⚙️ Cooling Tower Gear Temp AI Predictor
</h2>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ===== INPUTS =====
st.subheader("Enter Parameters")

load = st.slider("Load", 50, 100)
temp = st.slider("Ambient Temperature", 25, 50)
rpm = st.slider("RPM", 1200, 1800)
oil = st.slider("Oil Condition", 40, 100)

# ===== PREDICTION =====
if st.button("Predict Temperature"):
    result = model.predict([[load, temp, rpm, oil]])
    st.success(f"Predicted Temperature: {result[0]:.2f} °C")

# ===== FOOTER =====
st.markdown("""
<hr>
<p style='text-align:center; font-size:12px; color:gray;'>
Built with AI | Mobile Friendly Version
</p>
""", unsafe_allow_html=True)
