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

# ==================================================
 import re
 class Cliente(EntidadBase):
     """Clase que representa a un cliente con datos protegidos y validados"""
     
     # Lista para evitar documentos duplicados
     _documentos_registrados = set()
     
     def _init_(self, identificador, nombre, documento, correo, telefono):
         super()._init_(identificador)
         # Validaciones antes de asignar valores
         self._validar_datos(nombre, documento, correo, telefono)
         
         self._nombre = nombre
         self._documento = documento
         self._correo = correo
         self._telefono = telefono
         
         # Registrar documento para evitar duplicados
         Cliente._documentos_registrados.add(documento)
     
     def _validar_datos(self, nombre, documento, correo, telefono):
         """Validación estricta de datos del cliente"""
         if not nombre or len(nombre.strip()) < 2:
             raise ErrorValidacion(" El nombre debe tener al menos 2 caracteres")
         
         if not documento or not documento.isdigit() or len(documento) < 5:
             raise ErrorValidacion(" El documento debe tener solo números y mínimo 5 dígitos")
         
         if documento in Cliente._documentos_registrados:
             raise ClienteDuplicadoError(f" Ya existe un cliente con el documento {documento}")
         
         patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
         if not re.match(patron_correo, correo):
             raise ParametroInvalidoError(f" El correo '{correo}' no tiene un formato válido")
         
         if not telefono or not telefono.isdigit() or len(telefono) < 7:
             raise ErrorValidacion(" El teléfono debe tener solo números y mínimo 7 dígitos")
     
     # Métodos para leer datos (encapsulación: solo lectura)
     @property
     def nombre(self):
         return self._nombre
     
     @property
     def documento(self):
         return self._documento
     
     @property
     def correo(self):
         return self._correo
     
     @property
     def telefono(self):
         return self._telefono
     
     def mostrar_informacion(self):
         return f" Cliente: {self._nombre} | Doc: {self._documento} | Correo: {self._correo
         


