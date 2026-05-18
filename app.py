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
# BACKGROUND IMAGE
# =====================================================

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg = get_base64("bg.jpg")
logo = get_base64("logo.png")

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(f"""
<style>

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
}}

.block-container {{
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}}

section[data-testid="stSidebar"] {{
    display:none;
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
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,140,0,0.5);
    border-radius: 18px;
    padding: 22px;
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}}

.small-card {{
    background: rgba(0,0,0,0.45);
    border: 1px solid rgba(255,140,0,0.4);
    border-radius: 15px;
    padding: 18px;
    backdrop-filter: blur(8px);
}}

.title-orange {{
    color: #ff8800;
    font-size: 20px;
    font-weight: 700;
}}

.big-number {{
    font-size: 70px;
    font-weight: 800;
    color: white;
    line-height: 1;
}}

.safe-box {{
    background: linear-gradient(90deg,#003b18,#006d2c);
    border-radius: 10px;
    padding: 14px;
    color: #4cff88;
    font-size: 28px;
    font-weight: 700;
}}

.warn-box {{
    background: rgba(255,180,0,0.15);
    border: 1px solid rgba(255,180,0,0.3);
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 10px;
    color: #ffd76a;
}}

.stButton>button {{
    width: 100%;
    background: linear-gradient(90deg,#ff8800,#00d4ff);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 15px;
    font-size: 22px;
    font-weight: 700;
}}

.logo-img {{
    width: 500px;
}}

.system-box {{
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(255,140,0,0.4);
    border-radius: 12px;
    padding: 14px 22px;
    color: white;
    font-size: 22px;
    text-align: center;
}}

.graph-card {{
    background: rgba(0,0,0,0.55);
    border: 1px solid rgba(255,140,0,0.5);
    border-radius: 18px;
    padding: 20px;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

top1, top2 = st.columns([4,1])

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
# MAIN LAYOUT
# =====================================================

left, right = st.columns([1,1])

# =====================================================
# LEFT PANEL
# =====================================================

with left:

    st.markdown("""
    <div class="main-card">

    <h1 style="color:white; margin-bottom:0px;">
    AI Dashboard
    </h1>

    <p style="color:#cfcfcf; font-size:22px;">
    Enter parameters to get AI-powered temperature predictions and system insights.
    </p>

    <div class="small-card">
    <div class="title-orange">⚙️ Enter Parameters</div>
    </div>

    </div>
    """, unsafe_allow_html=True)

    load = st.slider("Load", 50, 100, 70)
    temp = st.slider("Ambient Temp", 25, 50, 30)
    rpm = st.slider("RPM", 1200, 1800, 1450)
    oil = st.slider("Oil Condition", 40, 100, 75)

    st.button("PREDICT TEMPERATURE")

# =====================================================
# RIGHT PANEL
# =====================================================

with right:

    pred_value = model.predict([[load,temp,rpm,oil]])[0]

    st.markdown(f"""
    <div class="main-card">

    <div class="title-orange">
    📊 Prediction Summary
    </div>

    <div class="big-number">
    {pred_value:.1f}
    <span style="font-size:40px;">°C</span>
    </div>

    <div class="safe-box">
    🟢 Safe
    </div>

    <br>

    <div class="title-orange">
    💡 Suggestions
    </div>

    <br>

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
# ANALYSIS SECTION
# =====================================================

st.markdown("""
<div class="main-card">
<div class="title-orange">
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

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=80
    )

    ax1.set_facecolor("#050b18")
    fig1.patch.set_facecolor("#050b18")

    ax1.set_title(
        "Temperature vs Load",
        color="white",
        fontsize=16
    )

    ax1.set_xlabel("Load (%)", color="white")
    ax1.set_ylabel("Temperature (°C)", color="white")

    ax1.tick_params(colors='white')

    for spine in ax1.spines.values():
        spine.set_color("white")

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# GRAPH 2
# =====================================================

with g2:

    fig2, ax2 = plt.subplots(figsize=(7,4))

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=80
    )

    ax2.set_facecolor("#050b18")
    fig2.patch.set_facecolor("#050b18")

    ax2.set_title(
        "Temperature vs RPM",
        color="white",
        fontsize=16
    )

    ax2.set_xlabel("RPM", color="white")
    ax2.set_ylabel("Temperature (°C)", color="white")

    ax2.tick_params(colors='white')

    for spine in ax2.spines.values():
        spine.set_color("white")

    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig2)
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
            "THERMOLYTIX AI REPORT",
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
