import streamlit as st
import pandas as pd
import base64
from sklearn.linear_model import LinearRegression

# ===== PAGE SETTING =====
st.set_page_config(page_title="Cooling Tower AI", layout="centered")

# ===== BACKGROUND (JPG) =====
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
    }}

    /* transparent header */
    [data-testid="stHeader"], .stToolbar {{
        background: transparent;
    }}

    /* slight dark overlay for readability */
    .stApp {{
        background-color: rgba(0,0,0,0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# 👉 APPLY BACKGROUND
set_bg()

# ===== TITLE (DARK ORANGE) =====
st.markdown("""
<h1 style='
    text-align: center;
    color: #FF8C00;
    font-size: 40px;
    font-weight: 700;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.7);
'>
⚙️ Cooling Tower Gear Temp AI Predictor
</h1>
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
temp = st.slider("Ambient Temp", 25, 50)
rpm = st.slider("RPM", 1200, 1800)
oil = st.slider("Oil Condition", 40, 100)

from openai import OpenAI

# ===== LLM SETUP =====
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.subheader("🤖 AI Assistant (Ask Anything)")

user_question = st.text_input("Ask about cooling tower:")

if user_question:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert mechanical engineer specializing in cooling towers, gearboxes, and industrial systems. Give clear and practical answers."
            },
            {
                "role": "user",
                "content": user_question
            }
        ]
    )

    answer = response.choices[0].message.content
    st.write(answer)
