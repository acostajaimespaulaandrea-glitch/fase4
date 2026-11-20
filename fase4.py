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
