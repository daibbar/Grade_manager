from abs import ABC

class Utilisateur(ABC):
    
   @abstractmethod
   def to_dict(self):
      pass

   abstractmethod
   def from_dict(cls, data):
      pass