from typing import List
from src.models.base import Base

class Professeur(Base):
    # 1. Add password to __init__ with default "1234"
    def __init__(self, id_professeur: str, nom: str, prenom: str, password: str = "1234"):
        self.id_professeur = id_professeur
        self.nom = nom
        self.prenom = prenom
        self.password = password # <--- NEW FIELD
        self.modules_enseignes: List[str] = []

    def assigner_module(self, code_module: str):
        if code_module not in self.modules_enseignes:
            self.modules_enseignes.append(code_module)

    def to_dict(self):
        return {
            "id_professeur": self.id_professeur,
            "nom": self.nom,
            "prenom": self.prenom,
            "password": self.password, # <--- SAVE IT
            "modules_enseignes": self.modules_enseignes
        }

    @classmethod
    def from_dict(cls, data):
        prof = cls(
            data["id_professeur"],
            data["nom"],
            data["prenom"],
            data.get("password", "1234") # <--- LOAD IT (Default to "1234")
        )
        prof.modules_enseignes = data.get("modules_enseignes", [])
        return prof