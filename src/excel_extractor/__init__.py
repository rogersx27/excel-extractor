"""Módulo para extraer hojas de archivos Excel a archivos individuales.

Este módulo proporciona herramientas para dividir un archivo Excel con
múltiples hojas en archivos separados, uno por cada hoja.

Uso básico:
    from excel_extractor import extract_excel_sheets
    from pathlib import Path

    # Extraer todas las hojas
    result = extract_excel_sheets(Path("archivo.xlsx"))

    # Extraer hojas específicas
    result = extract_excel_sheets(
        Path("archivo.xlsx"),
        sheet_names=["Hoja1", "Hoja2"]
    )

Uso avanzado:
    from excel_extractor import ExcelSheetExtractor

    # Control total del proceso
    extractor = ExcelSheetExtractor(Path("archivo.xlsx"))
    sheet_names = extractor.get_sheet_names()
    print(f"Hojas: {sheet_names}")

    result = extractor.extract_all_sheets(with_index=True)
"""

from .extractor import ExcelSheetExtractor, extract_excel_sheets
from .utils import clean_filename, sanitize_sheet_name, format_bytes

__all__ = [
    # Clase principal
    "ExcelSheetExtractor",

    # Función helper
    "extract_excel_sheets",

    # Utilidades
    "clean_filename",
    "sanitize_sheet_name",
    "format_bytes",
]

__version__ = "1.0.0"
