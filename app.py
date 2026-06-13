import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import random
from knowledge_base import KnowledgeBase
from inference_engine import ForwardChaining

st.set_page_config(page_title='Dermalyze | AI Skin Analysis', page_icon='🩺', layout='wide')

st.markdown("""
    <style>
    .main {background-color: #f8fafc;}
    .title-box {background: linear-gradient(135deg, #0f172a, #3b82f6); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);}
    .risk-badge {background-color: #ef4444; color: white; padding: 5px 10px; border-radius: 5px; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_expert_system():
    kb = KnowledgeBase()
    fc = ForwardChaining(kb)
    return kb, fc

kb, fc = init_expert_system()

if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []

st.markdown('<div class="title-box"><h1>🩺 Dermalyze AI</h1><p style="font-size: 1.2rem;">Sistem Pakar Deteksi Risiko Kanker Kulit Berbasis Aturan Klinis (ABCDE)</p></div>', unsafe_allow_html=True)
st.warning("⚠️ **Peringatan Medis:** Sistem pakar ini adalah alat skrining awal dan **bukan** pengganti diagnosis resmi dari Dokter Spesialis Kulit (Sp.KK).")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3003/3003114.png", width=80)
    st.header('☀️ Panel Dermalyze')
    
    uv_index = random.randint(5, 11)
    status_uv = "Sangat Tinggi" if uv_index > 8 else "Tinggi"
    st.metric("Indeks UV Saat Ini", f"{uv_index} ({status_uv})", delta="- Hindari Paparan UV", delta_color="inverse")
    
    st.markdown("---")
    st.header('📊 Engine Stats')
    st.write(f"- Gejala Klinis Terdaftar: **{len(kb.gejala)}**")
    st.write(f"- Aturan Logika AI: **{len(kb.rules)}**")
    st.write("- Algoritma: **Forward Chaining**")
    st.write("- Ketidakpastian: **Certainty Factor**")

st.header('📝 Analisis Klinis (Kuesioner)')
st.write("Jawablah pertanyaan berikut sesuai dengan kondisi lesi/tahi lalat pada kulit Anda dengan jujur.")

jawaban_user = {}
gejala_list = kb.get_semua_gejala()

col1, col2 = st.columns(2)
for idx, g in enumerate(gejala_list):
    with (col1 if idx % 2 == 0 else col2):
        st.markdown(f"**{g['id']} - {g['kategori']}**")
        pilihan = st.radio(
            g['pertanyaan'],
            options=['Tidak (0%)', 'Kurang Yakin (40%)', 'Cukup Yakin (80%)', 'Sangat Yakin (100%)'],
            key=f"q_{g['id']}",
            horizontal=True,
            label_visibility="collapsed"
        )
        st.markdown("<br>", unsafe_allow_html=True)
        
        cf_mapping = {'Tidak (0%)': 0.0, 'Kurang Yakin (40%)': 0.4, 'Cukup Yakin (80%)': 0.8, 'Sangat Yakin (100%)': 1.0}
        jawaban_user[g['id']] = cf_mapping[pilihan]

st.markdown("---")

if st.button('🔍 Proses Analisis dengan Engine AI', type='primary', use_container_width=True):
    gejala_aktif = [gid for gid, cf in jawaban_user.items() if cf > 0]
    
    if len(gejala_aktif) < 2:
        st.error('❌ Data tidak cukup. Mohon pilih minimal 2 gejala agar sistem dapat menarik kesimpulan.')
    else:
        fc.reset()
        fc.set_fakta(gejala_aktif)
        hasil_diagnosis = fc.run_analysis(jawaban_user)
        
        sesi = {
            'waktu': datetime.now().strftime('%d %B %Y - %H:%M:%S'),
            'gejala_aktif': gejala_aktif,
            'hasil': hasil_diagnosis,
            'log_inferensi': fc.jalur_inferensi.copy()
        }
        st.session_state.riwayat.append(sesi)

        st.header('🎯 Hasil Diagnosis Dermalyze')
        
        if not hasil_diagnosis:
            st.success('✅ **Aman!** Tidak ditemukan pola risiko penyakit kulit klinis berdasarkan gejala yang Anda masukkan.')
        else:
            terbaik = hasil_diagnosis[0]
            
            c1, c2 = st.columns([1, 1])
            with c1:
                st.info(f"🚨 **Tingkat Risiko:** {terbaik.tingkat_risiko}")
                st.subheader(f"Indikasi: {terbaik.nama}")
                st.write(f"**Deskripsi:** {terbaik.deskripsi}")
                
                st.markdown("### 💡 Saran Tindakan Medis:")
                for saran in terbaik.saran:
                    st.markdown(f"- {saran}")
                    
            with c2:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = terbaik.persentase,
                    number = {'suffix': "%"},
                    title = {'text': "Tingkat Keyakinan (Certainty Factor)"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#ef4444" if terbaik.persentase > 70 else "#f59e0b"},
                        'steps': [
                            {'range': [0, 40], 'color': "#dcfce3"},
                            {'range': [40, 70], 'color': "#fef08a"},
                            {'range': [70, 100], 'color': "#fecaca"}
                        ]
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")
            with st.expander("⚙️ Explanation Facility (Trace Analisis Logika)"):
                st.write("Sistem ini menggunakan **Forward Chaining** untuk pelacakan fakta dan **Certainty Factor** untuk menangani ketidakpastian.")
                
                st.subheader("1. Aturan yang Memicu Kesimpulan Utama:")
                for detail in terbaik.detail_cf:
                    st.code(f"Rule ID : {detail['rule_id']}\nCF Pakar: {detail['cf_pakar']} | CF Pasien Terendah: {detail['cf_user_terendah']}\nEvidensi CF: {detail['cf_evidence']:.3f}")
                
                st.subheader("2. Jejak Inferensi (Trace Log):")
                st.code('\n'.join(sesi['log_inferensi']), language='text')

if st.session_state.riwayat:
    st.markdown("---")
    st.header('⏳ Riwayat Scanning (Sesi Saat Ini)')
    for i, sesi in enumerate(reversed(st.session_state.riwayat)):
        with st.expander(f"Konsultasi ke-{len(st.session_state.riwayat)-i} | ⏰ {sesi['waktu']}"):
            st.write(f"**Gejala yang dialami:** {', '.join(sesi['gejala_aktif'])}")
            if sesi['hasil']:
                st.write(f"**Diagnosis:** {sesi['hasil'][0].nama} ({sesi['hasil'][0].persentase:.1f}%)")
            else:
                st.write("**Diagnosis:** Aman / Tidak Terdeteksi")