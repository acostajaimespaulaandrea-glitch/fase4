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
