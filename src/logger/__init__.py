"""Paquete de logging comprehensivo con archivos por fecha.

Este paquete proporciona un sistema de logging fácil de usar con:
- Archivos organizados por fecha (YYYY-MM-DD.log)
- Salida en consola con colores
- Configuración flexible por módulo

Uso rápido:
    from logger import setup_logger

    logger = setup_logger(__name__)
    logger.info("Mensaje")
"""

from .logging_config import (
    setup_logger,
    get_logger,
    configure_root_logger,
    log_function_call,
    create_module_logger,
    DateBasedFileHandler,
)

__all__ = [
    "setup_logger",
    "get_logger",
    "configure_root_logger",
    "log_function_call",
    "create_module_logger",
    "DateBasedFileHandler",
]

__version__ = "1.0.0"
