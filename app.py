import json
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from knowledge_base import KnowledgeBase
from inference_engine import ForwardChaining
from backward_chaining import BackwardChaining
from validators import KnowledgeBaseValidator
from report_generator import ReportGenerator


st.set_page_config(
    page_title="Dermalyze",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #f3fbfc;
    --white: #ffffff;
    --ink: #102033;
    --muted: #66758a;
    --line: #d8edf2;
    --teal: #0ea5a8;
    --teal-dark: #087e83;
    --cyan: #14b8d4;
    --blue: #0ea5e9;
    --soft: #e9f8fa;
    --green: #12b981;
    --red: #ef4444;
    --amber: #f59e0b;
    --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
}

* {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 0% 10%, rgba(20,184,212,.17), transparent 28%),
        radial-gradient(circle at 100% 3%, rgba(14,165,168,.12), transparent 24%),
        linear-gradient(180deg, #ecfbfd 0%, #ffffff 48%, #f8fcfd 100%) !important;
    color: var(--ink) !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

div[data-testid="stToolbar"] {
    display: none !important;
}

section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    max-width: 1160px !important;
    padding: 1.1rem 1.2rem 4rem !important;
}

.navbar {
    height: 68px;
    background: rgba(255,255,255,.94);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow);
    margin-bottom: 24px;
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo {
    width: 44px;
    height: 44px;
    border-radius: 16px;
    background: linear-gradient(135deg, var(--teal), var(--cyan));
    color: white;
    display: grid;
    place-items: center;
    font-size: 14px;
    font-weight: 900;
    letter-spacing: -.6px;
}

.brand-title {
    font-size: 19px;
    font-weight: 900;
    color: var(--ink);
    letter-spacing: -.6px;
    line-height: 1.05;
}

.brand-sub {
    font-size: 10.5px;
    font-weight: 800;
    color: var(--muted);
    letter-spacing: .9px;
    text-transform: uppercase;
    margin-top: 3px;
}

.nav-menu {
    display: flex;
    align-items: center;
    gap: 22px;
    color: #334155;
    font-size: 12.5px;
    font-weight: 800;
}

.nav-cta {
    background: linear-gradient(135deg, var(--teal), var(--cyan));
    color: white;
    padding: 12px 18px;
    border-radius: 999px;
    font-weight: 900;
    box-shadow: 0 12px 28px rgba(14,165,168,.22);
}

.hero {
    position: relative;
    min-height: 390px;
    background:
        linear-gradient(90deg, rgba(10,164,166,.95), rgba(20,184,212,.88)),
        radial-gradient(circle at 85% 30%, rgba(255,255,255,.25), transparent 28%);
    border-radius: 42px 42px 42px 12px;
    overflow: hidden;
    box-shadow: 0 28px 70px rgba(14,165,168,.24);
    margin-bottom: 34px;
}

.hero:before {
    content: "";
    position: absolute;
    inset: 0;
    background:
        radial-gradient(circle at 72% 18%, rgba(255,255,255,.35), transparent 12%),
        radial-gradient(circle at 92% 92%, rgba(255,255,255,.23), transparent 21%);
}

.hero-grid {
    position: relative;
    z-index: 2;
    display: grid;
    grid-template-columns: 1.05fr .95fr;
    min-height: 390px;
}

.hero-copy {
    padding: 58px 58px 48px;
    color: white;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,.18);
    border: 1px solid rgba(255,255,255,.35);
    color: white;
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 900;
    margin-bottom: 20px;
}

.hero-dot {
    width: 7px;
    height: 7px;
    border-radius: 99px;
    background: white;
}

.hero-title {
    font-size: 49px;
    line-height: 1.02;
    letter-spacing: -2.2px;
    font-weight: 900;
    color: white;
    margin-bottom: 16px;
    max-width: 540px;
}

.hero-desc {
    max-width: 490px;
    color: rgba(255,255,255,.9);
    font-size: 15px;
    line-height: 1.72;
    font-weight: 600;
    margin-bottom: 25px;
}

.hero-actions {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.hero-primary,
.hero-secondary {
    height: 45px;
    padding: 0 19px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    font-size: 13px;
    font-weight: 900;
}

.hero-primary {
    background: white;
    color: var(--teal-dark);
}

.hero-secondary {
    background: rgba(255,255,255,.15);
    color: white;
    border: 1px solid rgba(255,255,255,.36);
}

.hero-art {
    position: relative;
    min-height: 390px;
}

.doctor-shape {
    position: absolute;
    right: 42px;
    bottom: 0;
    width: 270px;
    height: 335px;
    border-radius: 140px 140px 0 0;
    background: linear-gradient(180deg, #ffffff 0%, #e6f7fb 100%);
    box-shadow: 0 24px 60px rgba(15,23,42,.13);
}

.doctor-head {
    position: absolute;
    top: 35px;
    left: 94px;
    width: 82px;
    height: 82px;
    border-radius: 50%;
    background: #f2c9ad;
}

.doctor-hair {
    position: absolute;
    top: 25px;
    left: 95px;
    width: 84px;
    height: 45px;
    border-radius: 50px 50px 18px 18px;
    background: #24364c;
}

.doctor-body {
    position: absolute;
    left: 55px;
    bottom: 0;
    width: 160px;
    height: 205px;
    border-radius: 42px 42px 0 0;
    background: white;
}

.steth {
    position: absolute;
    left: 88px;
    bottom: 85px;
    width: 92px;
    height: 92px;
    border: 8px solid #0ea5a8;
    border-top: 0;
    border-radius: 0 0 70px 70px;
    opacity: .75;
}

.float-card {
    position: absolute;
    left: 18px;
    width: 195px;
    height: 54px;
    border-radius: 16px;
    background: rgba(255,255,255,.92);
    box-shadow: 0 16px 35px rgba(15,23,42,.14);
    border: 1px solid rgba(255,255,255,.78);
}

.float-card.one { top: 78px; }
.float-card.two { top: 155px; left: 48px; }
.float-card.three { top: 232px; }

.float-card:before {
    content: "";
    position: absolute;
    left: 15px;
    top: 17px;
    width: 20px;
    height: 20px;
    border-radius: 999px;
    background: var(--teal);
}

.float-card:after {
    content: "";
    position: absolute;
    left: 47px;
    top: 17px;
    width: 120px;
    height: 8px;
    border-radius: 99px;
    background: #d7e8ee;
    box-shadow: 0 15px 0 #edf5f7;
}

.section-title {
    text-align: center;
    font-size: 27px;
    line-height: 1.15;
    font-weight: 900;
    letter-spacing: -1px;
    color: var(--ink);
    margin: 8px 0 22px;
}

.features {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 34px;
}

.feature {
    background: white;
    border: 1px solid var(--line);
    border-radius: 28px;
    padding: 23px;
    min-height: 180px;
    box-shadow: 0 14px 38px rgba(15,23,42,.06);
    transition: .18s ease;
}

.feature:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 48px rgba(15,23,42,.08);
}

.feature-icon {
    width: 54px;
    height: 54px;
    border-radius: 20px;
    background: #e0f7f9;
    color: var(--teal);
    display: grid;
    place-items: center;
    margin-bottom: 18px;
}

.feature-title {
    font-size: 15px;
    font-weight: 900;
    color: var(--ink);
    margin-bottom: 8px;
}

.feature-text {
    color: var(--muted);
    font-size: 12.5px;
    line-height: 1.65;
    font-weight: 600;
}

.notice {
    background: #fff8ed;
    border: 1px solid #fed7aa;
    color: #7c2d12;
    border-radius: 18px;
    padding: 14px 17px;
    font-size: 12.8px;
    line-height: 1.65;
    font-weight: 700;
    margin-bottom: 24px;
}

.screening-card {
    background: white;
    border: 1px solid var(--line);
    border-radius: 30px;
    padding: 26px;
    box-shadow: 0 18px 50px rgba(15,23,42,.07);
    margin-bottom: 28px;
}

.card-head {
    display: flex;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 20px;
}

.card-title {
    color: var(--ink);
    font-size: 23px;
    letter-spacing: -.7px;
    font-weight: 900;
    margin-bottom: 5px;
}

.card-sub {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
    font-weight: 600;
}

.step-pill {
    height: 35px;
    padding: 0 13px;
    border-radius: 999px;
    background: #e0f7f9;
    color: var(--teal-dark);
    border: 1px solid #bdecef;
    display: flex;
    align-items: center;
    font-size: 12px;
    font-weight: 900;
    white-space: nowrap;
}

.q-card {
    background: #fbfdfe;
    border: 1px solid var(--line);
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 11px;
}

.q-top {
    display: flex;
    gap: 8px;
    margin-bottom: 10px;
}

.q-id,
.q-cat {
    height: 25px;
    padding: 0 9px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    font-size: 11px;
    font-weight: 900;
}

.q-id {
    background: #e0f2fe;
    color: #0369a1;
}

.q-cat {
    background: #dcfce7;
    color: #166534;
}

.q-text {
    color: var(--ink);
    font-size: 14px;
    line-height: 1.58;
    font-weight: 800;
}

.result-box {
    border: 1px solid;
    border-radius: 22px;
    padding: 20px;
    margin-bottom: 16px;
}

.result-high {
    background: #fff1f2;
    border-color: #fecdd3;
    color: #881337;
}

.result-medium {
    background: #fffbeb;
    border-color: #fde68a;
    color: #78350f;
}

.result-low {
    background: #ecfdf5;
    border-color: #a7f3d0;
    color: #064e3b;
}

.result-label {
    font-size: 12px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: .7px;
    margin-bottom: 8px;
}

.result-name {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -.7px;
    margin-bottom: 10px;
}

.result-meta {
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 5px;
}

.result-desc {
    margin-top: 10px;
    font-size: 13px;
    line-height: 1.65;
    font-weight: 650;
}

.rank {
    background: #fbfdfe;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 9px;
}

.rank-top {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 8px;
}

.rank-name {
    color: var(--ink);
    font-size: 13px;
    font-weight: 900;
}

.rank-score {
    color: var(--teal);
    font-size: 13px;
    font-weight: 900;
    white-space: nowrap;
}

.track {
    height: 7px;
    background: #e1f6f8;
    border-radius: 999px;
    overflow: hidden;
}

.fill {
    height: 100%;
    background: linear-gradient(90deg, var(--teal), var(--cyan));
}

.info-item {
    background: #fbfdfe;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 13px;
    margin-bottom: 9px;
}

.info-top {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 7px;
}

.info-id {
    color: var(--teal-dark);
    font-size: 12px;
    font-weight: 900;
}

.info-cf {
    color: #16a34a;
    font-size: 12px;
    font-weight: 900;
}

.info-text {
    color: #415268;
    font-size: 13px;
    line-height: 1.6;
    font-weight: 650;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    font-weight: 800;
    padding: 22px 0 5px;
    border-top: 1px solid var(--line);
}

svg {
    width: 28px;
    height: 28px;
    stroke-width: 2.2;
}

/* Streamlit overrides */
div[data-testid="stTabs"] > div > div > div {
    background: #f8fcfd !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    padding: 4px !important;
    gap: 4px !important;
}

div[data-testid="stTabs"] button {
    color: #5f7086 !important;
    font-size: 13px !important;
    font-weight: 800 !important;
    border-radius: 13px !important;
    padding: 10px 16px !important;
    background: transparent !important;
    border: none !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, var(--teal), var(--cyan)) !important;
    color: white !important;
}

div[data-testid="stTabsContent"] {
    padding-top: 18px !important;
}

div[data-baseweb="select"] > div {
    background: white !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
    color: var(--ink) !important;
    min-height: 44px !important;
}

div[data-baseweb="select"] span {
    color: var(--ink) !important;
}

textarea,
input {
    background: white !important;
    color: var(--ink) !important;
    border: 1px solid var(--line) !important;
    border-radius: 14px !important;
}

textarea::placeholder,
input::placeholder {
    color: #9aa9ba !important;
}

label[data-testid="stWidgetLabel"] p {
    color: #405268 !important;
    font-size: 13px !important;
    font-weight: 800 !important;
}

div[data-testid="stRadio"] > div {
    gap: 8px !important;
    flex-wrap: wrap !important;
}

div[data-testid="stRadio"] label {
    background: white !important;
    border: 1px solid var(--line) !important;
    border-radius: 13px !important;
    padding: 7px 13px !important;
    min-width: 122px !important;
    cursor: pointer !important;
}

div[data-testid="stRadio"] label p {
    color: #24364c !important;
    font-size: 12.5px !important;
    font-weight: 800 !important;
}

div[data-testid="stRadio"] input {
    accent-color: var(--teal) !important;
}

div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid var(--line) !important;
    border-radius: 18px !important;
    box-shadow: none !important;
    overflow: hidden !important;
}

div[data-testid="stExpander"] summary {
    background: white !important;
    color: var(--ink) !important;
    font-weight: 900 !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--teal), var(--cyan)) !important;
    color: white !important;
    border: none !important;
    border-radius: 15px !important;
    padding: .85rem 1rem !important;
    font-size: 14px !important;
    font-weight: 900 !important;
    box-shadow: 0 14px 28px rgba(14,165,168,.22) !important;
}

.stButton > button:hover {
    color: white !important;
    filter: brightness(1.05) !important;
}

.stDownloadButton > button {
    width: 100%;
    background: #f8fcfd !important;
    color: var(--ink) !important;
    border: 1px solid var(--line) !important;
    border-radius: 15px !important;
    font-weight: 900 !important;
}

div[data-testid="stMetric"] {
    background: #fbfdfe !important;
    border: 1px solid var(--line) !important;
    border-radius: 15px !important;
    padding: 12px !important;
}

div[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-weight: 800 !important;
}

div[data-testid="stMetricValue"] {
    color: var(--teal) !important;
    font-weight: 900 !important;
}

code {
    white-space: pre-wrap !important;
}

@media (max-width: 980px) {
    .hero-grid {
        grid-template-columns: 1fr;
    }

    .hero-art {
        display: none;
    }

    .features {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .hero-copy {
        padding: 42px 34px;
    }

    .hero-title {
        font-size: 40px;
    }

    .nav-menu span {
        display: none;
    }
}

@media (max-width: 680px) {
    .block-container {
        padding: .7rem !important;
    }

    .navbar {
        height: auto;
        border-radius: 24px;
        align-items: flex-start;
        flex-direction: column;
        padding: 14px;
    }

    .hero {
        border-radius: 30px;
    }

    .hero-copy {
        padding: 32px 24px;
    }

    .hero-title {
        font-size: 34px;
        letter-spacing: -1.4px;
    }

    .features {
        grid-template-columns: 1fr;
    }

    .screening-card {
        padding: 18px;
        border-radius: 24px;
    }

    .card-head {
        flex-direction: column;
    }

    div[data-testid="stRadio"] label {
        min-width: 100% !important;
    }
}
</style>
""", unsafe_allow_html=True)


def svg_scan():
    return """
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M4 7V5a1 1 0 0 1 1-1h2"/>
        <path d="M17 4h2a1 1 0 0 1 1 1v2"/>
        <path d="M20 17v2a1 1 0 0 1-1 1h-2"/>
        <path d="M7 20H5a1 1 0 0 1-1-1v-2"/>
        <path d="M8 12h8"/>
        <path d="M12 8v8"/>
    </svg>
    """


def svg_rule():
    return """
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M8 6h12"/>
        <path d="M8 12h12"/>
        <path d="M8 18h12"/>
        <path d="M4 6h.01"/>
        <path d="M4 12h.01"/>
        <path d="M4 18h.01"/>
    </svg>
    """


def svg_chart():
    return """
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M4 19V5"/>
        <path d="M4 19h16"/>
        <path d="M8 16v-4"/>
        <path d="M12 16V8"/>
        <path d="M16 16v-6"/>
    </svg>
    """


def svg_history():
    return """
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M3 12a9 9 0 1 0 3-6.7"/>
        <path d="M3 4v5h5"/>
        <path d="M12 7v5l3 2"/>
    </svg>
    """


@st.cache_resource
def init_system():
    kb = KnowledgeBase()
    fc = ForwardChaining(kb)
    bc = BackwardChaining(kb)
    validator = KnowledgeBaseValidator(kb)
    return kb, fc, bc, validator


kb, fc, bc, validator = init_system()
validation = validator.validate()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "hasil" not in st.session_state:
    st.session_state.hasil = None

if "sesi" not in st.session_state:
    st.session_state.sesi = None


CF_MAP = {
    "Tidak": 0.0,
    "Kurang Yakin": 0.4,
    "Cukup Yakin": 0.8,
    "Sangat Yakin": 1.0
}

CF_LABEL = {
    0.0: "Tidak",
    0.4: "Kurang Yakin",
    0.8: "Cukup Yakin",
    1.0: "Sangat Yakin"
}


def result_class(value):
    if value >= 70:
        return "result-high"
    if value >= 40:
        return "result-medium"
    return "result-low"


def result_label(value):
    if value >= 70:
        return "Risiko Tinggi"
    if value >= 40:
        return "Risiko Sedang"
    return "Risiko Rendah"


def make_gauge(value):
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%", "font": {"size": 32, "color": "#102033"}},
            title={"text": "Certainty Factor", "font": {"size": 14, "color": "#66758a"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"size": 11}},
                "bar": {"color": "#0ea5a8", "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "steps": [
                    {"range": [0, 40], "color": "#dcfce7"},
                    {"range": [40, 70], "color": "#fef3c7"},
                    {"range": [70, 100], "color": "#fee2e2"}
                ],
                "threshold": {
                    "line": {"color": "#102033", "width": 3},
                    "thickness": 0.72,
                    "value": value
                }
            }
        )
    )
    fig.update_layout(
        height=230,
        margin=dict(l=8, r=8, t=36, b=6),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig


st.markdown("""
<div class="navbar">
    <div class="brand">
        <div class="logo">DM</div>
        <div>
            <div class="brand-title">Dermalyze</div>
            <div class="brand-sub">Skin Expert System</div>
        </div>
    </div>
    <div class="nav-menu">
        <span>Beranda</span>
        <span>Skrining</span>
        <span>Metode</span>
        <span>Edukasi</span>
        <div class="nav-cta">Mulai Skrining</div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="hero">
    <div class="hero-grid">
        <div class="hero-copy">
            <div class="hero-badge"><span class="hero-dot"></span> Sistem Pakar Skrining Kulit</div>
            <div class="hero-title">Cek risiko lesi kulit, lebih awal dan lebih terarah.</div>
            <div class="hero-desc">
                Dermalyze membantu menganalisis gejala lesi kulit menggunakan Forward Chaining,
                Backward Chaining, dan Certainty Factor berbasis rule klinis.
            </div>
            <div class="hero-actions">
                <div class="hero-primary">Mulai Analisis</div>
                <div class="hero-secondary">Lihat Metode</div>
            </div>
        </div>

        <div class="hero-art">
            <div class="float-card one"></div>
            <div class="float-card two"></div>
            <div class="float-card three"></div>
            <div class="doctor-shape">
                <div class="doctor-hair"></div>
                <div class="doctor-head"></div>
                <div class="doctor-body"></div>
                <div class="steth"></div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="section-title">Fitur Utama Dermalyze</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="features">
    <div class="feature">
        <div class="feature-icon">{svg_scan()}</div>
        <div class="feature-title">Skrining Gejala</div>
        <div class="feature-text">Kuesioner gejala berdasarkan kategori ABCDE, sensasi, bentuk lesi, dan faktor risiko.</div>
    </div>
    <div class="feature">
        <div class="feature-icon">{svg_rule()}</div>
        <div class="feature-title">Rule IF-THEN</div>
        <div class="feature-text">Basis pengetahuan terdiri dari gejala, diagnosis, dan aturan pakar yang dapat ditelusuri.</div>
    </div>
    <div class="feature">
        <div class="feature-icon">{svg_chart()}</div>
        <div class="feature-title">Certainty Factor</div>
        <div class="feature-text">Sistem menghitung tingkat keyakinan hasil berdasarkan bobot user dan bobot pakar.</div>
    </div>
    <div class="feature">
        <div class="feature-icon">{svg_history()}</div>
        <div class="feature-title">Riwayat Sesi</div>
        <div class="feature-text">Hasil konsultasi tersimpan selama sesi aplikasi masih berjalan.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
    <b>Peringatan medis:</b> Dermalyze adalah prototype akademis untuk skrining awal, bukan pengganti diagnosis dokter.
    Segera konsultasi ke dokter spesialis kulit apabila lesi berubah, berdarah, nyeri, atau tidak sembuh lebih dari 4 minggu.
</div>
""", unsafe_allow_html=True)


with st.container():
    st.markdown('<div class="screening-card">', unsafe_allow_html=True)

    tab_screening, tab_result, tab_explain, tab_backward, tab_education, tab_history = st.tabs([
        "Skrining",
        "Hasil",
        "Penjelasan",
        "Backward",
        "Edukasi",
        "Riwayat"
    ])

    with tab_screening:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Form Skrining Lesi Kulit</div>
                <div class="card-sub">Isi data singkat, lalu jawab pertanyaan sesuai kondisi lesi atau tahi lalat.</div>
            </div>
            <div class="step-pill">Step 1 of 2</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Data Singkat Lesi", expanded=True):
            col1, col2, col3 = st.columns(3)

            with col1:
                lokasi = st.selectbox(
                    "Lokasi lesi",
                    ["Wajah", "Leher", "Tangan", "Lengan", "Punggung", "Dada", "Kaki", "Area lain"]
                )

            with col2:
                lama = st.selectbox(
                    "Lama muncul",
                    ["Kurang dari 1 minggu", "1–4 minggu", "Lebih dari 4 minggu", "Lebih dari 3 bulan", "Tidak ingat"]
                )

            with col3:
                perubahan = st.selectbox(
                    "Perubahan terakhir",
                    ["Tidak ada perubahan", "Membesar", "Berubah warna", "Berdarah", "Nyeri/gatal", "Tidak yakin"]
                )

            catatan = st.text_area(
                "Catatan tambahan",
                placeholder="Contoh: muncul di tangan kanan, kadang gatal, warnanya makin gelap...",
                height=82
            )

        gejala_all = kb.get_semua_gejala()
        kategori_list = list(dict.fromkeys(item["kategori"] for item in gejala_all))
        kategori_tabs = st.tabs(kategori_list)

        jawaban = {}

        for kategori_tab, kategori in zip(kategori_tabs, kategori_list):
            with kategori_tab:
                daftar_gejala = [item for item in gejala_all if item["kategori"] == kategori]

                for gejala in daftar_gejala:
                    st.markdown(f"""
                    <div class="q-card">
                        <div class="q-top">
                            <span class="q-id">{gejala["id"]}</span>
                            <span class="q-cat">{gejala["kategori"]}</span>
                        </div>
                        <div class="q-text">{gejala["pertanyaan"]}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    pilihan = st.radio(
                        label=f"Jawaban {gejala['id']}",
                        options=["Tidak", "Kurang Yakin", "Cukup Yakin", "Sangat Yakin"],
                        horizontal=True,
                        key=f"q_{gejala['id']}",
                        label_visibility="collapsed"
                    )

                    jawaban[gejala["id"]] = CF_MAP[pilihan]

        if st.button("Proses Analisis Sekarang", type="primary", use_container_width=True):
            gejala_aktif = [gid for gid, nilai in jawaban.items() if nilai > 0]

            if len(gejala_aktif) < 2:
                st.error("Pilih minimal 2 gejala selain 'Tidak' untuk memulai analisis.")
            else:
                fc.reset()
                fc.set_fakta(gejala_aktif)
                hasil = fc.run_analysis(jawaban)

                sesi = {
                    "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                    "lokasi": lokasi,
                    "lama": lama,
                    "perubahan": perubahan,
                    "catatan": catatan,
                    "aktif": gejala_aktif,
                    "jawaban": jawaban,
                    "hasil": hasil,
                    "log": fc.jalur_inferensi.copy()
                }

                st.session_state.hasil = hasil
                st.session_state.sesi = sesi
                st.session_state.riwayat.append(sesi)

                st.success("Analisis selesai. Buka tab Hasil untuk melihat ringkasan diagnosis.")

    with tab_result:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Hasil Analisis</div>
                <div class="card-sub">Ringkasan diagnosis berdasarkan rule aktif dan nilai Certainty Factor.</div>
            </div>
            <div class="step-pill">Result</div>
        </div>
        """, unsafe_allow_html=True)

        hasil = st.session_state.hasil
        sesi = st.session_state.sesi

        if hasil is None:
            st.info("Belum ada hasil. Jalankan skrining terlebih dahulu.")
        elif not hasil:
            st.markdown("""
            <div class="result-box result-low">
                <div class="result-label">Risiko Rendah</div>
                <div class="result-name">Tidak Ada Rule Aktif</div>
                <div class="result-desc">
                    Gejala yang dipilih belum memicu rule apa pun. Tetap lakukan pemantauan mandiri dan gunakan perlindungan kulit.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            diagnosis_utama = hasil[0]
            persentase = diagnosis_utama.persentase

            col_a, col_b = st.columns([1.25, 1])

            with col_a:
                st.markdown(f"""
                <div class="result-box {result_class(persentase)}">
                    <div class="result-label">{result_label(persentase)}</div>
                    <div class="result-name">{diagnosis_utama.nama}</div>
                    <div class="result-meta">Nilai keyakinan: <b>{persentase:.1f}%</b></div>
                    <div class="result-meta">Tingkat risiko: <b>{diagnosis_utama.tingkat_risiko}</b></div>
                    <div class="result-desc">{diagnosis_utama.deskripsi}</div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("#### Saran Tindakan")
                for saran in diagnosis_utama.saran:
                    st.write(f"• {saran}")

            with col_b:
                st.plotly_chart(make_gauge(persentase), use_container_width=True)

            st.markdown("#### Ranking Diagnosis")
            for item in hasil[:5]:
                width = max(2, min(100, int(item.persentase)))
                st.markdown(f"""
                <div class="rank">
                    <div class="rank-top">
                        <span class="rank-name">{item.nama}</span>
                        <span class="rank-score">{item.persentase:.1f}%</span>
                    </div>
                    <div class="track">
                        <div class="fill" style="width:{width}%"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            if sesi:
                with st.expander("Ringkasan Input"):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Lokasi", sesi["lokasi"])
                    c2.metric("Lama", sesi["lama"])
                    c3.metric("Perubahan", sesi["perubahan"])
                    st.write(f"**Gejala aktif:** {', '.join(sesi['aktif'])}")
                    if sesi["catatan"]:
                        st.write(f"**Catatan:** {sesi['catatan']}")

                laporan = ReportGenerator.generate_text_report({
                    "waktu": sesi["waktu"],
                    "lokasi_lesi": sesi["lokasi"],
                    "lama_lesi": sesi["lama"],
                    "perubahan_lesi": sesi["perubahan"],
                    "gejala_aktif": sesi["aktif"],
                    "hasil": sesi["hasil"]
                })

                st.download_button(
                    "Unduh Laporan Hasil",
                    data=laporan,
                    file_name=f"dermalyze_{sesi['waktu'].replace(':', '-').replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    with tab_explain:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Explanation Facility</div>
                <div class="card-sub">Menampilkan gejala aktif, rule aktif, CF evidence, dan jalur inferensi.</div>
            </div>
            <div class="step-pill">Trace</div>
        </div>
        """, unsafe_allow_html=True)

        hasil = st.session_state.hasil
        sesi = st.session_state.sesi

        if hasil is None or sesi is None:
            st.info("Jalankan skrining terlebih dahulu.")
        else:
            st.markdown("#### Gejala Aktif")
            for gid in sesi["aktif"]:
                data_gejala = kb.gejala.get(gid, {})
                nilai = sesi["jawaban"].get(gid, 0)

                st.markdown(f"""
                <div class="info-item">
                    <div class="info-top">
                        <span class="info-id">{gid}</span>
                        <span class="info-cf">{CF_LABEL.get(nilai, "-")} ({nilai})</span>
                    </div>
                    <div class="info-text">{data_gejala.get("pertanyaan", "-")}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            if not hasil:
                st.warning("Tidak ada rule yang aktif.")
            else:
                diagnosis_utama = hasil[0]

                c1, c2, c3 = st.columns(3)
                c1.metric("Diagnosis", diagnosis_utama.nama[:20] + "..." if len(diagnosis_utama.nama) > 20 else diagnosis_utama.nama)
                c2.metric("CF Final", f"{diagnosis_utama.cf_final:.4f}")
                c3.metric("Keyakinan", f"{diagnosis_utama.persentase:.1f}%")

                st.markdown("#### Rule Aktif")
                for detail in diagnosis_utama.detail_cf:
                    rule_id = detail["rule_id"]
                    rule_data = next((rule for rule in kb.rules if rule["id"] == rule_id), None)

                    with st.expander(f"{rule_id} · CF Evidence {detail['cf_evidence']:.4f}"):
                        if rule_data:
                            st.write(f"**IF:** {' AND '.join(rule_data['kondisi'])}")
                            st.write(f"**THEN:** {rule_data['kesimpulan']}")
                            st.write(f"**CF Pakar:** {rule_data['cf_pakar']}")
                            st.write(f"**Alasan:** {rule_data.get('alasan', '-')}")
                        st.write(f"**CF User Terendah:** {detail['cf_user_terendah']}")
                        st.write(f"**CF Evidence:** {detail['cf_evidence']:.4f}")

                st.markdown("#### Log Forward Chaining")
                st.code("\n".join(sesi["log"]), language="text")

    with tab_backward:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Backward Chaining</div>
                <div class="card-sub">Verifikasi diagnosis dari tujuan ke gejala pendukung.</div>
            </div>
            <div class="step-pill">Bonus</div>
        </div>
        """, unsafe_allow_html=True)

        sesi = st.session_state.sesi
        opsi = {pid: penyakit["nama"] for pid, penyakit in kb.penyakit.items()}

        pilihan_diagnosis = st.selectbox(
            "Pilih diagnosis untuk diverifikasi",
            list(opsi.keys()),
            format_func=lambda item: opsi[item]
        )

        if sesi:
            st.info(f"Gejala sesi terakhir: {', '.join(sesi['aktif'])}")
        else:
            st.warning("Jalankan skrining terlebih dahulu sebelum verifikasi.")

        if st.button("Jalankan Verifikasi Backward Chaining", use_container_width=True):
            if not sesi:
                st.error("Belum ada sesi konsultasi.")
            else:
                hasil_backward = bc.verify_diagnosis(pilihan_diagnosis, sesi["aktif"])

                if not hasil_backward:
                    st.warning("Tidak ada rule terkait diagnosis ini.")
                else:
                    terpenuhi = sum(1 for item in hasil_backward if item["terpenuhi"])
                    total = len(hasil_backward)

                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Rule", total)
                    c2.metric("Terpenuhi", terpenuhi)
                    c3.metric("Status", "Terverifikasi" if terpenuhi > 0 else "Belum Terverifikasi")

                    for item in hasil_backward:
                        status = "Terpenuhi" if item["terpenuhi"] else "Belum Terpenuhi"
                        with st.expander(f"Rule {item['rule_id']} · {status}"):
                            st.write(f"**Kondisi:** {' AND '.join(item['kondisi'])}")
                            if item["kekurangan"]:
                                st.write(f"**Gejala kurang:** {', '.join(item['kekurangan'])}")
                            else:
                                st.write("Semua gejala pada rule ini terpenuhi.")

    with tab_education:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Edukasi Kesehatan Kulit</div>
                <div class="card-sub">Informasi singkat untuk membantu pengguna memahami skrining awal.</div>
            </div>
            <div class="step-pill">Info</div>
        </div>
        """, unsafe_allow_html=True)

        path_edukasi = Path("data/edukasi.json")

        try:
            with open(path_edukasi, "r", encoding="utf-8") as file:
                edukasi = json.load(file).get("edukasi", [])
        except Exception:
            edukasi = [
                {
                    "judul": "ABCDE pada Tahi Lalat",
                    "isi": "ABCDE adalah panduan awal untuk memeriksa asimetri, batas, warna, diameter, dan perubahan lesi."
                },
                {
                    "judul": "Perlindungan UV",
                    "isi": "Gunakan sunscreen, pakaian pelindung, dan hindari paparan matahari berlebihan."
                },
                {
                    "judul": "Kapan ke Dokter",
                    "isi": "Segera periksa jika lesi berubah, berdarah, nyeri, atau tidak sembuh lebih dari 4 minggu."
                }
            ]

        for item in edukasi:
            st.markdown(f"""
            <div class="info-item">
                <div class="info-top">
                    <span class="info-id">{item["judul"]}</span>
                </div>
                <div class="info-text">{item["isi"]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("#### Status Knowledge Base")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Gejala", validation["jumlah_gejala"])
        c2.metric("Diagnosis", validation["jumlah_penyakit"])
        c3.metric("Rules", validation["jumlah_rules"])
        c4.metric("Status", "Valid" if validation["valid"] else f"{len(validation['errors'])} Error")

        if not validation["valid"]:
            for error in validation["errors"]:
                st.error(error)

    with tab_history:
        st.markdown("""
        <div class="card-head">
            <div>
                <div class="card-title">Riwayat Konsultasi</div>
                <div class="card-sub">Riwayat tersimpan selama sesi aplikasi masih berjalan.</div>
            </div>
            <div class="step-pill">Session</div>
        </div>
        """, unsafe_allow_html=True)

        riwayat = st.session_state.riwayat

        if not riwayat:
            st.info("Belum ada riwayat konsultasi.")
        else:
            col_total, col_button = st.columns([3, 1])
            col_total.metric("Total Sesi", len(riwayat))

            with col_button:
                if st.button("Hapus Riwayat", use_container_width=True):
                    st.session_state.riwayat = []
                    st.session_state.hasil = None
                    st.session_state.sesi = None
                    st.rerun()

            for index, item in enumerate(reversed(riwayat), start=1):
                hasil_utama = item["hasil"][0] if item["hasil"] else None
                nama = hasil_utama.nama if hasil_utama else "Tidak ada rule aktif"
                cf = f"{hasil_utama.persentase:.1f}%" if hasil_utama else "-"

                st.markdown(f"""
                <div class="info-item">
                    <div class="info-top">
                        <span class="info-id">#{index} — {nama}</span>
                        <span class="info-cf">{item["waktu"]}</span>
                    </div>
                    <div class="info-text">
                        Lokasi: {item["lokasi"]} · Lama: {item["lama"]} · Perubahan: {item["perubahan"]}<br>
                        CF: {cf} · Gejala aktif: {', '.join(item["aktif"][:6])}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    Dermalyze · Sistem Pakar Skrining Risiko Lesi Kulit · UAS Sistem Pakar
</div>
""", unsafe_allow_html=True)