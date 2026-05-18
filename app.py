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
        linear-gradient(
        rgba(0,0,0,0.84),
        rgba(0,0,0,0.84)),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    .block-container {{
        padding-top: 0.4rem;
        padding-left: 1.8rem;
        padding-right: 1.8rem;
        max-width: 1450px;
    }}

    section[data-testid="stSidebar"] {{
        display:none;
    }}

    header {{
        visibility:hidden;
    }}

    footer {{
        visibility:hidden;
    }}

    /* MAIN CARDS */

    .glass {{
        background: rgba(0,0,0,0.58);
        border: 1px solid rgba(255,140,0,0.28);
        border-radius: 18px;
        padding: 14px;
        backdrop-filter: blur(6px);
        margin-bottom: 12px;
    }}

    /* TITLES */

    .title {{
        color:white;
        font-size:30px;
        font-weight:700;
        margin-bottom:6px;
    }}

    .sub {{
        color:#cfcfcf;
        font-size:14px;
        line-height:1.5;
    }}

    .section {{
        color:#ff8800;
        font-size:18px;
        font-weight:700;
        margin-bottom:8px;
    }}

    /* PREDICTION */

    .predict {{
        color:white;
        font-size:42px;
        font-weight:800;
        line-height:1;
    }}

    .safe {{
        background:rgba(0,120,25,0.65);
        padding:12px;
        border-radius:12px;
        color:#7dff8a;
        font-size:18px;
        font-weight:700;
        text-align:center;
    }}

    .warn {{
        background:rgba(255,180,0,0.08);
        border:1px solid rgba(255,180,0,0.22);
        padding:9px;
        border-radius:10px;
        color:white;
        margin-bottom:7px;
        font-size:13px;
    }}

    /* STATUS BOX */

    .status {{
        background:rgba(0,0,0,0.58);
        border:1px solid rgba(255,140,0,0.25);
        border-radius:14px;
        padding:10px;
        color:white;
        text-align:center;
        font-size:14px;
        margin-top:12px;
    }}

    /* BUTTON */

    .stButton > button {{
        width:100%;
        height:44px;
        border:none;
        border-radius:10px;
        color:white;
        font-size:16px;
        font-weight:700;

        background:linear-gradient(
        90deg,
        #ff8800,
        #00cfff
        );
    }}

    /* LABELS */

    label {{
        color:white !important;
        font-size:14px !important;
    }}

    /* GRAPH */

    .graph-card {{
        background: rgba(0,0,0,0.58);
        border: 1px solid rgba(255,140,0,0.25);
        border-radius: 16px;
        padding: 10px;
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
# HEADER
# ======================================================

top1, top2 = st.columns([6,1])

with top1:

    st.image("logo.png", width=220)

with top2:

    st.markdown("""
    <div class="status">
        🟢 System Operational
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# MAIN LAYOUT
# ======================================================

left, right = st.columns(
    [0.9,1.1],
    gap="medium"
)

# ======================================================
# LEFT PANEL
# ======================================================

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

# ======================================================
# RIGHT PANEL
# ======================================================

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
            {pred:.1f}
            <span style="font-size:22px;">
            °C
            </span>
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

st.markdown("""
<div class="glass">
    <div class="section">
        📈 Analysis
    </div>
</div>
""", unsafe_allow_html=True)

g1, g2 = st.columns(2)

# ======================================================
# GRAPH 1
# ======================================================

with g1:

    st.markdown(
        '<div class="graph-card">',
        unsafe_allow_html=True
    )

    fig1, ax1 = plt.subplots(
        figsize=(5.8,2.8)
    )

    fig1.patch.set_facecolor("#050505")
    ax1.set_facecolor("#050505")

    ax1.scatter(
        data['Load'],
        data['Temperature'],
        s=35
    )

    ax1.set_xlabel(
        "Load (%)",
        color="white",
        fontsize=9
    )

    ax1.set_ylabel(
        "Temperature",
        color="white",
        fontsize=9
    )

    ax1.tick_params(
        colors='white',
        labelsize=8
    )

    for spine in ax1.spines.values():
        spine.set_color("#666")

    st.pyplot(fig1)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# ======================================================
# GRAPH 2
# ======================================================

with g2:

    st.markdown(
        '<div class="graph-card">',
        unsafe_allow_html=True
    )

    fig2, ax2 = plt.subplots(
        figsize=(5.8,2.8)
    )

    fig2.patch.set_facecolor("#050505")
    ax2.set_facecolor("#050505")

    ax2.scatter(
        data['RPM'],
        data['Temperature'],
        s=35
    )

    ax2.set_xlabel(
        "RPM",
        color="white",
        fontsize=9
    )

    ax2.set_ylabel(
        "Temperature",
        color="white",
        fontsize=9
    )

    ax2.tick_params(
        colors='white',
        labelsize=8
    )

    for spine in ax2.spines.values():
        spine.set_color("#666")

    st.pyplot(fig2)

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

# ======================================================
# PDF FUNCTION
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
            f"Predicted Temp: {result:.2f} °C",
            styles['Normal']
        )
    )

    doc.build(content)

    return file.name

# ======================================================
# DOWNLOAD
# ======================================================

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
