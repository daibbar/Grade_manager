from typing import List
from src.models.base import Base

class Module(Base):
    def __init__(self, code_module: str, intitule: str, annee_universitaire: str, id_professeur: str = None):
        self.code_module = code_module
        self.intitule = intitule
        self.annee_universitaire = annee_universitaire
        self.id_professeur = id_professeur  # Storing the ID, not the object
        self.etudiants_inscrits: List[str] = [] # List of student IDs

    def ajouter_etudiant(self, id_etudiant: str):
        if id_etudiant not in self.etudiants_inscrits:
            self.etudiants_inscrits.append(id_etudiant)

    def supprimer_etudiant(self, id_etudiant: str):
        if id_etudiant in self.etudiants_inscrits:
            self.etudiants_inscrits.remove(id_etudiant)

    def to_dict(self):
        return {
            "code_module": self.code_module,
            "intitule": self.intitule,
            "annee_universitaire": self.annee_universitaire,
            "id_professeur": self.id_professeur,
            "etudiants_inscrits": self.etudiants_inscrits
        }

    @classmethod
    def from_dict(cls, data):
        module = cls(
            data["code_module"],
            data["intitule"],
            data["annee_universitaire"],
            data.get("id_professeur") # Use .get() in case it's None
        )
        module.etudiants_inscrits = data.get("etudiants_inscrits", [])
        return module