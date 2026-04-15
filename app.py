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
⚙️ Cooling Tower Gear Temp AI Dashboard
</h2>
""", unsafe_allow_html=True)

# ===== LOAD DATA =====
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ===== INPUT SECTION =====
st.sidebar.header("Enter Parameters")

load = st.sidebar.slider("Load", 50, 100)
temp = st.sidebar.slider("Ambient Temp", 25, 50)
rpm = st.sidebar.slider("RPM", 1200, 1800)
oil = st.sidebar.slider("Oil Condition", 40, 100)

pred_value = model.predict([[load, temp, rpm, oil]])[0]

# ===== DASHBOARD LAYOUT =====
col1, col2 = st.columns(2)

# ===== LEFT SIDE =====
with col1:
    st.subheader("📌 Prediction Summary")

    st.metric("Predicted Temp (°C)", f"{pred_value:.2f}")

    if pred_value > 90:
        st.error("🔴 Danger")
    elif pred_value > 80:
        st.warning("🟠 Warning")
    else:
        st.success("🟢 Safe")

    # ===== SMART SUGGESTIONS =====
    st.subheader("💡 Suggestions")

    if rpm > 1500:
        st.warning("Reduce RPM to control heat")

    if oil < 60:
        st.warning("Oil condition poor – maintenance needed")

    if load > 75:
        st.warning("High load – reduce load")

    if temp > 35:
        st.warning("High ambient temp – improve cooling")

# ===== RIGHT SIDE =====
with col2:
    st.subheader("📊 Analysis")

    fig1, ax1 = plt.subplots()
    ax1.scatter(data['Load'], data['Temperature'])
    ax1.set_xlabel("Load")
    ax1.set_ylabel("Temperature")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.scatter(data['RPM'], data['Temperature'])
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Temperature")
    st.pyplot(fig2)

# ===== PDF FUNCTION =====
def create_pdf(load, temp, rpm, oil, result):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(file.name)

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Cooling Tower Report", styles['Title']))
    content.append(Paragraph(f"Load: {load}", styles['Normal']))
    content.append(Paragraph(f"Ambient Temp: {temp}", styles['Normal']))
    content.append(Paragraph(f"RPM: {rpm}", styles['Normal']))
    content.append(Paragraph(f"Oil Condition: {oil}", styles['Normal']))
    content.append(Paragraph(f"Predicted Temperature: {result:.2f} °C", styles['Normal']))

    doc.build(content)
    return file.name

# ===== DOWNLOAD BUTTON =====
if st.button("📁 Download PDF Report"):
    pdf_file = create_pdf(load, temp, rpm, oil, pred_value)

    with open(pdf_file, "rb") as f:
        st.download_button("Download Report", f, file_name="report.pdf")
