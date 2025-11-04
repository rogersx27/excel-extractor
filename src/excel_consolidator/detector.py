"""Detector de estructura de archivos Excel.

Este módulo analiza archivos Excel para determinar si tienen:
- Estructura simple: Una tabla con un encabezado
- Estructura compleja: Múltiples tablas apiladas con encabezados repetidos
"""

from pathlib import Path
from typing import Dict, List, Tuple

from openpyxl import load_workbook

from logger import setup_logger

from .utils import count_non_empty_cells, is_empty_row, is_likely_header

logger = setup_logger(__name__)


class StructureType:
    """Tipos de estructura de Excel."""

    SIMPLE = "simple"
    COMPLEX = "complex"
    UNKNOWN = "unknown"


def detect_structure(file_path: Path, sheet_name: str = None) -> Dict:
    """Detecta la estructura de un archivo Excel.

    Args:
        file_path: Ruta al archivo Excel
        sheet_name: Nombre de la hoja a analizar (None = primera hoja)

    Returns:
        Diccionario con información de la estructura:
        {
            'type': 'simple' | 'complex' | 'unknown',
            'header_rows': [list of row indices],
            'data_ranges': [(start_row, end_row), ...],
            'total_rows': int,
            'sheet_name': str
        }

    Example:
        >>> info = detect_structure(Path('datos.xlsx'))
        >>> if info['type'] == 'complex':
        ...     print(f"Encontradas {len(info['header_rows'])} tablas")
    """
    logger.info(f"Analizando estructura de: {file_path}")

    try:
        wb = load_workbook(file_path, read_only=True, data_only=True)

        # Seleccionar hoja
        if sheet_name:
            ws = wb[sheet_name]
        else:
            ws = wb.active

        sheet_name = ws.title
        logger.debug(f"Analizando hoja: {sheet_name}")

        # Analizar filas
        header_rows = []
        data_ranges = []
        all_rows = []

        for idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
            all_rows.append(row)

        total_rows = len(all_rows)

        # Buscar encabezados
        header_rows = find_header_rows(all_rows)

        # Determinar rangos de datos
        data_ranges = determine_data_ranges(all_rows, header_rows)

        # Determinar tipo de estructura
        structure_type = classify_structure(header_rows, data_ranges)

        wb.close()

        result = {
            "type": structure_type,
            "header_rows": header_rows,
            "data_ranges": data_ranges,
            "total_rows": total_rows,
            "sheet_name": sheet_name,
        }

        logger.info(
            f"Estructura detectada: {structure_type.upper()} - "
            f"{len(header_rows)} encabezado(s), {total_rows} filas totales"
        )

        return result

    except Exception as e:
        logger.error(f"Error detectando estructura de {file_path}: {e}")
        raise


def find_header_rows(rows: List[tuple]) -> List[int]:
    """Encuentra las filas que son encabezados.

    Args:
        rows: Lista de tuplas con valores de filas

    Returns:
        Lista de índices (1-based) de filas que son encabezados

    Example:
        >>> rows = [(None,), ('NOMBRE', 'DIRECCIÓN'), ('Juan', 'Calle 1')]
        >>> find_header_rows(rows)
        [2]
    """
    header_rows = []

    for idx, row in enumerate(rows, start=1):
        row_list = list(row)

        # Saltar filas vacías
        if is_empty_row(row_list):
            continue

        # Verificar si es encabezado
        if is_likely_header(row_list):
            header_rows.append(idx)
            logger.debug(f"Encabezado encontrado en fila {idx}")

    return header_rows


def determine_data_ranges(
    rows: List[tuple], header_rows: List[int]
) -> List[Tuple[int, int]]:
    """Determina los rangos de filas que contienen datos.

    Args:
        rows: Lista de tuplas con valores de filas
        header_rows: Índices de filas de encabezados

    Returns:
        Lista de tuplas (start_row, end_row) con rangos de datos

    Example:
        >>> rows = [(...), (...), ...]
        >>> header_rows = [2, 10]
        >>> determine_data_ranges(rows, header_rows)
        [(3, 9), (11, 15)]
    """
    if not header_rows:
        # Si no hay encabezados detectados, asumir que todo es data
        # excepto las primeras filas vacías
        first_data_row = 1
        for idx, row in enumerate(rows, start=1):
            if not is_empty_row(list(row)):
                first_data_row = idx
                break

        return [(first_data_row, len(rows))]

    data_ranges = []

    for i, header_idx in enumerate(header_rows):
        start_row = header_idx + 1

        # Determinar fin del rango
        if i < len(header_rows) - 1:
            # Hay otro encabezado después
            next_header = header_rows[i + 1]
            end_row = next_header - 1
        else:
            # Último encabezado, ir hasta el final
            end_row = len(rows)

        # Ajustar end_row para excluir filas vacías al final
        while end_row > start_row:
            if not is_empty_row(list(rows[end_row - 1])):
                break
            end_row -= 1

        if start_row <= end_row:
            data_ranges.append((start_row, end_row))
            logger.debug(f"Rango de datos: filas {start_row} a {end_row}")

    return data_ranges


def classify_structure(
    header_rows: List[int], data_ranges: List[Tuple[int, int]]
) -> str:
    """Clasifica la estructura del archivo.

    Args:
        header_rows: Índices de encabezados
        data_ranges: Rangos de datos

    Returns:
        Tipo de estructura: 'simple', 'complex', o 'unknown'

    Example:
        >>> classify_structure([2], [(3, 10)])
        'simple'
        >>> classify_structure([2, 15, 28], [(3, 14), (16, 27), (29, 40)])
        'complex'
    """
    if not header_rows:
        return StructureType.UNKNOWN

    if len(header_rows) == 1:
        return StructureType.SIMPLE

    if len(header_rows) > 1:
        return StructureType.COMPLEX

    return StructureType.UNKNOWN


def get_sheet_names(file_path: Path) -> List[str]:
    """Obtiene los nombres de todas las hojas de un archivo Excel.

    Args:
        file_path: Ruta al archivo Excel

    Returns:
        Lista con nombres de hojas

    Example:
        >>> sheets = get_sheet_names(Path('datos.xlsx'))
        >>> print(sheets)
        ['Hoja1', 'Hoja2', 'Resumen']
    """
    try:
        wb = load_workbook(file_path, read_only=True)
        sheet_names = wb.sheetnames
        wb.close()
        return sheet_names
    except Exception as e:
        logger.error(f"Error obteniendo hojas de {file_path}: {e}")
        raise


def analyze_file_completely(file_path: Path) -> Dict:
    """Analiza completamente un archivo Excel (todas sus hojas).

    Args:
        file_path: Ruta al archivo Excel

    Returns:
        Diccionario con análisis de todas las hojas:
        {
            'file_path': Path,
            'total_sheets': int,
            'sheets': {
                'sheet_name': {...estructura...}
            }
        }

    Example:
        >>> analysis = analyze_file_completely(Path('datos.xlsx'))
        >>> for sheet, info in analysis['sheets'].items():
        ...     print(f"{sheet}: {info['type']}")
    """
    logger.info(f"Análisis completo de archivo: {file_path}")

    try:
        sheet_names = get_sheet_names(file_path)
        sheets_info = {}

        for sheet in sheet_names:
            sheets_info[sheet] = detect_structure(file_path, sheet)

        result = {
            "file_path": file_path,
            "total_sheets": len(sheet_names),
            "sheets": sheets_info,
        }

        logger.info(f"Análisis completado: {len(sheet_names)} hojas procesadas")

        return result

    except Exception as e:
        logger.error(f"Error en análisis completo de {file_path}: {e}")
        raise
