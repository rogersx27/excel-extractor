"""Excepciones personalizadas para el módulo excel_handler.

Este módulo define todas las excepciones específicas del dominio
para operaciones con archivos Excel.
"""


class ExcelHandlerError(Exception):
    """Excepción base para todos los errores del excel_handler.

    Todas las excepciones personalizadas heredan de esta clase base,
    permitiendo capturar cualquier error del módulo con un solo except.

    Example:
        >>> try:
        ...     handler.delete_sheet('NonExistent')
        ... except ExcelHandlerError as e:
        ...     print(f"Error en operación Excel: {e}")
    """
    pass


class SheetNotFoundError(ExcelHandlerError):
    """La hoja especificada no existe en el archivo Excel.

    Se lanza cuando se intenta acceder, modificar o eliminar una hoja
    que no está presente en el workbook.

    Example:
        >>> handler.delete_sheet('HojaInexistente')
        SheetNotFoundError: Hoja 'HojaInexistente' no encontrada...
    """
    pass


class InvalidFileFormatError(ExcelHandlerError):
    """El formato del archivo no es válido o no está soportado.

    Se lanza cuando:
    - La extensión del archivo no es soportada (.xlsx, .xlsm, etc.)
    - El archivo está corrupto
    - El archivo no es un Excel válido

    Example:
        >>> handler = ExcelHandler('document.pdf')
        InvalidFileFormatError: Extensión no soportada: .pdf
    """
    pass


class SheetAlreadyExistsError(ExcelHandlerError):
    """Intento de crear una hoja con un nombre que ya existe.

    Se lanza cuando se intenta agregar una hoja con un nombre
    duplicado en el workbook.

    Example:
        >>> handler.add_sheet('Ventas')  # Ya existe
        SheetAlreadyExistsError: La hoja 'Ventas' ya existe...
    """
    pass


class FileOperationError(ExcelHandlerError):
    """Error durante operaciones de archivo (lectura, escritura, permisos).

    Se lanza cuando hay problemas de I/O:
    - Archivo no encontrado
    - Sin permisos de lectura/escritura
    - Disco lleno
    - Archivo abierto en otra aplicación

    Example:
        >>> handler.save()
        FileOperationError: No se puede guardar el archivo (abierto en Excel)
    """
    pass


class EmptyDataError(ExcelHandlerError):
    """Intento de escribir datos vacíos o DataFrame sin filas.

    Se lanza cuando se intenta escribir un DataFrame vacío o None
    a una hoja de Excel.

    Example:
        >>> QuickExcel.write(empty_df, 'output.xlsx')
        EmptyDataError: No se pueden escribir datos vacíos
    """
    pass
