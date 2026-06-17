import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class KnowledgeBase:
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.gejala: Dict[str, Dict[str, Any]] = {}
        self.penyakit: Dict[str, Dict[str, Any]] = {}
        self.rules: List[Dict[str, Any]] = []
        self._load_data()

    def _load_json(self, filename: str) -> Dict[str, Any]:
        filepath = self.data_dir / filename
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"File {filename} tidak ditemukan di {filepath}.")
            return {}
        except json.JSONDecodeError:
            logger.error(f"File {filename} rusak.")
            return {}

    def _load_data(self) -> None:
        gejala_data = self._load_json('gejala.json')
        if 'gejala' in gejala_data:
            self.gejala = {g['id']: g for g in gejala_data['gejala']}

        penyakit_data = self._load_json('penyakit.json')
        if 'penyakit' in penyakit_data:
            self.penyakit = {p['id']: p for p in penyakit_data['penyakit']}

        rules_data = self._load_json('rules.json')
        if 'rules' in rules_data:
            self.rules = rules_data['rules']

    def get_semua_gejala(self) -> List[Dict[str, Any]]:
        return list(self.gejala.values())

    def get_penyakit_by_id(self, penyakit_id: str) -> Optional[Dict[str, Any]]:
        return self.penyakit.get(penyakit_id)