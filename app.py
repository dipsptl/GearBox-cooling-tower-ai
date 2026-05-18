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
# BACKGROUND
# =====================================================

def set_bg():

    with open("bg.jpg", "rb") as f:
        data = f.read()

    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>

    .stApp {{
        background:
        linear-gradient(
        rgba(0,0,0,0.88),
        rgba(0,0,0,0.88)),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 0.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1280px;
    }}

    header {{
        visibility:hidden;
    }}

    footer {{
        visibility:hidden;
    }}

    section[data-testid="stSidebar"] {{
        display:none;
    }}

    /* MAIN BOX */

    .glass {{
        background: rgba(0,0,0,0.52);
        border: 1px solid rgba(255,140,0,0.22);
        border-radius: 16px;
        padding: 10px;
        margin-bottom: 8px;
        backdrop-filter: blur(4px);
    }}

    /* TITLES */

    .title {{
        color:white;
        font-size:22px;
        font-weight:700;
        margin-bottom:6px;
    }}

    .sub {{
        color:#cfcfcf;
        font-size:12px;
        line-height:1.5;
    }}

    .section {{
        color:#ff8800;
        font-size:16px;
        font-weight:700;
        margin-bottom:8px;
    }}

    /* PREDICTION */

    .predict {{
        color:white;
        font-size:34px;
        font-weight:800;
    }}

    .safe {{
        background:rgba(0,120,25,0.65);
        padding:10px;
        border-radius:10px;
        color:#7dff8a;
        font-size:15px;
        text-align:center;
        font-weight:700;
    }}

    /* WARNING */

    .warn {{
        background:rgba(255,180,0,0.08);
        border:1px solid rgba(255,180,0,0.18);
        padding:8px;
        border-radius:8px;
        color:white;
        margin-bottom:6px;
        font-size:12px;
    }}

    /* STATUS */

    .status {{
        background:rgba(0,0,0,0.5);
        border:1px solid rgba(255,140,0,0.2);
        border-radius:12px;
        padding:8px;
        text-align:center;
        color:white;
        font-size:13px;
        margin-top:8px;
    }}

    /* BUTTON */

    .stButton > button {{
        width:100%;
        height:38px;
        border:none;
        border-radius:10px;
        font-size:14px;
        font-weight:700;
        color:white;

        background:linear-gradient(
        90deg,
        #ff8800,
        #00cfff
        );
    }}

    label {{
        color:white !important;
        font-size:13px !important;
    }}

    </style>
    """, unsafe_allow_html=True)

set_bg()

# =====================================================
# DATA
# =====================================================

data = pd.read_csv("cooling_data.csv")

X = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y = data['Temperature']

model = LinearRegression()
model.fit(X, y)

# =====================================================
# HEADER
# =====================================================

top1, top2 = st.columns([6,1])

with top1:

    st.image(
        "logo.png",
        width=180
    )

with top2:

    st.markdown("""
    <div class="status">
        🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns(
    [1,1],
    gap="medium"
)

# =====================================================
# LEFT SIDE
# =====================================================

with left:

    st.markdown("""
    <div class="glass">

        <div class="title">
            AI Dashboard
        </div>

        <div class="sub">
            Enter parameters to get AI-powered
            temperature predictions and system insights.
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="glass">

        <div class="section">
            ⚙️ Enter Parameters
        </div>

    """, unsafe_allow_html=True)

    load = st.slider(
        "Load",
        50,
        100,
        70
    )

    temp = st.slider(
        "Ambient Temp",
        25,
        50,
        30
    )

    rpm = st.slider(
        "RPM",
        1200,
        1800,
        1450
    )

    oil = st.slider(
        "Oil Condition",
        40,
        100,
        75
    )

    st.button("PREDICT TEMPERATURE")

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# RIGHT SIDE
# =====================================================

with right:

    pred = model.predict(
        [[load, temp, rpm, oil]]
    )[0]

    st.markdown(f"""
    <div class="glass">

        <div class="section">
            📊 Prediction Summary
        </div>

        <div class="predict">
            {pred:.1f} °C
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

        st.markdown("""
        <div class="warn">
            ⚠️ Reduce RPM to control heat
        </div>
        """, unsafe_allow_html=True)

    if oil < 60:

        st.markdown("""
        <div class="warn">
            ⚠️ Oil condition poor – maintenance needed
        </div>
        """, unsafe_allow_html=True)

    if load > 75:

        st.markdown("""
        <div class="warn">
            ⚠️ High load – reduce load
        </div>
        """, unsafe_allow_html=True)

    if temp > 35:

        st.markdown("""
        <div class="warn">
            ⚠️ High ambient temp – improve cooling
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# ANALYSIS TITLE
# =====================================================

st.markdown("""
<div class="glass">

<div class="section">
📈 Analysis
</div>

</div>
""", unsafe_allow_html=True)

# =====================================================
# GRAPHS
# =====================================================

g1, g2 = st.columns(2)

with g1:

    fig1, ax1 = plt.subplots(
        figsize=(4.8,2.4)
    )

    fig1.patch.set_facecolor("#050505")
    ax1.set_facecolor("#050505")

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=25
    )

    ax1.set_xlabel(
        "Load (%)",
        color="white",
        fontsize=8
    )

    ax1.set_ylabel(
        "Temperature",
        color="white",
        fontsize=8
    )

    ax1.tick_params(
        colors='white',
        labelsize=7
    )

    for spine in ax1.spines.values():
        spine.set_color("#666")

    st.pyplot(fig1)

with g2:

    fig2, ax2 = plt.subplots(
        figsize=(4.8,2.4)
    )

    fig2.patch.set_facecolor("#050505")
    ax2.set_facecolor("#050505")

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=25
    )

    ax2.set_xlabel(
        "RPM",
        color="white",
        fontsize=8
    )

    ax2.set_ylabel(
        "Temperature",
        color="white",
        fontsize=8
    )

    ax2.tick_params(
        colors='white',
        labelsize=7
    )

    for spine in ax2.spines.values():
        spine.set_color("#666")

    st.pyplot(fig2)

# =====================================================
# PDF FUNCTION
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
        pred
    )

    with open(pdf, "rb") as f:

        st.download_button(
            "Download Report",
            f,
            file_name="THERMOLYTIX_REPORT.pdf"
        )
