import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# ===== PAGE SETTINGS =====
st.set_page_config(page_title="Cooling Tower AI", layout="wide")

# ===== BACKGROUND =====
def set_bg():
    try:
        with open("bg.jpg", "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()

        st.markdown(f"""
        <style>
