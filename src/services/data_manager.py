import json
import os
from typing import List, Dict

# Import your models
from src.models.etudiant import Etudiant
from src.models.professeur import Professeur
from src.models.module import Module

class DataManager:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        
        # Define file paths
        self.files = {
            "etudiants": os.path.join(data_dir, "etudiants.json"),
            "professeurs": os.path.join(data_dir, "professeurs.json"),
            "modules": os.path.join(data_dir, "modules.json")
        }

        # Initialize in-memory storage (Cache)
        self.etudiants: List[Etudiant] = []
        self.professeurs: List[Professeur] = []
        self.modules: List[Module] = []

        # Ensure data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        # Load data immediately upon instantiation
        self.load_data()

    # ==========================
    # INTERNAL HELPERS (Private)
    # ==========================
    def _load_json(self, filepath: str) -> List[Dict]:
        """Safely loads a JSON file. Returns empty list if file doesn't exist."""
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return [] # Handle empty or corrupted files gracefully

    def _save_json(self, filepath: str, data: List[Dict]):
        """Writes a list of dictionaries to a JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # ==========================
    # PUBLIC METHODS (API)
    # ==========================
    def load_data(self):
        """Refreshes all data from disk to memory."""
        # Load Students
        etudiants_data = self._load_json(self.files["etudiants"])
        self.etudiants = [Etudiant.from_dict(d) for d in etudiants_data]

        # Load Professors
        profs_data = self._load_json(self.files["professeurs"])
        self.professeurs = [Professeur.from_dict(d) for d in profs_data]

        # Load Modules
        modules_data = self._load_json(self.files["modules"])
        self.modules = [Module.from_dict(d) for d in modules_data]

    def save_etudiants(self):
        """Persists only the students list."""
        data = [e.to_dict() for e in self.etudiants]
        self._save_json(self.files["etudiants"], data)

    def save_professeurs(self):
        """Persists only the professors list."""
        data = [p.to_dict() for p in self.professeurs]
        self._save_json(self.files["professeurs"], data)

    def save_modules(self):
        """Persists only the modules list."""
        data = [m.to_dict() for m in self.modules]
        self._save_json(self.files["modules"], data)

    # ==========================
    # CONVENIENCE METHODS
    # ==========================
    def get_etudiant_by_id(self, id_etudiant: str):
        for e in self.etudiants:
            if e.id_etudiant == id_etudiant:
                return e
        return None

    def get_module_by_code(self, code_module: str):
        for m in self.modules:
            if m.code_module == code_module:
                return m
        return None