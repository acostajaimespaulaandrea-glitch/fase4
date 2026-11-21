# ==================================================
 # SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
 # SOFTWARE FJ — Versión Corregida
 # ==================================================
 from abc import ABC, abstractmethod
 from datetime import datetime
 import re
 import sys
 # ==================================================
 # 1. EXCEPCIONES PERSONALIZADAS
 # ==================================================
 class ErrorValidacion(Exception):
     """Excepción base para errores de validación de datos"""
     pass
 class ClienteDuplicadoError(Exception):
     """Se lanza cuando el documento del cliente ya está registrado"""
     pass
 class ServicioNoDisponibleError(Exception):
     """Se lanza cuando se intenta reservar un servicio no disponible"""
     pass
 class ReservaInvalidaError(Exception):
     """Se lanza cuando los datos de la reserva no son correctos"""
     pass
 class ParametroInvalidoError(Exception):
     """Se lanza cuando un parámetro tiene un formato incorrecto"""
     pass

 # ==================================================
 # 2. GESTOR DE LOGS
 # ==================================================
 class GestorLogs:
     """Manejo centralizado del archivo de registro de eventos y errores"""
     
     @staticmethod
     def registrar(mensaje, tipo="INFO"):
         timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
         linea = f"[{timestamp}] [{tipo}] {mensaje}\n"
         try:
             with open("registro_eventos.log", "a", encoding="utf-8") as archivo:
                 archivo.write(linea)
         except Exception as e:
             print(f"⚠️ No se pudo escribir el log: {e}")
     
     @staticmethod
     def info(mensaje):
         GestorLogs.registrar(mensaje, "INFO")
     
     @staticmethod
     def error(mensaje):
         GestorLogs.registrar(mensaje, "ERROR")
     
     @staticmethod
     def advertencia(mensaje):
         GestorLogs.registrar(mensaje, "ADVERTENCIA")

# ==================================================
 # 3. CLASE ABSTRACTA BASE
 # ==================================================
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
 # 4. CLASE CLIENTE
 # ==================================================
 class Cliente(EntidadBase):
     """Clase que representa a un cliente con datos protegidos y validados"""
     
     _documentos_registrados = set()
     
     def _init_(self, identificador, nombre, documento, correo, telefono):
         super()._init_(identificador)
         self._validar_datos(nombre, documento, correo, telefono)
         
         self._nombre = nombre
         self._documento = documento
         self._correo = correo
         self._telefono = telefono
         
         Cliente._documentos_registrados.add(documento)
         GestorLogs.info(f"Cliente creado: {nombre} | Doc: {documento}")
     
     def _validar_datos(self, nombre, documento, correo, telefono):
         """Validación estricta de datos del cliente"""
         if not nombre or len(nombre.strip()) < 2:
             raise ErrorValidacion("El nombre debe tener al menos 2 caracteres")
         
         if not documento or not documento.isdigit() or len(documento) < 5:
             raise ErrorValidacion("El documento debe tener solo números y mínimo 5 dígitos")
         
         if documento in Cliente._documentos_registrados:
             raise ClienteDuplicadoError(f"Ya existe un cliente con el documento {documento}")
         
         patron_correo = r'^[\w\.-]+@[\w\.-]+\.\w+$'
         if not re.match(patron_correo, correo):
             raise ParametroInvalidoError(f"El correo '{correo}' no tiene un formato válido")
         
         if not telefono or not telefono.isdigit() or len(telefono) < 7:
             raise ErrorValidacion("El teléfono debe tener solo números y mínimo 7 dígitos")
     
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
         return f"👤 ID: {self._id} | Cliente: {self._nombre} | Doc: {self._documento} | Correo: {self._correo}"

# ==================================================
 # 5. CLASE ABSTRACTA SERVICIO Y SERVICIOS ESPECIALIZADOS
 # ==================================================
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
         GestorLogs.info(f"Servicio '{self._nombre}' marcado como NO disponible")
     
     def marcar_disponible(self):
         self._disponible = True
         GestorLogs.info(f"Servicio '{self._nombre}' marcado como disponible")
     
     @abstractmethod
     def calcular_costo(self, duracion, **kwargs):
         """Calcular costo del servicio — polimorfismo"""
         pass
     
     @abstractmethod
     def describir_servicio(self):
         """Devuelve la descripción completa del servicio"""
         pass
 class ReservaSala(Servicio):
     """Servicio: Reserva de Salas"""
     
     def _init_(self):
         super()._init_(
             "Reserva de Sala",
             "Espacios acondicionados para reuniones y eventos",
             50.0
         )
     
     def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, por_hora=False):
         if duracion <= 0:
             raise ParametroInvalidoError("La duración debe ser mayor a cero")
         
         if por_hora:
             costo_base = self._precio_base * (duracion * 0.1)
         else:
             costo_base = self._precio_base * duracion
         
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f"🏠 {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/día"
 class AlquilerEquipos(Servicio):
     """Servicio: Alquiler de Equipos"""
     
     def _init_(self):
         super()._init_(
             "Alquiler de Equipos",
             "Computadores, proyectores y equipos especializados",
             35.0
         )
     
     def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0, cantidad_equipos=1):
         if duracion <= 0:
             raise ParametroInvalidoError("La duración debe ser mayor a cero")
         if cantidad_equipos <= 0:
             raise ParametroInvalidoError("La cantidad de equipos debe ser mayor a cero")
         
         costo_base = self._precio_base * duracion * cantidad_equipos
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f"💻 {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/día por equipo"
 class AsesoriaEspecializada(Servicio):
     """Servicio: Asesoría Especializada"""
     
     def _init_(self):
         super()._init_(
             "Asesoría Especializada",
             "Orientación profesional en diferentes áreas",
             80.0
         )
     
     def calcular_costo(self, duracion_horas, impuesto=0.19, descuento=0.0, sesiones_grupo=False):
         if duracion_horas <= 0:
             raise ParametroInvalidoError("La duración debe ser mayor a cero")
         
         factor = 1.2 if sesiones_grupo else 1.0
         costo_base = self._precio_base * duracion_horas * factor
         monto_descuento = costo_base * descuento
         subtotal = costo_base - monto_descuento
         total = subtotal * (1 + impuesto)
         return round(total, 2)
     
     def describir_servicio(self):
         return f" {self._nombre}: {self._descripcion} | Precio base: ${self._precio_base}/hora"

# ==================================================
 # 6. CLASE RESERVA
 # ==================================================
 class Reserva:
     """Clase que representa una reserva con manejo de estados"""
     ESTADOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"}
     
     def _init_(self, identificador, cliente, servicio, duracion):
         self._id = identificador
         self._cliente = cliente
         self._servicio = servicio
         self._duracion = duracion
         self._estado = "PENDIENTE"
         self._fecha_creacion = datetime.now()
         GestorLogs.info(f"Reserva creada: #{self._id} | Cliente: {cliente.nombre} | Servicio: {servicio.nombre}")
     
     @property
     def id(self):
         return self._id
     
     @property
     def estado(self):
         return self._estado
     
     @property
     def cliente(self):
         return self._cliente
     
     @property
     def servicio(self):
         return self._servicio
     
     @property
     def duracion(self):
         return self._duracion
     
     def confirmar(self):
         """Confirmar la reserva con validaciones completas"""
         try:
             if self._estado != "PENDIENTE":
                 raise ReservaInvalidaError(f"No se puede confirmar: estado actual es '{self._estado}'")
             
             if not self._servicio.disponible:
                 raise ServicioNoDisponibleError(f"El servicio '{self._servicio.nombre}' no está disponible")
             
             if self._duracion <= 0:
                 raise ParametroInvalidoError("La duración debe ser mayor a cero")
             
             self._estado = "CONFIRMADA"
             GestorLogs.info(f"Reserva #{self._id}: CONFIRMADA")
             return f"✅ Reserva #{self._id} CONFIRMADA — Cliente: {self._cliente.nombre}"
         
         except (ReservaInvalidaError, ServicioNoDisponibleError, ParametroInvalidoError) as e:
             GestorLogs.error(f"Error al confirmar reserva #{self._id}: {e}")
             raise
         except Exception as e:
             GestorLogs.error(f"Error inesperado al confirmar #{self._id}: {e}")
             raise
         finally:
             pass
     
     def cancelar(self):
         """Cancelar la reserva"""
         try:
             if self._estado == "COMPLETADA":
                 raise ReservaInvalidaError("No se puede cancelar una reserva ya completada")
             
             if self._estado == "CANCELADA":
                 raise ReservaInvalidaError("La reserva ya se encuentra cancelada")
             
             self._estado = "CANCELADA"
             GestorLogs.info(f"Reserva #{self._id}: CANCELADA")
             return f"❌ Reserva #{self._id} CANCELADA — Cliente: {self._cliente.nombre}"
         
         except ReservaInvalidaError as e:
             GestorLogs.error(f"Error al cancelar #{self._id}: {e}")
             raise
     
     def procesar(self):
         """Marcar reserva como completada"""
         if self._estado == "CONFIRMADA":
             self._estado = "COMPLETADA"
             GestorLogs.info(f"Reserva #{self._id}: COMPLETADA")
             return f"✅ Reserva #{self._id} COMPLETADA"
         mensaje = f"⚠️ No se puede procesar #{self._id}: estado = {self._estado}"
         GestorLogs.advertencia(mensaje)
         return mensaje
     
     def calcular_costo_reserva(self, **kwargs):
         """Delega el cálculo al servicio — Polimorfismo"""
         return self._servicio.calcular_costo(self._duracion, **kwargs)
     
     def _str_(self):
         return f"📝 Reserva #{self._id} | Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | Estado: {self._estado}"

 # ==================================================
 # 7. SISTEMA PRINCIPAL
 # ==================================================
 class SistemaGestion:
     """Clase principal que gestiona todo el sistema"""
     
     def _init_(self):
         self._clientes = []
         self._servicios = []
         self._reservas = []
         GestorLogs.info("===== SISTEMA INICIADO =====")
     
     def registrar_cliente(self, cliente):
         try:
             self._clientes.append(cliente)
             return True
         except Exception as e:
             GestorLogs.error(f"Error al registrar cliente: {e}")
             raise
     
     def registrar_servicio(self, servicio):
         self._servicios.append(servicio)
         GestorLogs.info(f"Servicio registrado: {servicio.nombre}")
     
     def crear_reserva(self, reserva):
         self._reservas.append(reserva)
         return reserva
     
     def listar_clientes(self):
         return self._clientes
     
     def listar_servicios(self):
         return self._servicios
     
     def listar_reservas(self):
         return self._reservas
