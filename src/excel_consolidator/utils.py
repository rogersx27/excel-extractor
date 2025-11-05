"""Utilidades auxiliares para el consolidador de Excel.

Este módulo proporciona funciones de apoyo para limpiar y procesar datos.
"""

from pathlib import Path
from typing import Any, List, Optional

import pandas as pd

from logger import setup_logger

# Logger Nivel 4 - Utilidades: WARNING solo archivo, helpers silenciosos
logger = setup_logger(
    __name__,
    level="WARNING",
    console_output=False,
    file_output=True
)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Limpia un DataFrame eliminando filas y columnas vacías.

    Args:
        df: DataFrame a limpiar

    Returns:
        DataFrame limpio sin filas/columnas vacías

    Example:
        >>> df = pd.DataFrame({'A': [1, None, 3], 'B': [None, None, None]})
        >>> clean_df = clean_dataframe(df)
        >>> # Elimina columna B (completamente vacía) y fila 1
    """
    if df.empty:
        return df

    # Eliminar columnas completamente vacías
    df = df.dropna(axis=1, how="all")

    # Eliminar filas completamente vacías
    df = df.dropna(axis=0, how="all")

    # Reset index
    df = df.reset_index(drop=True)

    logger.debug(f"DataFrame limpio: {len(df)} filas, {len(df.columns)} columnas")
    return df


def is_empty_row(row: List[Any]) -> bool:
    """Verifica si una fila está completamente vacía.

    Args:
        row: Lista de valores de una fila

    Returns:
        True si la fila está vacía, False en caso contrario

    Example:
        >>> is_empty_row([None, '', None])
        True
        >>> is_empty_row([None, 'dato', None])
        False
    """
    return all(cell is None or str(cell).strip() == "" for cell in row)


def is_likely_header(row: List[Any]) -> bool:
    """Determina si una fila es probablemente un encabezado.

    Un encabezado típicamente:
    - Tiene la mayoría de celdas con contenido
    - Contiene texto (no solo números)
    - Tiene palabras comunes de encabezados

    Args:
        row: Lista de valores de una fila

    Returns:
        True si parece un encabezado, False en caso contrario

    Example:
        >>> is_likely_header(['NOMBRE', 'DIRECCIÓN', 'TELEFONO'])
        True
        >>> is_likely_header([123, 456, 789])
        False
    """
    # Palabras clave comunes en encabezados
    header_keywords = [
        "nombre",
        "dirección",
        "direccion",
        "telefono",
        "teléfono",
        "cliente",
        "usuario",
        "contacto",
        "aceite",
        "respel",
        "cantidad",
        "municipio",
        "ruta",
        "fecha",
        "código",
        "codigo",
        "NIT",
        "EMPRESA",
        "DIRECCION",
        "SECTOR",
        "ENCARGADO",
        "TELEFONOS",
        "CORREOS",
        "FRECUENCIA",
        "OBSERVACIONES",
        "PRODUCTO Y CANTIDAD",
        "FECHA ULTIMA LLAMADA",
        "FECHA DE RECOLECCION"
    ]

    # Filtrar valores no vacíos
    non_empty = [cell for cell in row if cell is not None and str(cell).strip() != ""]

    if len(non_empty) < 2:
        return False

    # Contar cuántos valores contienen palabras clave
    keyword_count = 0
    text_count = 0

    for cell in non_empty:
        cell_str = str(cell).lower().strip()

        # Verificar si es texto (no solo números)
        if not cell_str.replace(".", "").replace(",", "").isdigit():
            text_count += 1

        # Verificar palabras clave
        if any(keyword in cell_str for keyword in header_keywords):
            keyword_count += 1

    # Es encabezado si tiene suficiente texto y palabras clave
    has_enough_text = text_count >= len(non_empty) * 0.7
    has_keywords = keyword_count >= 2

    return has_enough_text and has_keywords


def create_output_filename(input_path: Path, suffix: str = "_consolidado") -> str:
    """Crea el nombre del archivo de salida basado en el archivo de entrada.

    Args:
        input_path: Ruta del archivo de entrada
        suffix: Sufijo a añadir al nombre (default: "_consolidado")

    Returns:
        Nombre del archivo de salida

    Example:
        >>> path = Path("01_RUTA 113.xlsx")
        >>> create_output_filename(path)
        '01_RUTA 113_consolidado.xlsx'
    """
    stem = input_path.stem
    extension = input_path.suffix
    return f"{stem}{suffix}{extension}"


def ensure_output_directory(base_dir: Path, subdir: str = "consolidado") -> Path:
    """Asegura que el directorio de salida existe.

    Args:
        base_dir: Directorio base
        subdir: Subdirectorio a crear (default: "consolidado")

    Returns:
        Path del directorio de salida creado

    Example:
        >>> base = Path("data/extraido")
        >>> output_dir = ensure_output_directory(base)
        >>> # Crea: data/extraido/consolidado/
    """
    output_dir = base_dir / subdir
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Directorio de salida asegurado: {output_dir}")
    return output_dir


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza los nombres de columnas del DataFrame.

    - Convierte a mayúsculas
    - Elimina espacios extra
    - Reemplaza espacios por guiones bajos

    Args:
        df: DataFrame a normalizar

    Returns:
        DataFrame con nombres de columnas normalizados

    Example:
        >>> df = pd.DataFrame({'Nombre Cliente': [1], '  Dirección ': [2]})
        >>> normalized = normalize_column_names(df)
        >>> list(normalized.columns)
        ['NOMBRE_CLIENTE', 'DIRECCION']
    """
    df = df.copy()
    df.columns = [str(col).strip().upper().replace(" ", "_") for col in df.columns]
    return df


def count_non_empty_cells(row: List[Any]) -> int:
    """Cuenta el número de celdas no vacías en una fila.

    Args:
        row: Lista de valores de una fila

    Returns:
        Número de celdas con contenido

    Example:
        >>> count_non_empty_cells(['A', None, 'B', ''])
        2
    """
    return sum(1 for cell in row if cell is not None and str(cell).strip() != "")
