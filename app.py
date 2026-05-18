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
    page_title="THERMOLYTIX AI Dashboard",
    layout="wide"
)

# =====================================================
# IMAGE LOAD
# =====================================================

def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("bg.jpg")
logo = get_base64("logo.png")

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    max-width: 1600px;
}}

header {{
    visibility:hidden;
}}

#MainMenu {{
    visibility:hidden;
}}

footer {{
    visibility:hidden;
}}

.main-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 18px;
    padding: 20px;
    backdrop-filter: blur(6px);
    margin-bottom: 18px;
}}

.small-card {{
    background: rgba(0,0,0,0.60);
    border-radius: 15px;
    padding: 15px;
}}

.logo-img {{
    width: 280px;
    margin-top: -10px;
}}

.title-orange {{
    color: #ff8800;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 12px;
}}

.big-number {{
    font-size: 48px;
    font-weight: 800;
    color: white;
    margin: 15px 0;
}}

.safe-box {{
    background: #006b28;
    border-radius: 10px;
    padding: 12px;
    color: #67ff99;
    font-size: 18px;
    font-weight: 700;
    margin: 12px 0;
}}

.warn-box {{
    background: rgba(255,180,0,0.12);
    border: 1px solid rgba(255,180,0,0.2);
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 8px;
    color: #ffd76a;
    font-size: 14px;
}}

.system-box {{
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,140,0,0.3);
    border-radius: 12px;
    padding: 8px 15px;
    color: white;
    font-size: 14px;
    text-align: center;
    width: 200px;
    margin-left: auto;
}}

.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg,#ff8800,#00cfff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px;
    font-size: 16px;
    font-weight: 700;
}}

.graph-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 18px;
    padding: 15px;
}}

.slider-label {{
    font-size: 13px;
    color: #d8d8d8;
    margin-bottom: 5px;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

top1, top2 = st.columns([5, 1])

with top1:
    st.markdown(f"""
    <img class="logo-img"
    src="data:image/png;base64,{logo}">
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="system-box">
    🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =====================================================
# MAIN SECTION
# =====================================================

left, right = st.columns([1, 1], gap="medium")

# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.markdown("""
    <div class="main-card">

    <h1 style="color:white; font-size:28px; margin:0 0 10px 0;">
    AI Dashboard
    </h1>

    <p style="color:#d8d8d8; font-size:14px; margin:0 0 20px 0;">
    Enter parameters to get AI-powered temperature predictions and system insights.
    </p>

    <div class="title-orange">
    ⚙️ Enter Parameters
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slider-label">Load</div>', unsafe_allow_html=True)
    load = st.slider("Load", 50, 100, 70, label_visibility="collapsed")
    
    st.markdown('<div class="slider-label">Ambient Temp</div>', unsafe_allow_html=True)
    temp = st.slider("Ambient Temp", 25, 50, 30, label_visibility="collapsed")
    
    st.markdown('<div class="slider-label">RPM</div>', unsafe_allow_html=True)
    rpm = st.slider("RPM", 1200, 1800, 1450, label_visibility="collapsed")
    
    st.markdown('<div class="slider-label">Oil Condition</div>', unsafe_allow_html=True)
    oil = st.slider("Oil Condition", 40, 100, 75, label_visibility="collapsed")

    st.button("PREDICT TEMPERATURE")

# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="main-card">

    <div class="title-orange">
    📊 Prediction Summary
    </div>

    <div class="big-number">
    {pred_value:.1f} °C
    </div>

    <div class="safe-box">
    🟢 Safe
    </div>

    <div class="title-orange" style="margin-top: 20px;">
    💡 Suggestions
    </div>

    """, unsafe_allow_html=True)

    if rpm > 1400:
        st.markdown("""
        <div class="warn-box">
        ⚠️ Reduce RPM to control heat
        </div>
        """, unsafe_allow_html=True)

    if oil < 80:
        st.markdown("""
        <div class="warn-box">
        ⚠️ Oil condition poor – maintenance needed
        </div>
        """, unsafe_allow_html=True)

    if load > 65:
        st.markdown("""
        <div class="warn-box">
        ⚠️ High load – reduce load
        </div>
        """, unsafe_allow_html=True)

    if temp > 28:
        st.markdown("""
        <div class="warn-box">
        ⚠️ High ambient temp – improve cooling
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS
# =====================================================

st.markdown("""
<div class="main-card">
<div class="title-orange">
📈 Analysis
</div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="medium")

# =====================================================
# GRAPH 1
# =====================================================

with g1:

    fig1, ax1 = plt.subplots(figsize=(5.5, 3))

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=50,
        color='#00bfff'
    )

    ax1.set_facecolor("#050b18")
    fig1.patch.set_facecolor("#050b18")

    ax1.set_title(
        "Temperature vs Load",
        color="white",
        fontsize=12,
        fontweight='bold',
        pad=10
    )

    ax1.set_xlabel("Load (%)", color="white", fontsize=10)
    ax1.set_ylabel("Temperature (°C)", color="white", fontsize=10)

    ax1.tick_params(colors='white', labelsize=9)

    for spine in ax1.spines.values():
        spine.set_color("white")
        spine.set_linewidth(0.5)

    ax1.grid(True, alpha=0.1, color='white')

    fig1.tight_layout()

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GRAPH 2
# =====================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(5.5, 3))

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=50,
        color='#00bfff'
    )

    ax2.set_facecolor("#050b18")
    fig2.patch.set_facecolor("#050b18")

    ax2.set_title(
        "Temperature vs RPM",
        color="white",
        fontsize=12,
        fontweight='bold',
        pad=10
    )

    ax2.set_xlabel("RPM", color="white", fontsize=10)
    ax2.set_ylabel("Temperature (°C)", color="white", fontsize=10)

    ax2.tick_params(colors='white', labelsize=9)

    for spine in ax2.spines.values():
        spine.set_color("white")
        spine.set_linewidth(0.5)

    ax2.grid(True, alpha=0.1, color='white')

    fig2.tight_layout()

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
        Paragraph(
            "THERMOLYTIX REPORT",
            styles['Title']
        )
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

    pdf = create_pdf(
        load,
        temp,
        rpm,
        oil,
        pred_value
    )

    with open(pdf, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="thermolytix_report.pdf"
        )
