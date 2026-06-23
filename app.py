import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

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
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300..700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap" rel="stylesheet">

<style>
:root {
    --primary: #0891b2;
    --primary-dark: #0e7490;
    --primary-light: #e0f2fe;
    --primary-xlight: #f0f9ff;
    --ink: #0f172a;
    --ink-muted: #475569;
    --ink-faint: #94a3b8;
    --surface: #ffffff;
    --surface-2: #f8fafc;
    --border: rgba(15,23,42,0.08);
    --border-strong: rgba(15,23,42,0.14);
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 24px;
    --radius-xl: 32px;
    --shadow-sm: 0 1px 3px rgba(15,23,42,0.06), 0 1px 2px rgba(15,23,42,0.04);
    --shadow-md: 0 4px 16px rgba(15,23,42,0.07), 0 2px 6px rgba(15,23,42,0.04);
    --shadow-lg: 0 12px 36px rgba(15,23,42,0.10), 0 4px 12px rgba(15,23,42,0.05);
    --transition: 180ms cubic-bezier(0.16, 1, 0.3, 1);
}

*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: linear-gradient(160deg, #e0f7fa 0%, #f0fdf4 50%, #e0f2fe 100%) !important;
    font-family: 'Inter', -apple-system, sans-serif !important;
    color: var(--ink) !important;
}

.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp h5,.stApp h6,.stApp p,.stApp label,.stMarkdown p,.stMarkdown span {
    font-family: 'Inter', -apple-system, sans-serif !important;
}

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
section[data-testid="stSidebar"],
#MainMenu { display: none !important; }

.block-container {
    max-width: 1080px !important;
    padding: 0 1.5rem 5rem !important;
    margin: 0 auto !important;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: 9999px;
    padding: 10px 10px 10px 16px;
    box-shadow: var(--shadow-sm);
    margin: 24px 0 28px;
    position: sticky;
    top: 12px;
    z-index: 100;
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.topbar-logo {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-weight: 800;
    font-size: 14px;
    letter-spacing: -0.5px;
    box-shadow: 0 4px 12px rgba(8,145,178,0.3);
}

.topbar-name {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 17px;
    font-weight: 800;
    color: var(--ink);
    letter-spacing: -0.3px;
}

.topbar-sub {
    font-size: 11px;
    color: var(--ink-faint);
    font-weight: 500;
    margin-top: 1px;
}

.topbar-badge {
    background: var(--primary-light);
    color: var(--primary-dark);
    font-size: 12px;
    font-weight: 700;
    padding: 7px 16px;
    border-radius: 9999px;
    letter-spacing: 0.2px;
}

.hero-card {
    background: rgba(255,255,255,0.65);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: var(--radius-xl);
    padding: 60px 32px 52px;
    text-align: center;
    box-shadow: var(--shadow-md);
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 400px; height: 200px;
    background: radial-gradient(ellipse at center, rgba(8,145,178,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface);
    color: var(--primary-dark);
    font-size: 12px;
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 9999px;
    border: 1px solid var(--border);
    margin-bottom: 22px;
    box-shadow: var(--shadow-sm);
    letter-spacing: 0.2px;
}

.hero-badge::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--primary);
    display: inline-block;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: clamp(28px, 4vw, 44px) !important;
    font-weight: 800 !important;
    color: var(--ink) !important;
    margin-bottom: 16px !important;
    line-height: 1.15 !important;
    letter-spacing: -1.5px !important;
}

.hero-desc {
    font-size: 15px !important;
    color: var(--ink-muted) !important;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.7 !important;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}

.stat-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: var(--radius-md);
    padding: 22px 16px;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: transform var(--transition), box-shadow var(--transition);
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.stat-icon-wrap {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--primary-light);
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px;
}

.stat-icon-wrap svg {
    width: 22px;
    height: 22px;
    stroke: var(--primary-dark);
    fill: none;
    stroke-width: 2;
    stroke-linecap: round;
    stroke-linejoin: round;
}

.stat-title {
    font-size: 13px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 3px;
}

.stat-value {
    font-size: 11px;
    color: var(--ink-faint);
    font-weight: 500;
}

div[data-testid="stTabs"] > div:first-child {
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(12px) !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--border) !important;
    padding: 6px !important;
    gap: 4px !important;
    box-shadow: var(--shadow-sm) !important;
    margin-bottom: 20px !important;
}

div[data-testid="stTabs"] button {
    color: var(--ink-muted) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    border-radius: 10px !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all var(--transition) !important;
}

div[data-testid="stTabs"] button:hover {
    color: var(--ink) !important;
    background: rgba(255,255,255,0.8) !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: var(--surface) !important;
    color: var(--primary-dark) !important;
    box-shadow: var(--shadow-sm) !important;
    font-weight: 700 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"]::after {
    display: none !important;
}

.dm-card {
    background: rgba(255,255,255,0.82);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 28px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 20px;
}

.dm-card-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 17px;
    font-weight: 800;
    color: var(--ink);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.dm-card-title-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--primary);
    flex-shrink: 0;
}

.warn-banner {
    background: #fffbeb;
    border: 1px solid #fcd34d;
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 20px;
}

.warn-banner-icon {
    font-size: 16px;
    flex-shrink: 0;
    margin-top: 1px;
}

.warn-banner-text {
    font-size: 13.5px;
    color: #78350f;
    font-weight: 500;
    line-height: 1.55;
}

input, textarea {
    background: var(--surface) !important;
    color: var(--ink) !important;
    border: 1.5px solid var(--border-strong) !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color var(--transition), box-shadow var(--transition) !important;
}

input:focus, textarea:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(8,145,178,0.12) !important;
    outline: none !important;
}

div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    color: var(--ink) !important;
    border: 1.5px solid var(--border-strong) !important;
    border-radius: 10px !important;
}

details[data-testid="stExpander"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    margin-bottom: 10px !important;
}

details[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    font-size: 14px !important;
    color: var(--ink) !important;
    padding: 14px 18px !important;
}

details[data-testid="stExpander"] summary:hover {
    background: rgba(8,145,178,0.04) !important;
    border-radius: var(--radius-sm) !important;
}

.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px 24px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 4px 14px rgba(8,145,178,0.3) !important;
    letter-spacing: 0.1px !important;
    transition: all var(--transition) !important;
    font-family: 'Inter', sans-serif !important;
}

.stButton > button:hover {
    background: var(--primary-dark) !important;
    box-shadow: 0 6px 20px rgba(8,145,178,0.4) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 8px rgba(8,145,178,0.3) !important;
}

.stDownloadButton > button {
    background: var(--surface-2) !important;
    color: var(--primary-dark) !important;
    border: 1.5px solid var(--border-strong) !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 700 !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all var(--transition) !important;
}

.stDownloadButton > button:hover {
    background: var(--primary-light) !important;
    border-color: var(--primary) !important;
}

.result-card {
    background: var(--surface);
    border-radius: var(--radius-lg);
    padding: 32px;
    margin-top: 24px;
    margin-bottom: 24px;
    border-left: 5px solid;
    box-shadow: var(--shadow-lg);
    animation: slideIn 0.35s cubic-bezier(0.16,1,0.3,1) both;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.high-risk { border-color: #ef4444; }
.med-risk  { border-color: #f59e0b; }
.low-risk  { border-color: #10b981; }

.progress-wrap {
    background: rgba(255,255,255,0.85);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    margin-bottom: 10px;
    box-shadow: var(--shadow-sm);
}

.progress-bar-bg {
    height: 7px;
    background: #e2e8f0;
    border-radius: 99px;
    overflow: hidden;
    margin-top: 10px;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--primary), #06b6d4);
    transition: width 0.6s cubic-bezier(0.16,1,0.3,1);
}

.rule-trace {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px;
    margin-bottom: 10px;
}

.rule-trace-header {
    font-weight: 700;
    font-size: 13px;
    margin-bottom: 6px;
    color: var(--primary-dark);
}

.rule-trace-body {
    font-size: 13px;
    color: var(--ink-muted);
    line-height: 1.55;
}

.history-entry {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 18px 22px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
    transition: box-shadow var(--transition);
}

.history-entry:hover {
    box-shadow: var(--shadow-md);
}

.history-name {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 800;
    font-size: 16px;
    margin-bottom: 5px;
    color: var(--ink);
}

.history-meta {
    font-size: 12.5px;
    color: var(--ink-faint);
}

.history-pct {
    font-weight: 800;
    font-size: 20px;
    color: var(--primary-dark);
    background: var(--primary-light);
    padding: 7px 14px;
    border-radius: 10px;
    white-space: nowrap;
}

.method-card {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 24px;
    height: 100%;
}

.method-card-title {
    font-weight: 800;
    font-size: 15px;
    margin-bottom: 10px;
    color: var(--ink);
    display: flex;
    align-items: center;
    gap: 8px;
}

.method-card-dot {
    width: 8px;
    height: 8px;
    background: var(--primary);
    border-radius: 50%;
    flex-shrink: 0;
}

.method-card-text {
    font-size: 13.5px;
    line-height: 1.65;
    color: var(--ink-muted);
}

.dm-footer {
    text-align: center;
    margin-top: 56px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
    color: var(--ink-faint);
    font-size: 12.5px;
    font-weight: 500;
}

@media (max-width: 768px) {
    .stats-grid { grid-template-columns: 1fr 1fr !important; }
    .hero-title { font-size: 28px !important; }
    .hero-card { padding: 40px 20px 36px !important; }
    .topbar { padding: 8px 8px 8px 14px !important; }
}

@media (max-width: 480px) {
    .stats-grid { grid-template-columns: 1fr !important; }
}
</style>
""",
    unsafe_allow_html=True,
)


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
if "show_inline_result" not in st.session_state:
    st.session_state.show_inline_result = False

CF_MAP = {"Tidak": 0.0, "Kurang Yakin": 0.4, "Cukup Yakin": 0.8, "Sangat Yakin": 1.0}


def get_risk_theme(pct):
    if pct >= 70:
        return "high-risk", "#fef2f2", "#7f1d1d", "🔴 Risiko Tinggi"
    if pct >= 40:
        return "med-risk", "#fffbeb", "#78350f", "🟡 Risiko Sedang"
    return "low-risk", "#ecfdf5", "#064e3b", "🟢 Risiko Rendah"


ICON_STETH = '<svg viewBox="0 0 24 24"><path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6v0a6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>'
ICON_SHIELD = '<svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
ICON_CHART = '<svg viewBox="0 0 24 24"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
ICON_CLOCK = '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'

st.markdown(
    """
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-logo">DM</div>
        <div>
            <div class="topbar-name">Dermalyze</div>
            <div class="topbar-sub">Skin Cancer Expert System</div>
        </div>
    </div>
    <div class="topbar-badge">v1.0 · Active</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero-card">
    <div class="hero-badge">Forward Chaining &amp; Certainty Factor</div>
    <div class="hero-title">Skrining Risiko Kanker Kulit</div>
    <div class="hero-desc">
        Dermalyze membantu melakukan estimasi awal risiko kanker kulit berdasarkan pola gejala ABCDE dan komplikasi medis lainnya. Aplikasi ini bukan pengganti diagnosis dokter spesialis.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

gejala_list = kb.get_semua_gejala()
total_rules = len(kb.rules)
total_gejala = len(gejala_list)
total_konsultasi = len(st.session_state.riwayat)

st.markdown(
    f"""
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon-wrap">{ICON_STETH}</div>
        <div class="stat-title">Gejala Klinis</div>
        <div class="stat-value">{total_gejala} Parameter</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon-wrap">{ICON_SHIELD}</div>
        <div class="stat-title">Aturan Pakar</div>
        <div class="stat-value">{total_rules} Rule Dasar</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon-wrap">{ICON_CHART}</div>
        <div class="stat-title">Diagnosis</div>
        <div class="stat-value">{len(kb.penyakit)} Klasifikasi</div>
    </div>
    <div class="stat-card">
        <div class="stat-icon-wrap">{ICON_CLOCK}</div>
        <div class="stat-title">Riwayat Sesi</div>
        <div class="stat-value">{total_konsultasi} Disimpan</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["📋 Konsultasi Baru", "📊 Detail Analisis", "📁 Riwayat", "ℹ️ Info Metode"]
)

with tab1:
    st.markdown(
        """
<div class="warn-banner">
    <div class="warn-banner-icon">⚠️</div>
    <div class="warn-banner-text">
        <strong>Penting:</strong> Aplikasi ini dirancang untuk skrining awal risiko kanker kulit, bukan untuk diagnosis pasti.
        Konsultasikan dengan dokter untuk tindakan medis lebih lanjut.
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="dm-card"><div class="dm-card-title"><span class="dm-card-title-dot"></span>Data Pasien</div>',
        unsafe_allow_html=True,
    )
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        nama = st.text_input("Nama Pasien", placeholder="Contoh: Angel")
    with col_b:
        usia = st.number_input("Usia", min_value=1, max_value=120, value=20)
    with col_c:
        lokasi_lesi = st.selectbox(
            "Lokasi Lesi",
            [
                "Pilih lokasi...",
                "Wajah",
                "Leher",
                "Tangan / Lengan",
                "Kaki / Tungkai",
                "Punggung",
                "Dada / Perut",
                "Lainnya",
            ],
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        '<div class="dm-card"><div class="dm-card-title"><span class="dm-card-title-dot"></span>Kuesioner Gejala Kanker Kulit</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='font-size:14px; color:var(--ink-muted); margin-bottom:20px; margin-top:-8px;'>Pilih tingkat keyakinan yang paling mendeskripsikan kondisi tahi lalat atau lesi kulit Anda.</p>",
        unsafe_allow_html=True,
    )

    kategori_map = defaultdict(list)
    for g in gejala_list:
        kategori_map[g["kategori"]].append(g)

    jawaban_user = {}
    pilihan_opsi = ["Tidak", "Kurang Yakin", "Cukup Yakin", "Sangat Yakin"]

    for kategori, gejala_in_kat in kategori_map.items():
        with st.expander(
            f"📌 {kategori}  ({len(gejala_in_kat)} Pertanyaan)",
            expanded=(kategori == "ABCDE"),
        ):
            for g in gejala_in_kat:
                pilihan = st.radio(
                    label=f"**{g['pertanyaan']}**",
                    options=pilihan_opsi,
                    horizontal=True,
                    key=f"radio_{g['id']}",
                )
                jawaban_user[g["id"]] = CF_MAP[pilihan]
                st.write("")
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🔍  Proses Analisis Kanker Kulit", type="primary", use_container_width=True):
        gejala_aktif = [gid for gid, val in jawaban_user.items() if val > 0]
        if not gejala_aktif:
            st.warning("Pilih minimal satu gejala untuk memulai analisis.")
            st.session_state.show_inline_result = False
        else:
            with st.spinner("Menganalisis pola gejala dengan algoritma Forward Chaining…"):
                fc.reset()
                fc.set_fakta(gejala_aktif)
                hasil = fc.run_analysis(jawaban_user)

            if hasil:
                sesi = {
                    "waktu": datetime.now().strftime("%d %b %Y %H:%M"),
                    "nama": nama or "Anonim",
                    "usia": usia,
                    "lokasi": lokasi_lesi if lokasi_lesi != "Pilih lokasi..." else "-",
                    "hasil": hasil,
                    "gejala_aktif": gejala_aktif,
                    "jawaban": jawaban_user,
                }
                st.session_state.hasil = sesi
                st.session_state.riwayat.insert(0, sesi)
                st.session_state.sesi = sesi
                st.session_state.show_inline_result = True
            else:
                st.info("Gejala yang dipilih belum memenuhi kondisi kanker kulit dalam basis pengetahuan.")
                st.session_state.show_inline_result = False

    if st.session_state.show_inline_result and st.session_state.hasil:
        hasil = st.session_state.hasil["hasil"]
        top = hasil[0] if hasil else None

        if top:
            pct = round(top.persentase, 1)
            risk_cls, bg_col, text_col, risk_lbl = get_risk_theme(pct)

            st.markdown(
                f"""
<div class="result-card {risk_cls}" style="background-color:{bg_col};">
    <div style="font-size:12px; font-weight:800; text-transform:uppercase; color:{text_col}; letter-spacing:1.2px; margin-bottom:6px;">{risk_lbl} · {pct}%</div>
    <div style="font-family:'Plus Jakarta Sans',sans-serif; font-size:28px; font-weight:800; color:{text_col}; margin-bottom:12px; line-height:1.2;">{top.nama}</div>
    <div style="font-size:14.5px; color:{text_col}; opacity:0.88; margin-bottom:20px; line-height:1.65;">{top.deskripsi}</div>
    <div style="border-top:1px solid rgba(0,0,0,0.1); padding-top:16px;">
        <div style="font-weight:700; font-size:13px; margin-bottom:10px; color:{text_col};">Saran Tindakan Cepat:</div>
""",
                unsafe_allow_html=True,
            )
            for s in top.saran:
                st.markdown(
                    f"<div style='font-size:13.5px; margin-bottom:7px; color:{text_col}; display:flex; gap:8px;'><span>•</span><span>{s}</span></div>",
                    unsafe_allow_html=True,
                )
            st.markdown("</div></div>", unsafe_allow_html=True)

with tab2:
    if not st.session_state.hasil:
        st.info("Belum ada analisis. Lakukan konsultasi terlebih dahulu di tab Konsultasi Baru.")
    else:
        sesi = st.session_state.hasil
        hasil = sesi["hasil"]
        top = hasil[0] if hasil else None

        if top:
            st.markdown(
                '<div class="dm-card"><div class="dm-card-title"><span class="dm-card-title-dot"></span>Hasil Analisis</div>',
                unsafe_allow_html=True,
            )
            col_res1, col_res2 = st.columns([1, 1])

            with col_res1:
                st.markdown(
                    "<h4 style='font-size:14px; font-weight:700; margin-bottom:14px; color:var(--ink);'>Distribusi Kemungkinan Diagnosis</h4>",
                    unsafe_allow_html=True,
                )
                for item in hasil[:5]:
                    pct_i = round(item.persentase, 1)
                    st.markdown(
                        f"""
<div class="progress-wrap">
    <div style="display:flex; justify-content:space-between; font-weight:700; font-size:13.5px;">
        <span style="color:var(--ink);">{item.nama}</span>
        <span style="color:var(--primary-dark);">{pct_i}%</span>
    </div>
    <div class="progress-bar-bg">
        <div class="progress-bar-fill" style="width:{pct_i}%;"></div>
    </div>
</div>
""",
                        unsafe_allow_html=True,
                    )

            with col_res2:
                st.markdown(
                    "<h4 style='font-size:14px; font-weight:700; margin-bottom:14px; color:var(--ink);'>Jejak Penarikan Kesimpulan (Rule)</h4>",
                    unsafe_allow_html=True,
                )
                detail_cf = top.detail_cf
                if detail_cf:
                    for detail in detail_cf:
                        rule_id = detail["rule_id"]
                        cf_ev = round(detail["cf_evidence"], 4)
                        rule_data = next(
                            (r for r in kb.rules if r["id"] == rule_id), None
                        )
                        alasan = (
                            rule_data["alasan"]
                            if rule_data and "alasan" in rule_data
                            else ""
                        )
                        st.markdown(
                            f"""
<div class="rule-trace">
    <div class="rule-trace-header">{rule_id} &bull; CF Evidence: {cf_ev}</div>
    <div class="rule-trace-body">{alasan}</div>
</div>
""",
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("Tidak ada log rule aktif.")
            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.sesi:
                rg = ReportGenerator()
                report_text = rg.generate_text_report(st.session_state.sesi)
                safe_name = sesi["nama"].replace(" ", "_")
                file_name = f"Laporan_KankerKulit_{safe_name}_{datetime.now().strftime('%Y%m%d')}.txt"
                st.download_button(
                    label="⬇️  Unduh Laporan Diagnosis (TXT)",
                    data=report_text,
                    file_name=file_name,
                    mime="text/plain",
                    use_container_width=True,
                )

with tab3:
    if not st.session_state.riwayat:
        st.markdown(
            """
<div style="text-align:center; padding:64px 32px; color:var(--ink-faint);">
    <div style="font-size:40px; margin-bottom:16px;">📭</div>
    <div style="font-weight:700; font-size:16px; color:var(--ink-muted); margin-bottom:8px;">Riwayat konsultasi kosong</div>
    <div style="font-size:14px;">Lakukan konsultasi pertama Anda di tab Konsultasi Baru.</div>
</div>
""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="dm-card"><div class="dm-card-title"><span class="dm-card-title-dot"></span>Riwayat Sesi Konsultasi</div>',
            unsafe_allow_html=True,
        )
        for r in st.session_state.riwayat:
            r_hasil = r["hasil"]
            top_r = r_hasil[0] if r_hasil else None
            if not top_r:
                continue
            pct_r = round(top_r.persentase, 1)
            st.markdown(
                f"""
<div class="history-entry">
    <div>
        <div class="history-name">{top_r.nama}</div>
        <div class="history-meta">Pasien: {r["nama"]} &bull; Waktu: {r["waktu"]} &bull; Gejala: {len(r["gejala_aktif"])} gejala aktif</div>
    </div>
    <div class="history-pct">{pct_r}%</div>
</div>
""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown(
        '<div class="dm-card"><div class="dm-card-title"><span class="dm-card-title-dot"></span>Landasan Teori Sistem Pakar</div>',
        unsafe_allow_html=True,
    )
    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown(
            """
<div class="method-card">
    <div class="method-card-title"><span class="method-card-dot"></span>Metode Forward Chaining</div>
    <div class="method-card-text">
        Sistem bekerja dengan metode pelacakan maju. Berawal dari mengumpulkan fakta berupa input gejala dari pasien (berbasis Data-Driven). Mesin kemudian menyusuri seluruh rule if-then yang ada di basis pengetahuan dan menyimpulkan risiko kanker kulit yang paling relevan.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )

    with col_m2:
        st.markdown(
            """
<div class="method-card">
    <div class="method-card-title"><span class="method-card-dot"></span>Certainty Factor (Metode Ketidakpastian)</div>
    <div class="method-card-text">
        Karena analisis medis sering kali tidak absolut, algoritma ini menggabungkan nilai bobot dari kepastian pakar (CF Rule) dengan tingkat keyakinan pasien saat menjawab gejala (CF User). Semakin banyak rule yang cocok, semakin tinggi persentase kepastian akhir.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    if not validation.get("valid", True):
        st.error("Ditemukan anomali pada Knowledge Base:")
        for err in validation.get("errors", []):
            st.write(f"- {err}")

st.markdown(
    """
<div class="dm-footer">
    Dermalyze Expert System &bull; Sistem Pakar Skrining Risiko Kanker Kulit &bull; Dhyana Pura University
</div>
""",
    unsafe_allow_html=True,
)
