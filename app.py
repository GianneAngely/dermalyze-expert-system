import json
from datetime import datetime
from pathlib import Path
from collections import defaultdict

import plotly.graph_objects as go
import streamlit as st

# Pastikan import module lokal Anda tetap ada
from knowledge_base import KnowledgeBase
from inference_engine import ForwardChaining
from backward_chaining import BackwardChaining
from validators import KnowledgeBaseValidator
from report_generator import ReportGenerator

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Dermalyze | Careplus Theme",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- 2. CUSTOM CSS (CAREPLUS THEME) ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

:root {
    --teal-primary: #55b4b4;
    --teal-dark: #3a8e8e;
    --teal-light: #e6f4f4;
    --ink: #1e293b;
    --ink-light: #64748b;
    --bg-main: #f2fafa;
}

/* ================================
   GLOBAL TEXT
================================ */
.stApp,
.stApp p,
.stApp label,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6 {
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #e0f2f2 0%, #f4fafa 300px, #ffffff 100%) !important;
}

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    max-width: 1100px !important;
    padding: 2rem 1.5rem 5rem !important;
    margin: 0 auto;
}

/* ================================
   NAVBAR
================================ */
.careplus-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 99px;
    padding: 12px 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
    margin-bottom: 50px;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 18px !important;
    font-weight: 800 !important;
    color: var(--ink) !important;
}

.nav-brand span,
.nav-brand div {
    color: var(--ink) !important;
}

.nav-logo {
    color: var(--teal-primary) !important;
    font-size: 24px !important;
}

.nav-links {
    display: flex;
    gap: 30px;
    font-size: 14px;
    font-weight: 600;
}

.nav-links span {
    color: var(--ink-light) !important;
    cursor: pointer;
    transition: color 0.2s;
}

.nav-links span:hover {
    color: var(--teal-primary) !important;
}

.nav-btn {
    background-color: var(--teal-primary) !important;
    color: white !important;
    padding: 10px 24px;
    border-radius: 99px;
    font-weight: 600;
    font-size: 14px;
    box-shadow: 0 4px 12px rgba(85, 180, 180, 0.3);
}

/* ================================
   HERO
================================ */
.hero-section {
    padding: 20px 0 40px 20px;
    max-width: 600px;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 52px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin-bottom: 16px !important;
    line-height: 1.1 !important;
    letter-spacing: -1px !important;
}

.hero-subtitle {
    font-size: 18px !important;
    color: #475569 !important;
    line-height: 1.6 !important;
}

/* ================================
   FLOATING BAR
================================ */
.floating-bar {
background: transparent !important;
    backdrop-filter: none !important;
    -webkit-backdrop-filter: none !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-bottom: 24px !important;

}

/* ================================
   CARDS / SECTION
================================ */
.section-title {
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 24px !important;
    font-weight: 800 !important;
    margin-bottom: 30px;
    color: var(--ink) !important;
}

.dept-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 30px 20px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.04);
    transition: transform 0.3s ease;
    height: 100%;
}

.dept-card:hover {
    transform: translateY(-5px);
}

.dept-icon {
    font-size: 40px;
    color: var(--teal-primary) !important;
    margin-bottom: 16px;
}

.dept-title {
    font-weight: 700;
    font-size: 16px;
    color: var(--ink) !important;
}


/* ================================
   FINAL FIX — INPUT / NUMBER / SELECTBOX
================================ */

/* Main outer field */
.stTextInput div[data-baseweb="input"] > div,
.stNumberInput div[data-baseweb="input"] > div,
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #dbe4ee !important;
    border-radius: 14px !important;
    box-shadow: none !important;
    min-height: 48px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

/* Remove Streamlit default inner border */
.stTextInput div[data-baseweb="input"],
.stNumberInput div[data-baseweb="input"],
.stTextInput input,
.stNumberInput input,
.stSelectbox input {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    background: transparent !important;
}

/* Text color */
.stTextInput input,
.stNumberInput input,
.stSelectbox input,
.stSelectbox div[data-baseweb="select"] *,
div[data-testid="stSelectbox"] * {
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
}

/* Placeholder color */
.stTextInput input::placeholder,
.stNumberInput input::placeholder,
.stSelectbox input::placeholder {
    color: #94a3b8 !important;
    opacity: 1 !important;
}

/* Focus style */
.stTextInput div[data-baseweb="input"] > div:focus-within,
.stNumberInput div[data-baseweb="input"] > div:focus-within,
.stSelectbox div[data-baseweb="select"] > div:focus-within {
    border: 1px solid var(--teal-primary) !important;
    box-shadow: 0 0 0 2px rgba(85, 180, 180, 0.12) !important;
    outline: none !important;
}

/* Number input buttons */
.stNumberInput button {
    background-color: #f8fafc !important;
    color: var(--ink) !important;
    border: none !important;
    box-shadow: none !important;
}

.stNumberInput button:hover,
.stNumberInput button:focus,
.stNumberInput button:active {
    background-color: var(--teal-light) !important;
    color: var(--teal-primary) !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Dropdown popup */
ul[role="listbox"] {
    background: #ffffff !important;
    border: 1px solid #dbe4ee !important;
    border-radius: 12px !important;
}

/* Dropdown text */
ul[role="listbox"] li,
ul[role="listbox"] li span,
ul[role="listbox"] div {
    color: var(--ink) !important;
    background: #ffffff !important;
}

/* Dropdown hover/selected */
ul[role="listbox"] li:hover,
ul[role="listbox"] li[aria-selected="true"] {
    background-color: var(--teal-light) !important;
    color: var(--ink) !important;
}

/* Dropdown arrow */
.stSelectbox svg,
div[data-testid="stSelectbox"] svg {
    fill: #64748b !important;
    color: #64748b !important;
}

/* ================================
   EXPANDER
================================ */
[data-testid="stExpander"] details summary {
    background-color: #f8fafc !important;
    border-radius: 12px !important;
    border: 1px solid #e2e8f0 !important;
    padding: 12px 16px !important;
    margin-bottom: 8px !important;
}

[data-testid="stExpander"] details summary:hover,
[data-testid="stExpander"] details summary:focus {
    background-color: #f8fafc !important;
    color: var(--ink) !important;
}

[data-testid="stExpander"] details summary p {
    font-weight: 600 !important;
    margin: 0 !important;
    color: var(--ink) !important;
}

/* ================================
   BUTTON
================================ */
.stButton > button {
    background: var(--teal-primary) !important;
    color: white !important;
    border-radius: 99px !important;
    padding: 12px 24px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(85, 180, 180, 0.2) !important;
    width: 100%;
}

.stButton > button:hover {
    background: var(--teal-dark) !important;
}

/* ================================
   TABS
================================ */
div[data-testid="stTabs"] > div > div > div {
    background: transparent !important;
}

div[data-testid="stTabs"] button {
    font-weight: 600 !important;
    color: var(--ink-light) !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--teal-primary) !important;
    border-bottom: 3px solid var(--teal-primary) !important;
}

/* ================================
   RESULT CARD
================================ */
.result-card-inline {
    background: #ffffff;
    border-radius: 24px;
    padding: 32px;
    margin-top: 24px;
    margin-bottom: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    border-left: 8px solid;
}

.high-risk { border-color: #ef4444 !important; }
.med-risk { border-color: #f59e0b !important; }
.low-risk { border-color: var(--teal-primary) !important; }
</style>
""",
    unsafe_allow_html=True,
)


# --- 3. SYSTEM INITIALIZATION ---
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
        return "high-risk", "#fef2f2", "#7f1d1d", "Risiko Tinggi"
    if pct >= 40:
        return "med-risk", "#fffbeb", "#78350f", "Risiko Sedang"
    return "low-risk", "#f2fafa", "#2d7a7a", "Risiko Rendah"


# --- 4. TOP NAVIGATION BAR ---
st.markdown(
    """
<div class="careplus-nav">
    <div class="nav-brand">
        <span class="nav-logo">✚</span> DERMALYZE MEDICAL
    </div>
    <div class="nav-links">
        <span>Home</span>
        <span>Services</span>
        <span>Departments</span>
        <span>Doctors</span>
        <span>Contact</span>
    </div>
    <div class="nav-btn">Book Appointment</div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 5. HERO SECTION ---
st.markdown(
    """
<div class="hero-section">
    <div class="hero-title">Kesehatan Kulit Anda Prioritas Kami</div>
    <div class="hero-subtitle">
Dermalyze membantu melakukan estimasi awal risiko kanker kulit berdasarkan pola gejala ABCDE dan komplikasi medis lainnya. Aplikasi ini bukan pengganti diagnosis dokter spesialis
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --- 6. MAIN CONTENT (TABS) ---
tab1, tab2, tab3, tab4 = st.tabs(
    ["Skrining Baru (Home)", "Detail Diagnosis", "Riwayat", "Metodologi"]
)

with tab1:
    # --- FLOATING INPUT BAR (MIMICKING CAREPLUS SEARCH BAR) ---
    st.markdown('<div class="floating-bar">', unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size: 13px; font-weight: 700; color: #64748b; margin-bottom: 12px; text-transform: uppercase;'>Data Pasien</p>",
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        nama = st.text_input("Nama Lengkap", placeholder="Contoh: Gianne Angely")
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

    # --- DEPARTMENTS STYLE CARDS (STATS) ---
    st.markdown(
        '<div class="section-title">Kapabilitas Sistem</div>', unsafe_allow_html=True
    )
    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown(
            f"""
        <div class="dept-card">
            <div class="dept-icon">🚑</div>
            <div class="dept-title">Analisis Gejala</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 8px;">Mengevaluasi {len(kb.get_semua_gejala())} parameter klinis.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_s2:
        st.markdown(
            f"""
        <div class="dept-card">
            <div class="dept-icon">🧸</div>
            <div class="dept-title">Aturan Pakar</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 8px;">Digerakkan oleh {len(kb.rules)} rule tervalidasi.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col_s3:
        st.markdown(
            f"""
        <div class="dept-card">
            <div class="dept-icon">🩺</div>
            <div class="dept-title">Klasifikasi Medis</div>
            <div style="font-size: 13px; color: #64748b; margin-top: 8px;">Mendeteksi {len(kb.penyakit)} jenis kondisi.</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- FEATURED SERVICES STYLE (QUESTIONNAIRE) ---
    st.markdown(
        '<div class="section-title">Kuesioner Klinis</div>', unsafe_allow_html=True
    )
    # st.markdown(
    #     """
    # <div style="background: #ffffff; border-radius: 24px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.04);">
    # """,
    #     unsafe_allow_html=True,
    # )

    gejala_list = kb.get_semua_gejala()
    kategori_map = defaultdict(list)
    for g in gejala_list:
        kategori_map[g["kategori"]].append(g)

    jawaban_user = {}
    pilihan_opsi = ["Tidak", "Kurang Yakin", "Cukup Yakin", "Sangat Yakin"]

    for kategori, gejala_in_kat in kategori_map.items():
        with st.expander(
            f"🩺 {kategori} ({len(gejala_in_kat)} Pertanyaan)",
            expanded=(kategori == "ABCDE"),
        ):
            if kategori.upper() == "ABCDE" or "ABCDE" in kategori.upper():
                st.markdown(
                    """
                <div style="background-color: #f2fafa; border-left: 4px solid var(--teal-primary); padding: 12px 16px; margin-bottom: 24px; border-radius: 0 8px 8px 0; font-size: 14px; color: var(--ink-light);">
                    <span style="color: var(--ink); font-weight: 700;">Indikator ABCDE:</span> A - Asymmetry, B - Border, C - Color, D - Diameter, E - Evolving
                </div>
                """,
                    unsafe_allow_html=True,
                )
            for g in gejala_in_kat:
                pilihan = st.radio(
                    label=f"**{g['pertanyaan']}**",
                    options=pilihan_opsi,
                    horizontal=True,
                    key=f"radio_{g['id']}",
                )
                jawaban_user[g["id"]] = CF_MAP[pilihan]
                st.write("")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Jalankan Skrining Sistem Pakar", type="primary"):
        gejala_aktif = [gid for gid, val in jawaban_user.items() if val > 0]
        if not gejala_aktif:
            st.warning("Pilih minimal satu gejala untuk memulai analisis.")
            st.session_state.show_inline_result = False
        else:
            with st.spinner("Memproses dengan algoritma Forward Chaining..."):
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
                st.info(
                    "Gejala yang dipilih belum memenuhi kondisi kanker kulit dalam basis pengetahuan."
                )
                st.session_state.show_inline_result = False

    # --- INLINE RESULTS ---
    if st.session_state.show_inline_result and st.session_state.hasil:
        hasil = st.session_state.hasil["hasil"]
        top = hasil[0] if hasil else None

        if top:
            pct = round(top.persentase, 1)
            risk_cls, bg_col, text_col, risk_lbl = get_risk_theme(pct)

            # Kumpulkan seluruh HTML dalam satu variabel string
            html_result = f"""
            <div class="result-card-inline {risk_cls}" style="background-color: {bg_col};">
                <div style="font-size: 13px; font-weight: 800; text-transform: uppercase; color: {text_col}; letter-spacing: 1px; margin-bottom: 8px;">{risk_lbl} ({pct}%)</div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 32px; font-weight: 800; color: {text_col}; margin-bottom: 12px; line-height: 1.2;">{top.nama}</div>
                <div style="font-size: 15px; color: {text_col}; opacity: 0.9; margin-bottom: 20px; line-height: 1.6;">{top.deskripsi}</div>
                <div style="border-top: 1px solid rgba(0,0,0,0.1); padding-top: 16px;">
                    <div style="font-weight: 700; font-size: 14px; margin-bottom: 12px; color: {text_col};">Saran Tindakan Cepat:</div>
            """

            # Tambahkan daftar centang ke dalam variabel string
            for s in top.saran:
                html_result += f"<div style='font-size: 14px; margin-bottom: 8px; color: {text_col}; display: flex; gap: 8px;'><span style='font-weight: bold;'>✓</span> <span>{s}</span></div>"

            # Tambahkan penutup div
            html_result += """
                </div>
            </div>
            """

            # Panggil st.markdown satu kali saja agar tidak terpotong
            st.markdown(html_result, unsafe_allow_html=True)
with tab2:
    sesi = st.session_state.hasil

    if not sesi:
        st.info("Belum ada data analisis. Silakan proses skrining terlebih dahulu.")
    else:
        hasil = sesi["hasil"]
        top = hasil[0] if hasil else None

        if top:
            st.markdown(
                """<div style="background: #ffffff; border-radius: 24px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.04);">""",
                unsafe_allow_html=True,
            )
            col_res1, col_res2 = st.columns([1, 1])

            with col_res1:
                st.markdown(
                    "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 18px; font-weight: 800; margin-bottom: 16px;'>Kemungkinan Diagnosis Lainnya</h3>",
                    unsafe_allow_html=True,
                )
                for item in hasil:
                    pct_i = round(item.persentase, 1)
                    st.markdown(
                        f"""
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 14px; margin-bottom: 12px;">
                            <span style="color: #0f172a;">{item.nama}</span>
                            <span style="color: #55b4b4;">{pct_i}%</span>
                        </div>
                        <div style="height: 8px; background: #e2e8f0; border-radius: 99px; overflow: hidden;">
                            <div style="height: 100%; background: #55b4b4; border-radius: 99px; width: {pct_i}%;"></div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

            with col_res2:
                st.markdown(
                    "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 18px; font-weight: 800; margin-bottom: 16px;'>Jejak Penarikan Kesimpulan (Rule)</h3>",
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
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 16px; margin-bottom: 12px;">
                            <div style="font-weight: 700; font-size: 14px; margin-bottom: 8px; color: #55b4b4;">{rule_id} &bull; CF Evidence: {cf_ev}</div>
                            <div style="font-size: 13px; color: #475569; line-height: 1.5;">{alasan}</div>
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
                    label="Unduh Laporan Diagnosis TXT",
                    data=report_text,
                    file_name=file_name,
                    mime="text/plain",
                )

with tab3:
    if not st.session_state.riwayat:
        st.info("Riwayat konsultasi kosong.")
    else:
        st.markdown(
            """<div style="background: #ffffff; border-radius: 24px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.04);">""",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 24px;'>Riwayat Sesi Konsultasi</h3>",
            unsafe_allow_html=True,
        )
        for idx, r in enumerate(st.session_state.riwayat):
            r_hasil = r["hasil"]
            top_r = r_hasil[0] if r_hasil else None
            if not top_r:
                continue
            pct_r = round(top_r.persentase, 1)

            st.markdown(
                f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 18px; margin-bottom: 6px; color: #0f172a;">{top_r.nama}</div>
                    <div style="font-size: 13px; color: #64748b;">Pasien: {r["nama"]} &bull; Waktu: {r["waktu"]} &bull; Gejala diinput: {len(r["gejala_aktif"])}</div>
                </div>
                <div style="font-weight: 800; font-size: 24px; color: #55b4b4; background: #e6f4f4; padding: 8px 16px; border-radius: 12px;">{pct_r}%</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown(
        """<div style="background: #ffffff; border-radius: 24px; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.04);">""",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 24px;'>Landasan Teori Sistem Pakar</h3>",
        unsafe_allow_html=True,
    )
    col_m1, col_m2 = st.columns(2)

    with col_m1:
        st.markdown(
            """
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; height: 100%;">
            <div style="font-weight: 800; font-size: 16px; margin-bottom: 12px; color: #0f172a;">Metode Forward Chaining</div>
            <div style="font-size: 14px; line-height: 1.6; color: #475569;">
                Sistem bekerja dengan metode pelacakan maju. Berawal dari mengumpulkan fakta berupa input gejala dari pasien (berbasis Data-Driven). Mesin kemudian menyusuri seluruh rule if-then yang ada di basis pengetahuan dan menyimpulkan risiko kanker kulit yang paling relevan.
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col_m2:
        st.markdown(
            """
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; height: 100%;">
            <div style="font-weight: 800; font-size: 16px; margin-bottom: 12px; color: #0f172a;">Certainty Factor (Metode Ketidakpastian)</div>
            <div style="font-size: 14px; line-height: 1.6; color: #475569;">
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
<div style="text-align: center; margin-top: 60px; padding-top: 30px; border-top: 1px solid rgba(0,0,0,0.05); color: #94a3b8; font-size: 13px; font-weight: 500;">
    Careplus Medical Theme &bull; Sistem Pakar Skrining Risiko Kanker Kulit &bull; Dhyana Pura University
</div>
""",
    unsafe_allow_html=True,
)
