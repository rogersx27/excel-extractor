"""Paquete de logging comprehensivo con archivos por fecha.

Este paquete proporciona un sistema de logging fácil de usar con:
- Archivos organizados por fecha (YYYY-MM-DD.log)
- Salida en consola con colores
- Configuración flexible por módulo
- Configuración dinámica basada en variables de entorno

Uso básico:
    from logger import setup_logger
    logger = setup_logger(__name__)
    logger.info("Mensaje")

Uso con categorías (recomendado):
    from logger import setup_logger, setup_cli_logger
    logger = setup_cli_logger(setup_logger, __name__)
"""

from .logging_config import (
    setup_logger,
    get_logger,
    configure_root_logger,
    log_function_call,
    create_module_logger,
    DateBasedFileHandler,
)

from .config_helper import (
    setup_cli_logger,
    setup_coordinator_logger,
    setup_processor_logger,
    setup_utils_logger,
    LoggerCategory,
    get_logger_config,
)

__all__ = [
    # Core logging functions
    "setup_logger",
    "get_logger",
    "configure_root_logger",
    "log_function_call",
    "create_module_logger",
    "DateBasedFileHandler",
    # Category-based helpers
    "setup_cli_logger",
    "setup_coordinator_logger",
    "setup_processor_logger",
    "setup_utils_logger",
    "LoggerCategory",
    "get_logger_config",
]

__version__ = "1.1.0"
