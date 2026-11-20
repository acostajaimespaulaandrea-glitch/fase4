class ErrorValidacion(Exception):
    pass

class ClienteDuplicadoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

 # ==================================================
 from abc import ABC, abstractmethod
 from datetime import datetime
 class EntidadBase(ABC):
     """Clase abstracta que representa a cualquier entidad del sistema"""
     
     def _init_(self, identificador):
         self._id = identificador
         self._fecha_creacion = datetime.now()
     
     @property
     def id(self):
         return self._id
     
     @abstractmethod
     def mostrar_informacion(self):
         """Método abstracto: cada clase hija debe implementarlo"""
         pass
         


