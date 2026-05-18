import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

# =========================================
# PAGE SETTINGS
# =========================================
st.set_page_config(
    page_title="Thermolytix AI",
    layout="wide"
)

# =========================================
# LOAD LOGO
# =========================================
def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64("logo.png")

# =========================================
# BACKGROUND
# =========================================
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
            background-attachment: fixed;
        }}

        .main-card {{
            background: rgba(0,0,0,0.55);
            border: 1px solid rgba(255,140,0,0.25);
            border-radius: 18px;
            padding: 25px;
            backdrop-filter: blur(8px);
            box-shadow: 0 0 18px rgba(255,140,0,0.15);
        }}

        .section-title {{
            color:#FF9C1A;
            font-size:28px;
            font-weight:700;
            margin-bottom:20px;
        }}

        .metric-box {{
            background: rgba(0,0,0,0.45);
            border:1px solid rgba(255,140,0,0.2);
            border-radius:16px;
            padding:20px;
        }}

        </style>
        """, unsafe_allow_html=True)

    except:
        pass

set_bg()

# =========================================
# TOP HEADER
# =========================================
st.markdown(f"""
<div style="
display:flex;
align-items:center;
justify-content:space-between;
margin-top:-20px;
margin-bottom:20px;
">

<div style="display:flex; align-items:center; gap:15px;">

<img src="data:image/png;base64,{logo}" width="90">

<div>
<div style="
font-size:42px;
font-weight:900;
color:#FF8C00;
line-height:1;
">
THERMO<span style="color:#29D8FF;">LYTIX</span>
</div>

<div style="
color:#CCCCCC;
font-size:14px;
letter-spacing:2px;
margin-top:4px;
">
GEARBOX THERMAL ANALYTICS
</div>
</div>

</div>

<div style="
background:rgba(0,0,0,0.5);
padding:10px 18px;
border-radius:12px;
border:1px solid rgba(255,140,0,0.2);
color:#00FF88;
font-weight:600;
">
🟢 System Operational
</div>

</div>
""", unsafe_allow_html=True)

# =========================================
# LOAD DATA
# =========================================
data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =========================================
# MAIN LAYOUT
# =========================================
left, right = st.columns([1.3, 1])

# =========================================
# LEFT PANEL
# =========================================
with left:

    st.markdown("""
    <div class="main-card">
    <div class="section-title">
    ⚙️ Cooling Tower Gear Temp. AI Dashboard
    </div>

    <div style="color:#CCCCCC; margin-bottom:25px;">
    Enter parameters to get AI-powered temperature predictions and system insights.
    </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load (%)", 50, 100, 70)

    temp = st.slider("Ambient Temp (°C)", 25, 50, 30)

    rpm = st.slider("RPM", 1200, 1800, 1450)

    oil = st.slider("Oil Condition (%)", 40, 100, 75)

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# RIGHT PANEL
# =========================================
with right:

    st.markdown("""
    <div class="main-card">
    <div class="section-title">
    📊 Prediction Summary
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <h1 style="
    color:white;
    font-size:58px;
    margin-top:-10px;
    ">
    {pred_value:.1f}
    <span style="font-size:24px;">°C</span>
    </h1>
    """, unsafe_allow_html=True)

    if pred_value > 90:
        st.error("🔴 Danger")

    elif pred_value > 80:
        st.warning("🟠 Warning")

    else:
        st.success("🟢 Safe")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
    💡 Suggestions
    </div>
    """, unsafe_allow_html=True)

    if rpm > 1500:
        st.warning("Reduce RPM to control heat")

    if oil < 60:
        st.warning("Oil condition poor – maintenance needed")

    if load > 75:
        st.warning("High load – reduce load")

    if temp > 35:
        st.warning("High ambient temp – improve cooling")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# ANALYSIS
# =========================================
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="main-card">
<div class="section-title">
📈 Analysis
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    ax1.scatter(data['Load'], data['Temperature'])
    ax1.set_xlabel("Load (%)")
    ax1.set_ylabel("Temperature (°C)")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    ax2.scatter(data['RPM'], data['Temperature'])
    ax2.set_xlabel("RPM")
    ax2.set_ylabel("Temperature (°C)")
    st.pyplot(fig2)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# PDF FUNCTION
# =========================================
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
    content.append(Paragraph(f"Temperature: {result:.2f} °C", styles['Normal']))

    doc.build(content)

    return file.name

# =========================================
# DOWNLOAD REPORT
# =========================================
st.markdown("<br>", unsafe_allow_html=True)

if st.button("📁 Download PDF Report"):

    pdf_file = create_pdf(load, temp, rpm, oil, pred_value)

    with open(pdf_file, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="Cooling_Tower_Report.pdf"
        )
