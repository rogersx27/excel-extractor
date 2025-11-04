"""Ejemplos de uso del sistema de logging.

Este archivo demuestra cómo usar el sistema de logging comprehensivo
del proyecto.
"""
import sys
import time
from pathlib import Path

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import (
    setup_logger,
    get_logger,
    configure_root_logger,
    log_function_call,
    create_module_logger
)


def ejemplo_1_uso_basico():
    """Ejemplo 1: Uso básico del logger."""
    print("\n" + "="*60)
    print("EJEMPLO 1: Uso Básico")
    print("="*60 + "\n")

    # Crear logger con configuración por defecto
    logger = setup_logger(__name__)

    # Diferentes niveles de log
    logger.debug("Mensaje de DEBUG - detalles técnicos")
    logger.info("Mensaje de INFO - información general")
    logger.warning("Mensaje de WARNING - advertencia")
    logger.error("Mensaje de ERROR - error encontrado")
    logger.critical("Mensaje de CRITICAL - error crítico")

    print("\n✓ Los logs se guardaron en logs/YYYY-MM-DD.log")


def ejemplo_2_logger_con_debug():
    """Ejemplo 2: Logger con nivel DEBUG."""
    print("\n" + "="*60)
    print("EJEMPLO 2: Logger con nivel DEBUG")
    print("="*60 + "\n")

    # Logger con nivel DEBUG para ver todos los mensajes
    logger = setup_logger("debug_module", level="DEBUG")

    logger.debug("Este mensaje DEBUG ahora es visible")
    logger.info("Procesando archivo datos.xlsx")
    logger.warning("Memoria en 80%")


def ejemplo_3_logger_solo_archivo():
    """Ejemplo 3: Logger solo para archivo (sin consola)."""
    print("\n" + "="*60)
    print("EJEMPLO 3: Logger Solo Archivo (sin salida en consola)")
    print("="*60 + "\n")

    # Logger que solo escribe en archivo, no en consola
    logger = setup_logger(
        "silent_logger",
        console_output=False,
        file_output=True
    )

    logger.info("Este mensaje solo aparece en el archivo de log")
    logger.warning("No verás esto en la consola")

    print("✓ Los mensajes fueron escritos solo en el archivo de log")


def ejemplo_4_logger_personalizado():
    """Ejemplo 4: Logger con directorio personalizado."""
    print("\n" + "="*60)
    print("EJEMPLO 4: Logger con Directorio Personalizado")
    print("="*60 + "\n")

    # Crear directorio personalizado para logs
    custom_dir = Path("logs/custom")

    logger = setup_logger(
        "custom_logger",
        log_dir=custom_dir
    )

    logger.info("Log guardado en directorio personalizado")
    logger.warning("Revisar logs/custom/YYYY-MM-DD.log")

    print(f"✓ Los logs se guardaron en {custom_dir}")


def ejemplo_5_decorador_log():
    """Ejemplo 5: Decorador para loguear funciones automáticamente."""
    print("\n" + "="*60)
    print("EJEMPLO 5: Decorador de Funciones")
    print("="*60 + "\n")

    logger = setup_logger("decorated_module", level="DEBUG")

    @log_function_call(logger)
    def sumar(a, b):
        """Función simple que suma dos números."""
        time.sleep(0.1)  # Simular procesamiento
        return a + b

    @log_function_call(logger)
    def dividir(a, b):
        """Función que puede generar error."""
        return a / b

    # Llamadas normales - se loguean automáticamente
    resultado1 = sumar(5, 3)
    print(f"Resultado suma: {resultado1}")

    # Llamada que genera error - se loguea el error
    try:
        resultado2 = dividir(10, 0)
    except ZeroDivisionError:
        print("Error capturado y logueado automáticamente")


def ejemplo_6_multiples_modulos():
    """Ejemplo 6: Diferentes loggers para diferentes módulos."""
    print("\n" + "="*60)
    print("EJEMPLO 6: Múltiples Módulos con Diferentes Niveles")
    print("="*60 + "\n")

    # Logger para módulo de base de datos (muy detallado)
    db_logger = create_module_logger("database", level="DEBUG")
    db_logger.debug("Conectando a base de datos...")
    db_logger.info("Conexión establecida")

    # Logger para módulo de API (menos detallado)
    api_logger = create_module_logger("api", level="INFO")
    api_logger.debug("Este DEBUG no se muestra porque el nivel es INFO")
    api_logger.info("Request recibido: GET /users")

    # Logger para módulo de seguridad (solo warnings y errores)
    security_logger = create_module_logger("security", level="WARNING")
    security_logger.info("Este INFO no se muestra")
    security_logger.warning("Intento de acceso no autorizado")


def ejemplo_7_contexto_rico():
    """Ejemplo 7: Logs con contexto rico."""
    print("\n" + "="*60)
    print("EJEMPLO 7: Logs con Contexto Rico")
    print("="*60 + "\n")

    logger = setup_logger("contexto_module")

    # Log con información estructurada
    user_id = 12345
    action = "login"
    ip = "192.168.1.100"

    logger.info(f"Usuario {user_id} realizó {action} desde {ip}")

    # Log con variables
    archivo = "datos.xlsx"
    filas = 1500
    columnas = 25

    logger.info(f"Procesando {archivo}: {filas} filas, {columnas} columnas")

    # Log de progreso
    total = 100
    for i in range(0, 101, 20):
        logger.info(f"Progreso: {i}/{total} ({i}%)")
        time.sleep(0.1)


def ejemplo_8_manejo_errores():
    """Ejemplo 8: Logging de excepciones con trazas completas."""
    print("\n" + "="*60)
    print("EJEMPLO 8: Logging de Excepciones")
    print("="*60 + "\n")

    logger = setup_logger("error_module")

    def funcion_problematica():
        """Función que genera una excepción."""
        datos = [1, 2, 3]
        return datos[10]  # IndexError

    try:
        funcion_problematica()
    except Exception as e:
        # Loguear con exc_info=True para incluir el traceback completo
        logger.error(f"Error al procesar datos: {e}", exc_info=True)
        print("✓ Error logueado con traceback completo en el archivo")


def ejemplo_9_configuracion_global():
    """Ejemplo 9: Configuración global del logging."""
    print("\n" + "="*60)
    print("EJEMPLO 9: Configuración Global")
    print("="*60 + "\n")

    # Configurar logging global para toda la aplicación
    configure_root_logger(level="INFO")

    # Ahora cualquier logger funcionará automáticamente
    import logging

    logger1 = logging.getLogger("modulo1")
    logger1.info("Mensaje desde módulo 1")

    logger2 = logging.getLogger("modulo2")
    logger2.info("Mensaje desde módulo 2")

    print("✓ Configuración global aplicada a todos los loggers")


def ejemplo_10_caso_real():
    """Ejemplo 10: Caso de uso real - procesamiento de Excel."""
    print("\n" + "="*60)
    print("EJEMPLO 10: Caso Real - Procesamiento de Excel")
    print("="*60 + "\n")

    logger = setup_logger("excel_processor", level="DEBUG")

    # Simular procesamiento de Excel
    archivos = ["ventas_2024.xlsx", "clientes.xlsx", "inventario.xlsx"]

    logger.info("Iniciando procesamiento de archivos Excel")

    for i, archivo in enumerate(archivos, 1):
        logger.debug(f"Procesando archivo {i}/{len(archivos)}: {archivo}")

        # Simular lectura
        logger.debug(f"Leyendo {archivo}...")
        time.sleep(0.2)

        # Simular procesamiento
        filas = 100 * i
        logger.info(f"Archivo {archivo} cargado: {filas} filas")

        # Simular validación
        logger.debug("Validando datos...")
        time.sleep(0.1)

        if i == 2:
            logger.warning(f"Advertencia en {archivo}: 5 filas con datos incompletos")

        logger.info(f"✓ {archivo} procesado exitosamente")

    logger.info(f"Procesamiento completado: {len(archivos)} archivos")


def ejecutar_todos_ejemplos():
    """Ejecuta todos los ejemplos."""
    print("\n" + "█"*60)
    print("  EJEMPLOS DEL SISTEMA DE LOGGING")
    print("█"*60)

    ejemplos = [
        ejemplo_1_uso_basico,
        ejemplo_2_logger_con_debug,
        ejemplo_3_logger_solo_archivo,
        ejemplo_4_logger_personalizado,
        ejemplo_5_decorador_log,
        ejemplo_6_multiples_modulos,
        ejemplo_7_contexto_rico,
        ejemplo_8_manejo_errores,
        ejemplo_9_configuracion_global,
        ejemplo_10_caso_real,
    ]

    for ejemplo in ejemplos:
        try:
            ejemplo()
            time.sleep(0.5)
        except Exception as e:
            print(f"\n❌ Error en {ejemplo.__name__}: {e}")

    print("\n" + "█"*60)
    print("  TODOS LOS EJEMPLOS COMPLETADOS")
    print("█"*60)
    print(f"\n📁 Revisa los logs en: logs/{Path('logs').resolve()}")
    print("   Cada día se crea un archivo nuevo: YYYY-MM-DD.log")


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejecutar_todos_ejemplos()

    # O ejecutar un ejemplo específico:
    # ejemplo_1_uso_basico()
    # ejemplo_5_decorador_log()
    # etc...
