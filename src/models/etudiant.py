from typing import List
from src.models.note import Note
from src.models.base import Base

class Etudiant(Base):
    # 1. Add password to __init__ with a default value
    def __init__(self, id_etudiant: str, nom: str, prenom: str, annee_universitaire: str, password: str = "1234"):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.annee_universitaire = annee_universitaire
        self.password = password  # <--- NEW FIELD
        self.modules_inscrits: List[str] = [] 
        self.notes: List[Note] = [] 

    def s_inscrire_module(self, code_module: str):
        if code_module not in self.modules_inscrits:
            self.modules_inscrits.append(code_module)

    def ajouter_note(self, note: Note):
        if note.code_module in self.modules_inscrits:
            self.notes.append(note)
        else:
            raise ValueError("L'étudiant n'est pas inscrit à ce module.")

    def calculer_moyenne(self) -> float:
        if not self.notes:
            return 0.0
        total = sum(n.valeur for n in self.notes)
        return round(total / len(self.notes), 2)

    def to_dict(self):
        return {
            "id_etudiant": self.id_etudiant,
            "nom": self.nom,
            "prenom": self.prenom,
            "annee_universitaire": self.annee_universitaire,
            "password": self.password, # <--- SAVE IT
            "modules_inscrits": self.modules_inscrits,
            "notes": [n.to_dict() for n in self.notes]
        }

    @classmethod
    def from_dict(cls, data):
        etudiant = cls(
            data["id_etudiant"], 
            data["nom"], 
            data["prenom"], 
            data["annee_universitaire"],
            data.get("password", "1234") # <--- LOAD IT (Default to "1234" if missing)
        )
        etudiant.modules_inscrits = data.get("modules_inscrits", [])
        etudiant.notes = [Note.from_dict(n) for n in data.get("notes", [])]
        return etudiant