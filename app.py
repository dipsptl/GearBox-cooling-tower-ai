import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import openai
import base64

# ===== PAGE =====
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
        st.warning("Background image not found")

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

# ===== LLM =====
st.subheader("🤖 AI Assistant")

question = st.text_input("Ask about cooling tower:")

if question:
    try:
        openai.api_key = st.secrets["OPENAI_API_KEY"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a mechanical engineer expert in cooling towers."},
                {"role": "user", "content": question}
            ]
        )

        answer = response['choices'][0]['message']['content']
        st.write(answer)

    except KeyError:
        st.error("API Key not found. Please add it in Streamlit secrets.")
    except Exception:
        st.error("Error connecting to AI. Please try again.")
