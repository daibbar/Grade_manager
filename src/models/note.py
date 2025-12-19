from src.models.base import Base

class Note(Base):
    def __init__(self, code_module: str, valeur: float, type_note: str):
        # Validation strict (Rule 4 in CDC)
        if not (0 <= valeur <= 20):
            raise ValueError("La note doit être comprise entre 0 et 20")
            
        self.code_module = code_module
        self.valeur = valeur
        self.type_note = type_note  # ex: "CC", "Exam"

    def to_dict(self):
        return {
            "code_module": self.code_module,
            "valeur": self.valeur,
            "type_note": self.type_note
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["code_module"], data["valeur"], data["type_note"])