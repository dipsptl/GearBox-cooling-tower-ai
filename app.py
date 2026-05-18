import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import base64
import tempfile

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="THERMOLYTIX",
    layout="wide"
)

# =====================================================
# BACKGROUND IMAGE
# =====================================================

def add_bg():

    with open("bg.jpg", "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background-image: linear-gradient(
            rgba(0,0,0,0.78),
            rgba(0,0,0,0.82)
        ),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }}

    section[data-testid="stSidebar"] {{
        display:none;
    }}

    /* REMOVE EXTRA WHITE SPACE */
    .element-container {{
        margin-bottom: 0.4rem !important;
    }}

    /* GLASS CARDS */
    .glass {{
        background: rgba(0,0,0,0.62);
        border: 1px solid rgba(255,140,0,0.45);
        border-radius: 22px;
        padding: 22px;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 18px rgba(0,0,0,0.4);
    }}

    .title-main {{
        font-size: 56px;
        font-weight: 800;
        color: white;
        line-height: 1;
        margin-bottom: 10px;
    }}

    .sub-text {{
        color: #D0D0D0;
        font-size: 22px;
        line-height: 1.6;
    }}

    .orange {{
        color:#ff8800;
        font-weight:700;
        font-size:36px;
    }}

    .prediction {{
        font-size: 82px;
        font-weight: 800;
        color: white;
        line-height: 1;
    }}

    .safe-box {{
        background: rgba(0,120,30,0.7);
        padding: 22px;
        border-radius: 18px;
        font-size: 30px;
        font-weight: 700;
        color: #7CFF8A;
        text-align:center;
    }}

    .warn-box {{
        background: rgba(255,180,0,0.12);
        border:1px solid rgba(255,180,0,0.4);
        padding:14px;
        border-radius:12px;
        color:white;
        margin-bottom:10px;
        font-size:18px;
    }}

    .logo-img {{
        width: 420px;
        margin-top: -10px;
        margin-bottom: 10px;
    }}

    .status-box {{
        background: rgba(0,0,0,0.55);
        border:1px solid rgba(255,140,0,0.4);
        border-radius:18px;
        padding:18px 26px;
        color:white;
        font-size:20px;
        text-align:center;
    }}

    .stButton>button {{
        width:100%;
        height:68px;
        border:none;
        border-radius:16px;
        font-size:26px;
        font-weight:700;
        color:white;
        background: linear-gradient(
            90deg,
            #ff8800,
            #00cfff
        );
    }}

    div[data-baseweb="slider"] > div {{
        color:#ff8800 !important;
    }}

    label {{
        color:white !important;
        font-size:18px !important;
    }}

    </style>
    """, unsafe_allow_html=True)

add_bg()

# =====================================================
# DATA + MODEL
# =====================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =====================================================
# TOP HEADER
# =====================================================

top1, top2 = st.columns([5,1])

with top1:
    st.image("logo.png", width=420)

with top2:
    st.markdown("""
    <div class="status-box">
        🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns([1.1, 1])

# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.markdown("""
    <div class="glass">

        <div class="title-main">
            AI Dashboard
        </div>

        <div class="sub-text">
            Enter parameters to get AI-powered temperature
            predictions and system insights.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">
        <div class="orange">
            ⚙️ Enter Parameters
        </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load", 50, 100, 70)
    temp = st.slider("Ambient Temp", 25, 50, 30)
    rpm = st.slider("RPM", 1200, 1800, 1450)
    oil = st.slider("Oil Condition", 40, 100, 75)

    st.button("PREDICT TEMPERATURE")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    pred = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="glass">

        <div class="orange">
            📊 Prediction Summary
        </div>

        <div class="prediction">
            {pred:.1f}
            <span style="font-size:42px;">°C</span>
        </div>

    """, unsafe_allow_html=True)

    if pred > 90:
        status = "🔴 Danger"
    elif pred > 80:
        status = "🟠 Warning"
    else:
        status = "🟢 Safe"

    st.markdown(f"""
    <div class="safe-box">
        {status}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="orange">
        💡 Suggestions
    </div>
    """, unsafe_allow_html=True)

    if rpm > 1500:
        st.markdown(
            '<div class="warn-box">⚠️ Reduce RPM to control heat</div>',
            unsafe_allow_html=True
        )

    if oil < 60:
        st.markdown(
            '<div class="warn-box">⚠️ Oil condition poor – maintenance needed</div>',
            unsafe_allow_html=True
        )

    if load > 75:
        st.markdown(
            '<div class="warn-box">⚠️ High load – reduce load</div>',
            unsafe_allow_html=True
        )

    if temp > 35:
        st.markdown(
            '<div class="warn-box">⚠️ High ambient temp – improve cooling</div>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS SECTION
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass">
    <div class="orange">
        📈 Analysis
    </div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# =====================================================
# GRAPH 1
# =====================================================

with g1:

    fig1, ax1 = plt.subplots(figsize=(7,4))

    fig1.patch.set_facecolor("#050505")
    ax1.set_facecolor("#050505")

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=70
    )

    ax1.set_xlabel("Load (%)", color="white")
    ax1.set_ylabel("Temperature (°C)", color="white")
    ax1.tick_params(colors='white')

    for spine in ax1.spines.values():
        spine.set_color("#666")

    st.pyplot(fig1)

# =====================================================
# GRAPH 2
# =====================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(7,4))

    fig2.patch.set_facecolor("#050505")
    ax2.set_facecolor("#050505")

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=70
    )

    ax2.set_xlabel("RPM", color="white")
    ax2.set_ylabel("Temperature (°C)", color="white")
    ax2.tick_params(colors='white')

    for spine in ax2.spines.values():
        spine.set_color("#666")

    st.pyplot(fig2)

# =====================================================
# PDF REPORT
# =====================================================

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
        Paragraph(
            f"Predicted Temperature: {result:.2f} °C",
            styles['Normal']
        )
    )

    doc.build(content)

    return file.name

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

if st.button("📁 Download PDF Report"):

    pdf = create_pdf(load, temp, rpm, oil, pred)

    with open(pdf, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="THERMOLYTIX_REPORT.pdf"
        )
