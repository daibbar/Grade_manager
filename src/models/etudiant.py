from typing import List, Dict
from src.models.note import Note

class Etudiant:
    def __init__(self, id_etudiant: str, nom: str, prenom: str, annee_universitaire: str):
        self.id_etudiant = id_etudiant
        self.nom = nom
        self.prenom = prenom
        self.annee_universitaire = annee_universitaire
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
            "modules_inscrits": self.modules_inscrits,
            "notes": [n.to_dict() for n in self.notes] # Serialize nested objects!
        }

    @classmethod
    def from_dict(cls, data):
        etudiant = cls(
            data["id_etudiant"], 
            data["nom"], 
            data["prenom"], 
            data["annee_universitaire"]
        )
        etudiant.modules_inscrits = data.get("modules_inscrits", [])
        # Recreate Note objects from the list of dicts
        etudiant.notes = [Note.from_dict(n) for n in data.get("notes", [])]
        return etudiant