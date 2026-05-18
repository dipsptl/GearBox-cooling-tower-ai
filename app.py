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

bg   = get_base64("bg.jpg")
logo = get_base64("logo.png")

# =====================================================
# CSS
# =====================================================

st.markdown(f"""
<style>

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"] {{
    height: 100vh;
    overflow: hidden;
}}

.stApp {{
    background-image: url("data:image/jpg;base64,{bg}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    height: 100vh;
    overflow: hidden;
}}

.block-container {{
    padding: 0.4rem 1rem 0 1rem !important;
    max-width: 100% !important;
}}

header {{ display: none !important; }}
#MainMenu {{ display: none !important; }}
footer {{ display: none !important; }}
[data-testid="stToolbar"] {{ display: none !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}

/* ── LOGO ── */
.logo-wrap {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0 4px 0;
}}
.logo-img {{ width: 110px; }}
.logo-title {{
    color: #ff8800;
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 2px;
    line-height: 1;
    font-family: 'Arial Black', sans-serif;
}}
.logo-sub {{
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-top: 3px;
}}

/* ── STATUS BADGE ── */
.status-box {{
    background: rgba(0,0,0,0.7);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 6px 14px;
    color: white;
    font-size: 12px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 7px;
    float: right;
    margin-top: 10px;
}}

/* ── CARDS ── */
.card {{
    background: rgba(15,15,25,0.82);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 12px;
    padding: 12px 14px;
    backdrop-filter: blur(8px);
    margin-bottom: 8px;
}}

/* ── SECTION TITLES ── */
.sec-title {{
    color: #ff8800;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}}

/* ── DASHBOARD TITLE CARD ── */
.dash-title {{
    color: white;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 3px;
}}
.dash-sub {{
    color: #aaaaaa;
    font-size: 11px;
}}

/* ── SLIDERS ── */
[data-testid="stSlider"] {{ padding: 0 !important; }}
[data-testid="stSlider"] > div {{ padding: 0 !important; }}
[data-testid="stSlider"] [data-baseweb="slider"] {{
    margin-top: 2px !important;
    margin-bottom: 2px !important;
}}
[data-testid="stSlider"] label {{ display: none !important; }}
.stSlider {{ margin-bottom: 0 !important; }}

/* slider value box */
.val-box {{
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px;
    color: white;
    font-size: 13px;
    font-weight: 700;
    min-width: 52px;
    text-align: center;
    padding: 4px 6px;
}}
.val-unit {{
    color: #888;
    font-size: 11px;
    min-width: 28px;
}}
.row-icon {{ font-size: 16px; min-width: 20px; text-align: center; padding-top: 14px; }}
.row-label {{ color: #cccccc; font-size: 12px; min-width: 90px; padding-top: 16px; }}
.row-right {{ display: flex; align-items: center; gap: 6px; padding-top: 12px; }}

/* ── PREDICT BUTTON ── */
.stButton > button {{
    width: 100%;
    background: linear-gradient(90deg, #ff7700, #00cfff);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 800;
    height: 42px;
    letter-spacing: 1px;
    margin-top: 4px;
}}

/* ── PREDICTION TEMP ── */
.pred-num {{
    font-size: 58px;
    font-weight: 900;
    color: white;
    line-height: 1;
    margin: 6px 0 4px 0;
    font-family: 'Arial Black', sans-serif;
}}
.pred-deg {{ font-size: 26px; color: #cccccc; font-weight: 400; }}

/* ── SAFE PILL ── */
.safe-pill {{
    background: #004d1f;
    border-radius: 6px;
    padding: 7px 14px;
    color: #4dff88;
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 6px 0 0 0;
}}

/* ── WARN PILLS ── */
.warn-pill {{
    background: rgba(80,60,0,0.55);
    border: 1px solid rgba(200,160,0,0.25);
    border-radius: 6px;
    padding: 7px 10px;
    color: #e8d080;
    font-size: 12px;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 8px;
}}

/* ── ANALYSIS ── */
.analysis-bar {{
    color: #ff8800;
    font-size: 14px;
    font-weight: 700;
    margin: 4px 0 6px 0;
    display: flex;
    align-items: center;
    gap: 6px;
}}
.graph-card {{
    background: rgba(15,15,25,0.82);
    border: 1px solid rgba(255,140,0,0.25);
    border-radius: 12px;
    padding: 8px 10px;
    backdrop-filter: blur(8px);
}}

/* ── DOWNLOAD BTN ── */
.dl-wrap .stButton > button {{
    background: rgba(10,10,20,0.75) !important;
    border: 1px solid rgba(255,180,0,0.4) !important;
    color: #ffd060 !important;
    font-size: 12px !important;
    height: 34px !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    width: auto !important;
    padding: 0 18px !important;
}}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

h1, h2 = st.columns([5, 1], gap="small")

with h1:
    st.markdown(f"""
    <div class="logo-wrap">
        <img class="logo-img" src="data:image/png;base64,{logo}">
        <div>
            <div class="logo-title">THERMOLYTIX</div>
            <div class="logo-sub">GEARBOX THERMAL ANALYTICS</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown('<div class="status-box">🟢 System Operational</div>', unsafe_allow_html=True)

# =====================================================
# LOAD DATA & MODEL
# =====================================================

data  = pd.read_csv("cooling_data.csv")
X     = data[['Load', 'Ambient_Temp', 'RPM', 'Oil_Condition']]
y     = data['Temperature']
model = LinearRegression()
model.fit(X, y)

# =====================================================
# MAIN COLUMNS
# =====================================================

left, right = st.columns([1.08, 1], gap="small")

# ── LEFT ──
with left:

    st.markdown("""
    <div class="card">
        <div class="dash-title">AI Dashboard</div>
        <div class="dash-sub">Enter parameters to get AI-powered temperature predictions and system insights.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="sec-title">⚙️ Enter Parameters</div>', unsafe_allow_html=True)

    slider_cfg = [
        ("🏎️", "Load",          "load", 50,   100,  70,   "%"),
        ("🌡️", "Ambient Temp",  "temp", 25,   50,   30,   "°C"),
        ("⚡",  "RPM",           "rpm",  1200, 1800, 1450, "RPM"),
        ("🛢️", "Oil Condition", "oil",  40,   100,  75,   "%"),
    ]

    vals = {}
    for icon, label, key, mn, mx, df, unit in slider_cfg:
        c1, c2, c3, c4 = st.columns([0.07, 0.19, 0.52, 0.22], gap="small")
        with c1:
            st.markdown(f'<div class="row-icon">{icon}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="row-label">{label}</div>', unsafe_allow_html=True)
        with c3:
            v = st.slider(label, mn, mx, df, key=key, label_visibility="collapsed")
            vals[key] = v
        with c4:
            st.markdown(
                f'<div class="row-right">'
                f'<div class="val-box">{v}</div>'
                f'<div class="val-unit">{unit}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown('</div>', unsafe_allow_html=True)

    st.button("PREDICT TEMPERATURE  →", use_container_width=True)

# ── RIGHT ──
with right:

    load = vals["load"]
    temp = vals["temp"]
    rpm  = vals["rpm"]
    oil  = vals["oil"]

    pred_value = model.predict([[load, temp, rpm, oil]])[0]

    st.markdown(f"""
    <div class="card">
        <div class="sec-title">📊 Prediction Summary</div>
        <div class="pred-num">{pred_value:.1f} <span class="pred-deg">°C</span></div>
        <div class="safe-pill">🟢 &nbsp;Safe</div>
    </div>
    """, unsafe_allow_html=True)

    suggestions = []
    if rpm  > 1400: suggestions.append(("⚠️", "Reduce RPM to control heat"))
    if oil  <   80: suggestions.append(("⚠️", "Oil condition poor – maintenance needed"))
    if load >   65: suggestions.append(("⚠️", "High load – reduce load"))
    if temp >   28: suggestions.append(("⚠️", "High ambient temp – improve cooling"))

    if suggestions:
        pills = "".join(
            f'<div class="warn-pill">{ic} {msg}</div>'
            for ic, msg in suggestions
        )
        st.markdown(f"""
        <div class="card">
            <div class="sec-title">💡 Suggestions</div>
            {pills}
        </div>
        """, unsafe_allow_html=True)

# =====================================================
# ANALYSIS SECTION
# =====================================================

st.markdown('<div class="analysis-bar">📈 Analysis</div>', unsafe_allow_html=True)

g1, g2 = st.columns(2, gap="small")

def make_chart(xdata, ydata, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(4.5, 2.2))
    ax.scatter(xdata, ydata, s=30, color='#3399ff', alpha=0.85, zorder=3)
    ax.set_facecolor("#0a0e1a")
    fig.patch.set_facecolor("#0a0e1a")
    ax.set_title(title, color="white", fontsize=10, fontweight='bold', pad=4)
    ax.set_xlabel(xlabel, color="white", fontsize=9)
    ax.set_ylabel(ylabel, color="white", fontsize=9)
    ax.tick_params(colors='white', labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor("#444444")
        spine.set_linewidth(0.5)
    ax.grid(True, alpha=0.12, color='white', linewidth=0.5)
    fig.tight_layout(pad=0.5)
    return fig

with g1:
    fig1 = make_chart(data['Load'], data['Temperature'],
                      "Temperature vs Load", "Load (%)", "Temperature (°C)")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with g2:
    fig2 = make_chart(data['RPM'], data['Temperature'],
                      "Temperature vs RPM", "RPM", "Temperature (°C)")
    st.markdown('<div class="graph-card">', unsafe_allow_html=True)
    st.pyplot(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================================
# PDF REPORT
# =====================================================

def create_pdf(load, temp, rpm, oil, result):
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc  = SimpleDocTemplate(file.name)
    styles  = getSampleStyleSheet()
    content = [
        Paragraph("THERMOLYTIX REPORT",                      styles['Title']),
        Paragraph(f"Load: {load}",                           styles['Normal']),
        Paragraph(f"Ambient Temp: {temp}",                   styles['Normal']),
        Paragraph(f"RPM: {rpm}",                             styles['Normal']),
        Paragraph(f"Oil Condition: {oil}",                   styles['Normal']),
        Paragraph(f"Predicted Temperature: {result:.2f} °C", styles['Normal']),
    ]
    doc.build(content)
    return file.name

# =====================================================
# DOWNLOAD BUTTON
# =====================================================

st.markdown('<div class="dl-wrap">', unsafe_allow_html=True)
if st.button("📁 Download PDF Report"):
    pdf = create_pdf(load, temp, rpm, oil, pred_value)
    with open(pdf, "rb") as f:
        st.download_button(
            "⬇ Download Report",
            f,
            file_name="thermolytix_report.pdf",
        )
st.markdown('</div>', unsafe_allow_html=True)
