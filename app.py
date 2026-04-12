import streamlit as st
import pandas as pd
import base64
from sklearn.linear_model import LinearRegression

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Cooling Tower AI", layout="centered")

# ===== BACKGROUND IMAGE =====
def set_bg():
    with open("bg.jpg", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    /* Make content readable */
    [data-testid="stHeader"], .stToolbar {{
        background: transparent;
    }}

    .stApp {{
        background-color: rgba(0,0,0,0.4);
    }}
    </style>
    """, unsafe_allow_html=True)

# 👉 CALL FUNCTION
set_bg()

# ===== LOAD DATA =====
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ===== UI =====
st.title("⚙️ Cooling Tower AI Predictor")

st.sidebar.header("Input Parameters")

load = st.sidebar.slider("Load", 50, 100)
temp = st.sidebar.slider("Ambient Temp", 25, 50)
rpm = st.sidebar.slider("RPM", 1200, 1800)
oil = st.sidebar.slider("Oil Condition", 40, 100)

if st.sidebar.button("Predict"):
    result = model.predict([[load, temp, rpm, oil]])
    st.success(f"Predicted Temperature: {result[0]:.2f} °C")
