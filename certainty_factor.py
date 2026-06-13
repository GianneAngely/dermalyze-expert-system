from typing import List, Dict, Any, Tuple

class CertaintyFactor:
    @staticmethod
    def cf_evidence(cf_user: float, cf_rule: float) -> float:
        return cf_user * cf_rule

    @staticmethod
    def kombinasi_cf(cf1: float, cf2: float) -> float:
        if cf1 >= 0 and cf2 >= 0:
            return cf1 + cf2 * (1 - cf1)
        elif cf1 < 0 and cf2 < 0:
            return cf1 + cf2 * (1 + cf1)
        else:
            return (cf1 + cf2) / (1 - min(abs(cf1), abs(cf2)))

    def hitung_cf_penyakit(self, rules_aktif: List[Dict[str, Any]], cf_user_dict: Dict[str, float]) -> Tuple[float, List[Dict[str, Any]]]:
        detail_perhitungan = []
        cf_list = []

        for rule in rules_aktif:
            cf_user_values = [cf_user_dict.get(g, 1.0) for g in rule['kondisi']]
            cf_user_min = min(cf_user_values) if cf_user_values else 0.0
            
            cf_ev = self.cf_evidence(cf_user_min, rule['cf_pakar'])
            cf_list.append(cf_ev)
            
            detail_perhitungan.append({
                'rule_id': rule['id'],
                'cf_pakar': rule['cf_pakar'],
                'cf_user_terendah': cf_user_min,
                'cf_evidence': cf_ev
            })

        if not cf_list:
            return 0.0, detail_perhitungan

        cf_final = cf_list[0]
        for i in range(1, len(cf_list)):
            cf_final = self.kombinasi_cf(cf_final, cf_list[i])

        return cf_final, detail_perhitungan