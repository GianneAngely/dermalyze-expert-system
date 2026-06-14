class KnowledgeBaseValidator:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def validate(self):
        errors = []

        gejala_ids = set(self.kb.gejala.keys())
        penyakit_ids = set(self.kb.penyakit.keys())

        for rule in self.kb.rules:
            for gid in rule.get("kondisi", []):
                if gid not in gejala_ids:
                    errors.append(f"Gejala {gid} pada rule {rule.get('id')} tidak ditemukan.")

            if rule.get("kesimpulan") not in penyakit_ids:
                errors.append(f"Kesimpulan {rule.get('kesimpulan')} pada rule {rule.get('id')} tidak ditemukan.")

            if "cf_pakar" not in rule:
                errors.append(f"Rule {rule.get('id')} belum memiliki nilai cf_pakar.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "jumlah_gejala": len(self.kb.gejala),
            "jumlah_penyakit": len(self.kb.penyakit),
            "jumlah_rules": len(self.kb.rules)
        }