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
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght=600;700;800&display=swap');

:root {
    --primary: #0891b2;
    --primary-light: #e0f2fe;
    --ink: #0f172a;
    --ink-light: #475569;
    --surface: rgba(255, 255, 255, 0.85);
    --border: rgba(255, 255, 255, 0.5);
}

.stApp {
    background: linear-gradient(135deg, #e0f2fe 0%, #f0fdfa 100%) !important;
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Selector yang aman tanpa merusak internal span/div Streamlit */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp p, .stApp label {
    color: var(--ink) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Mengatur font teks di dalam komponen mark-down secara aman */
.stMarkdown p, .stMarkdown span {
    font-family: 'Inter', sans-serif !important;
}

header[data-testid="stHeader"],
div[data-testid="stToolbar"],
section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    max-width: 1000px !important;
    padding: 2rem 1.5rem 5rem !important;
    margin: 0 auto;
}

.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border);
    border-radius: 99px;
    padding: 12px 24px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    margin-bottom: 32px;
}

.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.topbar-logo {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0891b2, #06b6d4);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white !important;
    font-weight: 800;
    font-size: 16px;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.topbar-name {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 18px;
    font-weight: 800;
}

.glass-hero {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 32px;
    padding: 56px 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
    margin-bottom: 32px;
}

.hero-badge {
    display: inline-block;
    background: #ffffff;
    color: #0891b2 !important;
    font-size: 13px;
    font-weight: 700;
    padding: 8px 20px;
    border-radius: 99px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 42px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    margin-bottom: 16px !important;
    line-height: 1.2 !important;
    letter-spacing: -1px !important;
}

.hero-desc {
    font-size: 16px !important;
    color: #475569 !important;
    max-width: 600px;
    margin: 0 auto 0 auto;
    line-height: 1.6 !important;
}

.glass-card {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.03);
    margin-bottom: 24px;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
}

.stat-item {
    background: rgba(255, 255, 255, 0.8);
    border: 1px solid white;
    border-radius: 20px;
    padding: 24px 16px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.stat-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.stat-title {
    font-size: 14px;
    font-weight: 700;
    color: #0f172a !important;
}

.result-card-inline {
    background: #ffffff;
    border-radius: 24px;
    padding: 32px;
    margin-top: 24px;
    margin-bottom: 24px;
    border-left: 6px solid;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.high-risk { border-color: #ef4444; }
.med-risk { border-color: #f59e0b; }
.low-risk { border-color: #10b981; }

input, textarea, div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
}

div[data-testid="stTabs"] > div > div > div {
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(8px);
    border-radius: 16px !important;
    padding: 6px !important;
}

div[data-testid="stTabs"] button {
    color: #475569 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background: #ffffff !important;
    color: #0891b2 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #0891b2, #06b6d4) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 16px !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border: none !important;
    box-shadow: 0 8px 20px rgba(8, 145, 178, 0.2) !important;
}

@media (max-width: 768px) {
    .stats-grid { grid-template-columns: 1fr 1fr; }
    .hero-title { font-size: 32px !important; }
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
        return "high-risk", "#fef2f2", "#7f1d1d", "Risiko Tinggi"
    if pct >= 40:
        return "med-risk", "#fffbeb", "#78350f", "Risiko Sedang"
    return "low-risk", "#ecfdf5", "#064e3b", "Risiko Rendah"


st.markdown(
    """
<div class="topbar">
    <div class="topbar-brand">
        <div class="topbar-logo">DM</div>
        <div>
            <div class="topbar-name">Dermalyze</div>
            <div style="font-size: 11px; color: #64748b; font-weight: 600;">Skin Cancer Expert System</div>
        </div>
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
    """
<div class="glass-hero">
    <div class="hero-badge">Forward Chaining & Certainty Factor</div>
    <div class="hero-title">Skrining Risiko Kanker Kulit</div>
    <div class="hero-desc">
        Dermalyze membantu melakukan estimasi awal risiko kanker kulit berdasarkan pola gejala ABCDE dan komplikasi medis lainnya. Aplikasi ini bukan pengganti diagnosis dokter spesialis.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
<div class="stats-grid">
    <div class="stat-item">
        <div class="stat-icon">🩺</div>
        <div class="stat-title">Gejala Klinis</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{total_gejala} Parameter</div>
    </div>
    <div class="stat-item">
        <div class="stat-icon">🛡️</div>
        <div class="stat-title">Aturan Pakar</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{total_rules} Rule Dasar</div>
    </div>
    <div class="stat-item">
        <div class="stat-icon">📊</div>
        <div class="stat-title">Diagnosis</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{len(kb.penyakit)} Klasifikasi</div>
    </div>
    <div class="stat-item">
        <div class="stat-icon">🕒</div>
        <div class="stat-title">Riwayat Sesi</div>
        <div style="font-size: 12px; color: #64748b; margin-top: 4px;">{total_konsultasi} Disimpan</div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Konsultasi Baru", "Detail Analisis", "Riwayat", "Info Metode"]
)

with tab1:
    st.markdown(
        """
    <div style="background: #fffbeb; border: 1px solid #fde68a; border-radius: 12px; padding: 16px; margin-bottom: 24px; display: flex; gap: 12px;">
        <span style="font-size: 18px;">⚠️</span>
        <span style="font-size: 14px; color: #92400e; font-weight: 500;">Penting: Aplikasi ini dirancang untuk skrining awal risiko kanker kulit, bukan untuk diagnosis pasti. Konsultasikan dengan dokter untuk tindakan medis lebih lanjut.</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 16px;'>Data Pasien</h3>",
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

    with st.container():
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown(
            "<h3 style='font-family: \"Plus Jakarta Sans\", sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 4px;'>Kuesioner Gejala Kanker Kulit</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='font-size: 14px; color: #64748b; margin-bottom: 24px;'>Pilih tingkat keyakinan yang paling mendeskripsikan kondisi tahi lalat atau lesi kulit Anda.</p>",
            unsafe_allow_html=True,
        )

        kategori_map = defaultdict(list)
        for g in gejala_list:
            kategori_map[g["kategori"]].append(g)

        jawaban_user = {}
        pilihan_opsi = ["Tidak", "Kurang Yakin", "Cukup Yakin", "Sangat Yakin"]

        for kategori, gejala_in_kat in kategori_map.items():
            with st.expander(
                f"📌 {kategori} ({len(gejala_in_kat)} Pertanyaan)",
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
    if st.button(
        "Proses Analisis Kanker Kulit", type="primary", use_container_width=True
    ):
        gejala_aktif = [gid for gid, val in jawaban_user.items() if val > 0]
        if not gejala_aktif:
            st.warning("Pilih minimal satu gejala untuk memulai analisis.")
            st.session_state.show_inline_result = False
        else:
            with st.spinner(
                "Menganalisis pola gejala dengan algoritma Forward Chaining..."
            ):
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

    if st.session_state.show_inline_result and st.session_state.hasil:
        hasil = st.session_state.hasil["hasil"]
        top = hasil[0] if hasil else None

        if top:
            pct = round(top.persentase, 1)
            risk_cls, bg_col, text_col, risk_lbl = get_risk_theme(pct)

            st.markdown(
                f"""
            <div class="result-card-inline {risk_cls}" style="background-color: {bg_col};">
                <div style="font-size: 13px; font-weight: 800; text-transform: uppercase; color: {text_col}; letter-spacing: 1px; margin-bottom: 8px;">{risk_lbl} ({pct}%)</div>
                <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 32px; font-weight: 800; color: {text_col}; margin-bottom: 12px; line-height: 1.2;">{top.nama}</div>
                <div style="font-size: 15px; color: {text_col}; opacity: 0.9; margin-bottom: 20px; line-height: 1.6;">{top.deskripsi}</div>
                <div style="border-top: 1px solid rgba(0,0,0,0.1); padding-top: 16px;">
                    <div style="font-weight: 700; font-size: 14px; margin-bottom: 12px; color: {text_col};">Saran Tindakan Cepat:</div>
            """,
                unsafe_allow_html=True,
            )

            for s in top.saran:
                st.markdown(
                    f"<div style='font-size: 14px; margin-bottom: 8px; color: {text_col}; display: flex; gap: 8px;'><span style='font-weight: bold;'>✓</span> <span>{s}</span></div>",
                    unsafe_allow_html=True,
                )

            st.markdown("</div></div>", unsafe_allow_html=True)

with tab2:
    sesi = st.session_state.hasil

    if not sesi:
        st.info(
            "Belum ada data analisis. Silakan proses skrining di tab Konsultasi Baru terlebih dahulu."
        )
    else:
        hasil = sesi["hasil"]
        top = hasil[0] if hasil else None

        if top:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
                    <div style="background: rgba(255,255,255,0.8); border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 14px; margin-bottom: 12px;">
                            <span style="color: #0f172a;">{item.nama}</span>
                            <span style="color: #0891b2;">{pct_i}%</span>
                        </div>
                        <div style="height: 8px; background: #e2e8f0; border-radius: 99px; overflow: hidden;">
                            <div style="height: 100%; background: #0891b2; border-radius: 99px; width: {pct_i}%;"></div>
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
                        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 12px;">
                            <div style="font-weight: 700; font-size: 14px; margin-bottom: 8px; color: #0891b2;">{rule_id} &bull; CF Evidence: {cf_ev}</div>
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
                    label="Unduh Laporan Diagnosis Format TXT",
                    data=report_text,
                    file_name=file_name,
                    mime="text/plain",
                    use_container_width=True,
                )

with tab3:
    if not st.session_state.riwayat:
        st.info("Riwayat konsultasi kosong.")
    else:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 20px; margin-bottom: 16px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                <div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 18px; margin-bottom: 6px; color: #0f172a;">{top_r.nama}</div>
                    <div style="font-size: 13px; color: #64748b;">Pasien: {r["nama"]} &bull; Waktu: {r["waktu"]} &bull; Gejala diinput: {len(r["gejala_aktif"])}</div>
                </div>
                <div style="font-weight: 800; font-size: 24px; color: #0891b2; background: #e0f2fe; padding: 8px 16px; border-radius: 12px;">{pct_r}%</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
<div style="text-align: center; margin-top: 48px; padding-top: 24px; border-top: 1px solid rgba(0,0,0,0.1); color: #64748b; font-size: 13px; font-weight: 500;">
    Dermalyze Expert System &bull; Sistem Pakar Skrining Risiko Kanker Kulit &bull; Dhyana Pura University
</div>
""",
    unsafe_allow_html=True,
)
