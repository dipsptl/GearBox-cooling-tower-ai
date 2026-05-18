import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="THERMOLYTIX",
    layout="wide"
)

# ======================================================
# BACKGROUND
# ======================================================

def set_bg():

    with open("bg.jpg", "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background:
        linear-gradient(rgba(0,0,0,0.82),
        rgba(0,0,0,0.82)),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 0.5rem;
        padding-left: 1.5rem;
        padding-right: 1.5rem;
        max-width: 100%;
    }}

    section[data-testid="stSidebar"] {{
        display:none;
    }}

    .glass {{
        background: rgba(0,0,0,0.55);
        border: 1px solid rgba(255,140,0,0.35);
        border-radius: 18px;
        padding: 18px;
        backdrop-filter: blur(6px);
    }}

    .title {{
        color:white;
        font-size:42px;
        font-weight:700;
        margin-bottom:8px;
    }}

    .sub {{
        color:#cfcfcf;
        font-size:17px;
        line-height:1.5;
    }}

    .section {{
        color:#ff8800;
        font-size:22px;
        font-weight:700;
        margin-bottom:10px;
    }}

    .predict {{
        color:white;
        font-size:64px;
        font-weight:800;
        line-height:1;
    }}

    .safe {{
        background:rgba(0,120,20,0.65);
        padding:16px;
        border-radius:14px;
        color:#7dff8a;
        font-size:24px;
        font-weight:700;
        text-align:center;
    }}

    .warn {{
        background:rgba(255,180,0,0.10);
        border:1px solid rgba(255,180,0,0.35);
        padding:12px;
        border-radius:10px;
        color:white;
        margin-bottom:8px;
        font-size:15px;
    }}

    .status {{
        background:rgba(0,0,0,0.55);
        border:1px solid rgba(255,140,0,0.35);
        border-radius:16px;
        padding:14px;
        color:white;
        text-align:center;
        font-size:18px;
    }}

    .stButton > button {{
        width:100%;
        height:55px;
        border:none;
        border-radius:12px;
        color:white;
        font-size:20px;
        font-weight:700;
        background:linear-gradient(90deg,#ff8800,#00cfff);
    }}

    label {{
        color:white !important;
    }}

    </style>
    """, unsafe_allow_html=True)

set_bg()

# ======================================================
# DATA
# ======================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# ======================================================
# TOP HEADER
# ======================================================

top1, top2 = st.columns([5,1])

with top1:
    st.image("logo.png", width=300)

with top2:
    st.markdown("""
    <div class="status">
        🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MAIN LAYOUT
# ======================================================

left, right = st.columns([1,1])

# ======================================================
# LEFT
# ======================================================

with left:

    st.markdown("""
    <div class="glass">
        <div class="title">AI Dashboard</div>

        <div class="sub">
            Enter parameters to get AI-powered
            temperature predictions and system insights.
        </div>

        <br>

        <div class="glass">

            <div class="section">
                ⚙️ Enter Parameters
            </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load", 50, 100, 70)

    temp = st.slider("Ambient Temp", 25, 50, 30)

    rpm = st.slider("RPM", 1200, 1800, 1450)

    oil = st.slider("Oil Condition", 40, 100, 75)

    st.button("PREDICT TEMPERATURE")

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# RIGHT
# ======================================================

with right:

    pred = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="glass">

        <div class="section">
            📊 Prediction Summary
        </div>

        <div class="predict">
            {pred:.1f}
            <span style="font-size:30px;">°C</span>
        </div>

        <br>

        <div class="safe">
            🟢 Safe
        </div>

        <br>

        <div class="section">
            💡 Suggestions
        </div>
    """, unsafe_allow_html=True)

    if rpm > 1500:
        st.markdown(
            '<div class="warn">⚠️ Reduce RPM to control heat</div>',
            unsafe_allow_html=True
        )

    if oil < 60:
        st.markdown(
            '<div class="warn">⚠️ Oil condition poor – maintenance needed</div>',
            unsafe_allow_html=True
        )

    if load > 75:
        st.markdown(
            '<div class="warn">⚠️ High load – reduce load</div>',
            unsafe_allow_html=True
        )

    if temp > 35:
        st.markdown(
            '<div class="warn">⚠️ High ambient temp – improve cooling</div>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# ANALYSIS
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass">
    <div class="section">📈 Analysis</div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# ======================================================
# GRAPH 1
# ======================================================

with g1:

    fig1, ax1 = plt.subplots(figsize=(6,3))

    fig1.patch.set_facecolor("#050505")
    ax1.set_facecolor("#050505")

    ax1.scatter(data['Load'], data['Temperature'])

    ax1.set_xlabel("Load (%)", color="white")
    ax1.set_ylabel("Temperature", color="white")

    ax1.tick_params(colors='white')

    for spine in ax1.spines.values():
        spine.set_color("#666")

    st.pyplot(fig1)

# ======================================================
# GRAPH 2
# ======================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(6,3))

    fig2.patch.set_facecolor("#050505")
    ax2.set_facecolor("#050505")

    ax2.scatter(data['RPM'], data['Temperature'])

    ax2.set_xlabel("RPM", color="white")
    ax2.set_ylabel("Temperature", color="white")

    ax2.tick_params(colors='white')

    for spine in ax2.spines.values():
        spine.set_color("#666")

    st.pyplot(fig2)

# ======================================================
# PDF
# ======================================================

def create_pdf(load, temp, rpm, oil, result):

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(file.name)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("THERMOLYTIX REPORT", styles['Title'])
    )

    content.append(
        Paragraph(f"Load: {load}", styles['Normal'])
    )

    content.append(
        Paragraph(f"Ambient Temp: {temp}", styles['Normal'])
    )

    content.append(
        Paragraph(f"RPM: {rpm}", styles['Normal'])
    )

    content.append(
        Paragraph(f"Oil Condition: {oil}", styles['Normal'])
    )

    content.append(
        Paragraph(f"Predicted Temp: {result:.2f} °C", styles['Normal'])
    )

    doc.build(content)

    return file.name

# ======================================================
# DOWNLOAD
# ======================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("📁 Download PDF Report"):

    pdf = create_pdf(load, temp, rpm, oil, pred)

    with open(pdf, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="THERMOLYTIX_REPORT.pdf"
        )
