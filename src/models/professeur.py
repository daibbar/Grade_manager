from typing import List

class Professeur:
    def __init__(self, id_professeur: str, nom: str, prenom: str):
        self.id_professeur = id_professeur
        self.nom = nom
        self.prenom = prenom
        self.modules_enseignes: List[str] = [] # List of Module Codes

    def assigner_module(self, code_module: str):
        if code_module not in self.modules_enseignes:
            self.modules_enseignes.append(code_module)

    def to_dict(self):
        return {
            "id_professeur": self.id_professeur,
            "nom": self.nom,
            "prenom": self.prenom,
            "modules_enseignes": self.modules_enseignes
        }

    @classmethod
    def from_dict(cls, data):
        prof = cls(
            data["id_professeur"],
            data["nom"],
            data["prenom"]
        )
        prof.modules_enseignes = data.get("modules_enseignes", [])
        return prof