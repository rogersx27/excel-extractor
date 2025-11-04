"""Utilidades para el extractor de hojas Excel."""
import re


def clean_filename(filename: str) -> str:
    """
    Limpia un nombre de archivo eliminando caracteres no válidos.

    Args:
        filename: Nombre del archivo a limpiar

    Returns:
        str: Nombre de archivo limpio

    Example:
        >>> clean_filename('Hoja 1: Datos/Info.xlsx')
        'Hoja 1_ Datos_Info.xlsx'
    """
    # Caracteres no válidos en nombres de archivo de Windows y Unix
    invalid_chars = '<>:"/\\|?*'

    # Reemplazar caracteres inválidos con guión bajo
    for char in invalid_chars:
        filename = filename.replace(char, '_')

    # Eliminar espacios múltiples y normalizar
    filename = ' '.join(filename.split())

    # Eliminar puntos al inicio o final (excepto la extensión)
    parts = filename.rsplit('.', 1)
    if len(parts) == 2:
        name, ext = parts
        name = name.strip('. ')
        filename = f"{name}.{ext}"
    else:
        filename = filename.strip('. ')

    return filename


def sanitize_sheet_name(sheet_name: str, max_length: int = 31) -> str:
    """
    Sanitiza un nombre de hoja para Excel.

    Excel tiene restricciones en nombres de hojas:
    - Máximo 31 caracteres
    - No puede contener: [ ] : * ? / \\

    Args:
        sheet_name: Nombre de hoja a sanitizar
        max_length: Longitud máxima (default: 31)

    Returns:
        str: Nombre de hoja sanitizado

    Example:
        >>> sanitize_sheet_name('Datos/Ventas 2024: Resumen')
        'Datos_Ventas 2024_ Resumen'
    """
    # Caracteres prohibidos en nombres de hojas Excel
    invalid_chars = r'[\[\]:*?/\\]'

    # Reemplazar caracteres inválidos
    clean_name = re.sub(invalid_chars, '_', sheet_name)

    # Truncar si es muy largo
    if len(clean_name) > max_length:
        clean_name = clean_name[:max_length]

    # Eliminar espacios al inicio/final
    clean_name = clean_name.strip()

    return clean_name


def format_bytes(bytes_size: int) -> str:
    """
    Formatea tamaño de archivo en formato legible.

    Args:
        bytes_size: Tamaño en bytes

    Returns:
        str: Tamaño formateado (ej: "1.5 MB")

    Example:
        >>> format_bytes(1536)
        '1.5 KB'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} PB"
