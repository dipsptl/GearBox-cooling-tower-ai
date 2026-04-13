import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from openai import OpenAI

# ===== PAGE =====
st.set_page_config(page_title="Cooling Tower AI", layout="centered")

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

# ===== LLM SECTION =====
st.subheader("🤖 AI Assistant")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

question = st.text_input("Ask about cooling tower:")

if question:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a mechanical engineer expert in cooling towers and gear systems."},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content
    st.write(answer)
