from dataclasses import dataclass
from typing import List, Dict, Any, Set
from knowledge_base import KnowledgeBase
from certainty_factor import CertaintyFactor

@dataclass
class DiagnosticResult:
    penyakit_id: str
    nama: str
    deskripsi: str
    tingkat_risiko: str
    saran: List[str]
    cf_final: float
    persentase: float
    rules_aktif: List[str]
    detail_cf: List[Dict[str, Any]]

class ForwardChaining:
    def __init__(self, knowledge_base: KnowledgeBase):
        self.kb = knowledge_base
        self.cf_engine = CertaintyFactor()
        self.fakta: Set[str] = set()
        self.jalur_inferensi: List[str] = []

    def reset(self) -> None:
        self.fakta.clear()
        self.jalur_inferensi.clear()

    def set_fakta(self, gejala_ids: List[str]) -> None:
        self.fakta = set(gejala_ids)
        self.jalur_inferensi.append(f"Fakta diterima: {sorted(list(self.fakta))}")

    def _cek_kondisi(self, rule: Dict[str, Any]) -> bool:
        kondisi = set(rule['kondisi'])
        return kondisi.issubset(self.fakta)

    def inferensi(self) -> Dict[str, List[Dict[str, Any]]]:
        self.jalur_inferensi.append('\n--- MEMULAI MESIN INFERENSI ---')
        kesimpulan_mentah: Dict[str, List[Dict[str, Any]]] = {}

        for rule in self.kb.rules:
            terpenuhi = self._cek_kondisi(rule)
            status = 'AKTIF' if terpenuhi else 'tidak aktif'
            self.jalur_inferensi.append(f"Rule {rule['id']}: kondisi={rule['kondisi']} --> {status}")
            
            if terpenuhi:
                penyakit_id = rule['kesimpulan']
                if penyakit_id not in kesimpulan_mentah:
                    kesimpulan_mentah[penyakit_id] = []
                kesimpulan_mentah[penyakit_id].append(rule)
                
        return kesimpulan_mentah

    def run_analysis(self, cf_user_dict: Dict[str, float]) -> List[DiagnosticResult]:
        kesimpulan_mentah = self.inferensi()
        hasil_akhir: List[DiagnosticResult] = []

        for penyakit_id, rules_aktif in kesimpulan_mentah.items():
            penyakit = self.kb.get_penyakit_by_id(penyakit_id)
            if not penyakit:
                continue

            cf_final, detail = self.cf_engine.hitung_cf_penyakit(rules_aktif, cf_user_dict)
            
            hasil_akhir.append(DiagnosticResult(
                penyakit_id=penyakit_id,
                nama=penyakit['nama'],
                deskripsi=penyakit['deskripsi'],
                tingkat_risiko=penyakit['tingkat_risiko'],
                saran=penyakit['saran'],
                cf_final=cf_final,
                persentase=cf_final * 100,
                rules_aktif=[r['id'] for r in rules_aktif],
                detail_cf=detail
            ))
            
        hasil_akhir.sort(key=lambda x: x.cf_final, reverse=True)
        return hasil_akhir