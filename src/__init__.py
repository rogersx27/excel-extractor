"""Paquete principal del proyecto ascrudos.

Módulos disponibles:
- excel_handler: Manipulación central de archivos Excel
- excel_extractor: Extracción de hojas individuales de Excel
- find_excel_and_extract_sheets: Búsqueda y extracción masiva de hojas Excel
- logger: Sistema de logging comprehensivo
- config: Configuración del proyecto
"""

from .excel_handler import ExcelHandler
from .excel_extractor import extract_excel_sheets, ExcelSheetExtractor
from .find_excel_and_extract_sheets import (
    find_and_extract_excel_sheets,
    scan_directory_info,
    ProcessingStrategy,
    ExcelFinder,
    ExcelBatchProcessor
)
from .logger import setup_logger

__all__ = [
    'ExcelHandler',
    'extract_excel_sheets',
    'ExcelSheetExtractor',
    'find_and_extract_excel_sheets',
    'scan_directory_info',
    'ProcessingStrategy',
    'ExcelFinder',
    'ExcelBatchProcessor',
    'setup_logger'
]