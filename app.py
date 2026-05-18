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
# CSS - ULTRA COMPACT
# =====================================================

st.markdown(f"""
<style>

* {{
    margin: 0;
    padding: 0;
}}

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.block-container {{
    padding-top: 0.3rem !important;
    padding-left: 0.8rem !important;
    padding-right: 0.8rem !important;
    max-width: 100% !important;
}}

header {{
    display: none !important;
}}

#MainMenu {{
    display: none !important;
}}

footer {{
    display: none !important;
}}

.main-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 12px;
    padding: 12px;
    backdrop-filter: blur(6px);
    margin-bottom: 10px;
}}

.logo-img {{
    width: 150px;
    margin: 0;
    padding: 0;
}}

.title-orange {{
    color: #ff8800;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 8px;
}}

.big-number {{
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin: 8px 0;
    line-height: 1;
}}

.safe-box {{
    background: #006b28;
    border-radius: 8px;
    padding: 8px;
    color: #67ff99;
    font-size: 16px;
    font-weight: 700;
    margin: 8px 0;
}}

.warn-box {{
    background: rgba(255,180,0,0.12);
    border: 1px solid rgba(255,180,0,0.2);
    border-radius: 8px;
    padding: 6px 8px;
    margin-bottom: 5px;
    color: #ffd76a;
    font-size: 12px;
}}

.system-box {{
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,140,0,0.3);
    border-radius: 8px;
    padding: 6px 10px;
    color: white;
    font-size: 12px;
    text-align: center;
    width: 170px;
    margin-left: auto;
}}

.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg,#ff8800,#00cfff);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px;
    font-size: 13px;
    font-weight: 700;
    height: 38px;
}}

.graph-card {{
    background: rgba(0,0,0,0.72);
    border: 1px solid rgba(255,140,0,0.35);
    border-radius: 12px;
    padding: 10px;
}}

.slider-container {{
    margin-bottom: 8px;
}}

.slider-label {{
    font-size: 11px;
    color: #d8d8d8;
    margin-bottom: 3px;
}}

[data-testid="stMetricValue"] {{
    font-size: 24px !important;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER - MINIMAL
# =====================================================

top1, top2 = st.columns([5, 1], gap="small")

with top1:
    st.markdown(f"""
    <img class="logo-img" src="data:image/png;base64,{logo}">
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="system-box">
    🟢 Operational
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

left, right = st.columns([1.05, 1], gap="small")

# =====================================================
# LEFT SIDE - COMPACT
# =====================================================

with left:

    st.markdown("""
    <div class="main-card">
    <h2 style="color:white; font-size:20px; margin:0 0 6px 0;">AI Dashboard</h2>
    <p style="color:#d8d8d8; font-size:12px; margin:0 0 12px 0;">Enter parameters to get AI-powered temperature predictions.</p>
    <div class="title-orange">⚙️ Enter Parameters</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="slider-label">Load</div>', unsafe_allow_html=True)
    load = st.slider("Load", 50, 100, 70, label_visibility="collapsed", key="load")
    
    st.markdown('<div class="slider-label">Ambient Temp</div>', unsafe_allow_html=True)
    temp = st.slider("Ambient Temp", 25, 50, 30, label_visibility="collapsed", key="temp")
    
    st.markdown('<div class="slider-label">RPM</div>', unsafe_allow_html=True)
    rpm = st.slider("RPM", 1200, 1800, 1450, label_visibility="collapsed", key="rpm")
    
    st.markdown('<div class="slider-label">Oil Condition</div>', unsafe_allow_html=True)
    oil = st.slider("Oil Condition", 40, 100, 75, label_visibility="collapsed", key="oil")

    st.button("🔥 PREDICT TEMPERATURE", use_container_width=True)

# =====================================================
# RIGHT SIDE - COMPACT
# =====================================================

with right:

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="main-card">
    <div class="title-orange">📊 Prediction Summary</div>
    <div class="big-number">{pred_value:.1f} °C</div>
    <div class="safe-box">🟢 Safe</div>
    <div class="title-orange" style="margin-top: 10px;">💡 Suggestions</div>
    </div>
    """, unsafe_allow_html=True)

    suggestions_html = ""
    
    if rpm > 1400:
        suggestions_html += '<div class="warn-box">⚠️ Reduce RPM to control heat</div>'

    if oil < 80:
        suggestions_html += '<div class="warn-box">⚠️ Oil condition poor – maintenance needed</div>'

    if load > 65:
        suggestions_html += '<div class="warn-box">⚠️ High load – reduce load</div>'

    if temp > 28:
        suggestions_html += '<div class="warn-box">⚠️ High ambient temp – improve cooling</div>'

    if suggestions_html:
        st.markdown(f'<div class="main-card">{suggestions_html}</div>', unsafe_allow_html=True)

# =====================================================
# ANALYSIS SECTION - COMPACT
# =====================================================

st.markdown("""
<div class="main-card">
<div class="title-orange">📈 Analysis</div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="small")

# =====================================================
# GRAPH 1 - SMALL
# =====================================================

with g1:

    fig1, ax1 = plt.subplots(figsize=(4, 2.2))

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=30,
        color='#00bfff',
        alpha=0.7
    )

    ax1.set_facecolor("#050b18")
    fig1.patch.set_facecolor("#050b18")

    ax1.set_title("Temperature vs Load", color="white", fontsize=10, fontweight='bold', pad=5)
    ax1.set_xlabel("Load (%)", color="white", fontsize=9)
    ax1.set_ylabel("Temperature (°C)", color="white", fontsize=9)

    ax1.tick_params(colors='white', labelsize=8)

    for spine in ax1.spines.values():
        spine.set_color("white")
        spine.set_linewidth(0.5)

    ax1.grid(True, alpha=0.1, color='white', linewidth=0.5)
    fig1.tight_layout(pad=0.5)

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GRAPH 2 - SMALL
# =====================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(4, 2.2))

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=30,
        color='#00bfff',
        alpha=0.7
    )

    ax2.set_facecolor("#050b18")
    fig2.patch.set_facecolor("#050b18")

    ax2.set_title("Temperature vs RPM", color="white", fontsize=10, fontweight='bold', pad=5)
    ax2.set_xlabel("RPM", color="white", fontsize=9)
    ax2.set_ylabel("Temperature (°C)", color="white", fontsize=9)

    ax2.tick_params(colors='white', labelsize=8)

    for spine in ax2.spines.values():
        spine.set_color("white")
        spine.set_linewidth(0.5)

    ax2.grid(True, alpha=0.1, color='white', linewidth=0.5)
    fig2.tight_layout(pad=0.5)

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

if st.button("📁 Download PDF Report", use_container_width=True):

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
            file_name="thermolytix_report.pdf",
            use_container_width=True
        )
