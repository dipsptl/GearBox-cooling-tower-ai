import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import base64

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Cooling Tower AI", layout="centered")

# ===== BACKGROUND =====
def set_bg():
    try:
        with open("bg.jpg", "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()

        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        pass

set_bg()

# ===== TITLE =====
st.markdown("""
<h2 style='text-align: center; color: #FF8C00;'>
⚙️ Cooling Tower Gear Temp AI Predictor
</h2>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ===== INPUT =====
st.subheader("Enter Parameters")

load = st.slider("Load", 50, 100)
temp = st.slider("Ambient Temp", 25, 50)
rpm = st.slider("RPM", 1200, 1800)
oil = st.slider("Oil Condition", 40, 100)

# ===== PREDICTION =====
if st.button("Predict Temperature"):
    result = model.predict([[load, temp, rpm, oil]])
    st.success(f"Predicted Temperature: {result[0]:.2f} °C")

# ===== BASIC AI ASSISTANT (NO API) =====
st.subheader("🤖 AI Assistant (Basic)")

question = st.text_input("Ask about cooling tower:")

if question:
    q = question.lower()

    if "temperature" in q:
        st.write("High temperature can be due to high load, high RPM, or poor oil condition.")
    elif "rpm" in q:
        st.write("Higher RPM increases heat. Maintain optimal RPM to control temperature.")
    elif "oil" in q:
        st.write("Poor oil condition increases friction and heat. Regular maintenance is important.")
    elif "load" in q:
        st.write("Higher load increases stress on gearbox and raises temperature.")
    else:
        st.write("Check load, RPM, ambient temperature, and oil condition for better performance.")
