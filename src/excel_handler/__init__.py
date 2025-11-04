"""Módulo excel_handler para manipulación avanzada de archivos Excel.

Este módulo proporciona herramientas completas para trabajar con archivos Excel:

- QuickExcel: Operaciones rápidas de una línea (lectura/escritura simple)
- ExcelHandler: Manipulación avanzada multi-hoja con context manager
- Utilidades: merge_excel_files, split_excel_by_column, compare_excel_files
- Excepciones: Manejo de errores específico del dominio

Example:
    >>> from excel_handler import QuickExcel, ExcelHandler
    >>>
    >>> # Operación rápida
    >>> df = QuickExcel.read('datos.xlsx')
    >>> QuickExcel.write(df, 'salida.xlsx')
    >>>
    >>> # Operación compleja multi-hoja
    >>> with ExcelHandler('reporte.xlsx') as excel:
    ...     excel.add_sheet('Ventas', df_ventas)
    ...     excel.add_sheet('Resumen', df_resumen)
    ...     excel.rename_sheet('Sheet1', 'Principal')
    ...     excel.save()

"""

# Importar versión
__version__ = "2.0.0"
__author__ = "Juan P. Guevara"

# Importar clases principales
from .quick import QuickExcel
from .handler import ExcelHandler

# Importar utilidades
from .utils import (
    merge_excel_files,
    split_excel_by_column,
    compare_excel_files,
)

# Importar excepciones
from .exceptions import (
    ExcelHandlerError,
    SheetNotFoundError,
    InvalidFileFormatError,
    SheetAlreadyExistsError,
    FileOperationError,
    EmptyDataError,
)

# Definir API pública
__all__ = [
    # Versión
    "__version__",
    # Clases principales
    "QuickExcel",
    "ExcelHandler",
    # Utilidades
    "merge_excel_files",
    "split_excel_by_column",
    "compare_excel_files",
    # Excepciones
    "ExcelHandlerError",
    "SheetNotFoundError",
    "InvalidFileFormatError",
    "SheetAlreadyExistsError",
    "FileOperationError",
    "EmptyDataError",
]
