class BackwardChaining:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def verify_diagnosis(self, penyakit_id, fakta_user):
        rules_terkait = [
            rule for rule in self.kb.rules
            if rule.get("kesimpulan") == penyakit_id
        ]

        hasil_verifikasi = []

        for rule in rules_terkait:
            kondisi = set(rule.get("kondisi", []))
            fakta = set(fakta_user)
            terpenuhi = kondisi.issubset(fakta)

            hasil_verifikasi.append({
                "rule_id": rule.get("id"),
                "kondisi": list(kondisi),
                "terpenuhi": terpenuhi,
                "kekurangan": list(kondisi - fakta)
            })

        return hasil_verifikasi