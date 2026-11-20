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

      ==================================================
 class Servicio(ABC):
     """Clase abstracta para todos los servicios ofrecidos"""
     
     def _init_(self, nombre, descripcion, precio_base, disponible=True):
         self._nombre = nombre
         self._descripcion = descripcion
         self._precio_base = precio_base
         self._disponible = disponible
     
     @property
     def nombre(self):
         return self._nombre
     
     @property
     def disponible(self):
         return self._disponible
     
     def marcar_no_disponible(self):
         self._disponible = False
     
     def marcar_disponible(self):
         self._disponible = True
     
     # Métodos sobrecargados: cálculo de costo con diferentes parámetros
     @abstractmethod
     def calcular_costo(self, duracion_dias, **kwargs):
         """Calcular costo del servicio — polimorfismo"""
         pass
     
     @abstractmethod
     def describir_servicio(self):
         """Devuelve la descripción completa del servicio"""
         pass
 # ─── SERVICIO 1: RESERVA DE SALA ───
 class ReservaSala(Servicio):
     def _init_(self):
         super()._init_("Reserva de Sala", "Espacios acondicionados para reuniones y eventos", 50.0)
     
     # Sobrecarga: costo según horas o días
     def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, por_hora=False):
         if por_hora:
             costo_base = self._precio_base * (duracion * 0.1)
         else:
             costo_base = self._precio_base * duracion
         
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f" {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/día"
 # ─── SERVICIO 2: ALQUILER DE EQUIPOS ───
 class AlquilerEquipos(Servicio):
     def _init_(self):
         super()._init_("Alquiler de Equipos", "Computadores, proyectores y equipos especializados", 35.0)
     
     def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, cantidad_equipos=1):
         costo_base = self._precio_base * duracion * cantidad_equipos
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f" {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/día por equipo"
 # ─── SERVICIO 3: ASESORÍA ESPECIALIZADA ───
 class AsesoriaEspecializada(Servicio):
     def _init_(self):
         super()._init_("Asesoría Especializada", "Orientación profesional en diferentes áreas", 80.0)
     
     def calcular_costo(self, duracion_horas, impuesto=0.19, descuento=0.0, sesiones_grupo=False):
         factor = 1.2 if sesiones_grupo else 1.0
         costo_base = self._precio_base * duracion_horas * factor
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f" {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/hora"
     
     def mostrar_informacion(self):
         return f" Cliente: {self._nombre} | Doc: {self._documento} | Correo: {self._correo
         


