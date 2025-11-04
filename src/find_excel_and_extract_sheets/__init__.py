"""Módulo simplificado para búsqueda y extracción de hojas Excel.

Este módulo permite buscar archivos Excel en directorios de forma recursiva
y extraer sus hojas en archivos separados automáticamente.

Uso básico:
    from find_excel_and_extract_sheets import find_and_extract_excel_sheets

    # Procesamiento automático
    result = find_and_extract_excel_sheets("mi_directorio")
    print(f"Procesados: {result['successful']}/{result['total_files']}")

Uso avanzado:
    from find_excel_and_extract_sheets import ExcelProcessor

    # Control total del proceso
    processor = ExcelProcessor(
        output_base_dir="salida/",
        max_workers=4
    )
    excel_files = processor.find_excel_files("directorio")
    result = processor.process_files(excel_files, parallel=True)
"""

from .core import (
    ExcelProcessor,
    find_and_extract_excel_sheets,
    scan_directory,
)

__all__ = [
    "ExcelProcessor",
    "find_and_extract_excel_sheets",
    "scan_directory",
]

__version__ = "2.0.0"  # Version simplificada
