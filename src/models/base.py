from abc import ABC, abstractmethod

class Base(ABC):
   @abstractmethod
   def to_dict(self):
      pass

   @abstractmethod
   def from_dict(cls, data):
      pass