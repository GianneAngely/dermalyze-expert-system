from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_text_report(sesi):
        hasil = sesi.get("hasil", [])
        hasil_utama = hasil[0] if hasil else None

        laporan = []
        laporan.append("LAPORAN HASIL KONSULTASI DERMALYZE")
        laporan.append("=" * 45)
        laporan.append(f"Waktu Konsultasi: {sesi.get('waktu', datetime.now())}")
        laporan.append(f"Lokasi Lesi: {sesi.get('lokasi_lesi', '-')}")
        laporan.append(f"Lama Lesi: {sesi.get('lama_lesi', '-')}")
        laporan.append(f"Perubahan Lesi: {sesi.get('perubahan_lesi', '-')}")
        laporan.append("")
        laporan.append("Gejala Aktif:")
        laporan.append(", ".join(sesi.get("gejala_aktif", [])))

        if hasil_utama:
            laporan.append("")
            laporan.append(f"Hasil Utama: {hasil_utama.nama}")
            laporan.append(f"Certainty Factor: {hasil_utama.persentase:.1f}%")
            laporan.append(f"Tingkat Risiko: {hasil_utama.tingkat_risiko}")
        else:
            laporan.append("")
            laporan.append("Hasil Utama: Tidak ada rule aktif.")

        return "\n".join(laporan)