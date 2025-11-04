"""Módulo excel_consolidator para consolidar archivos Excel extraídos.

Este módulo proporciona herramientas para consolidar archivos Excel
con estructuras simples o complejas (múltiples tablas) en archivos
limpios con datos normalizados.

Características principales:
- Detección automática de estructura (simple/compleja)
- Extracción de datos de múltiples tablas apiladas
- Consolidación en archivos únicos limpios
- Procesamiento individual o en batch

Example:
    >>> from excel_consolidator import ExcelConsolidator
    >>>
    >>> # Consolidar un archivo
    >>> consolidator = ExcelConsolidator()
    >>> result = consolidator.consolidate_file('datos.xlsx')
    >>>
    >>> # Consolidar directorio completo
    >>> with ExcelConsolidator() as cons:
    ...     summary = cons.consolidate_directory('extraido/')
    ...     print(f"Procesados: {summary['successful']}/{summary['total_files']}")

Example:
    >>> # Función helper para consolidación rápida
    >>> from excel_consolidator import consolidate_excel_file
    >>> result = consolidate_excel_file('datos.xlsx')
"""

__version__ = "1.0.0"
__author__ = "Juan P. Guevara"

# Importar clases principales
from .consolidator import ExcelConsolidator
from .batch import BatchConsolidator

# Importar funciones de utilidad
from .detector import (
    StructureType,
    analyze_file_completely,
    detect_structure,
    get_sheet_names,
)
from .extractor import extract_all_sheets, extract_data, preview_data
from .utils import (
    clean_dataframe,
    create_output_filename,
    ensure_output_directory,
    is_likely_header,
    make_unique_column_names,
    normalize_column_names,
)

# API pública
__all__ = [
    # Versión
    "__version__",
    # Clases principales
    "ExcelConsolidator",
    "BatchConsolidator",
    # Detector
    "StructureType",
    "detect_structure",
    "get_sheet_names",
    "analyze_file_completely",
    # Extractor
    "extract_data",
    "extract_all_sheets",
    "preview_data",
    # Utilidades
    "clean_dataframe",
    "create_output_filename",
    "ensure_output_directory",
    "is_likely_header",
    "make_unique_column_names",
    "normalize_column_names",
    # Función helper
    "consolidate_excel_file",
]


def consolidate_excel_file(file_path, output_dir=None, suffix="_consolidado"):
    """Función helper para consolidar un archivo Excel rápidamente.

    Args:
        file_path: Ruta al archivo Excel
        output_dir: Directorio de salida (None = mismo que entrada)
        suffix: Sufijo para el archivo consolidado

    Returns:
        Diccionario con resultado de la consolidación

    Example:
        >>> result = consolidate_excel_file('datos.xlsx')
        >>> if result['success']:
        ...     print(f"Consolidado: {result['output_file']}")
    """
    consolidator = ExcelConsolidator(output_dir=output_dir, suffix=suffix)
    return consolidator.consolidate_file(file_path)
