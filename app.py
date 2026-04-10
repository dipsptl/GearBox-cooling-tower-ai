import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load data
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

st.title("Cooling Tower AI Predictor")

load = st.slider("Load", 50, 100)
temp = st.slider("Ambient Temp", 25, 50)
rpm = st.slider("RPM", 1200, 1800)
oil = st.slider("Oil Condition", 40, 100)

if st.button("Predict"):
    result = model.predict([[load, temp, rpm, oil]])
    st.success(f"Predicted Temperature: {result[0]:.2f}")