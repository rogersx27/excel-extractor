"""Funciones utilitarias para operaciones complejas con múltiples archivos Excel.

Este módulo proporciona funciones para:
- Combinar múltiples archivos Excel
- Dividir archivos Excel por valores de columna
- Otras operaciones batch sobre archivos Excel
"""
from pathlib import Path
from typing import List, Optional, Union

import pandas as pd

from logger import setup_logger
from .exceptions import EmptyDataError, FileOperationError

logger = setup_logger(__name__)


def merge_excel_files(
    file_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None,
    ignore_errors: bool = False
) -> pd.DataFrame:
    """Combina múltiples archivos Excel en uno solo.

    Lee la misma hoja de múltiples archivos y las combina verticalmente
    en un único DataFrame, que luego guarda en un archivo de salida.

    Args:
        file_paths: Lista de rutas de archivos a combinar
        output_path: Ruta del archivo de salida
        sheet_name: Nombre o índice de la hoja a leer (None = primera hoja)
        ignore_errors: Si True, ignora archivos con errores (default: False)

    Returns:
        DataFrame combinado con todos los datos

    Raises:
        FileNotFoundError: Si algún archivo no existe
        EmptyDataError: Si no se pudieron leer archivos o todos están vacíos
        FileOperationError: Si hay error al procesar archivos

    Example:
        >>> files = ['ventas_enero.xlsx', 'ventas_febrero.xlsx', 'ventas_marzo.xlsx']
        >>> df = merge_excel_files(files, 'ventas_trimestre.xlsx')
        >>> print(f"Total filas: {len(df)}")
        >>>
        >>> # Especificar hoja y manejar errores
        >>> df = merge_excel_files(
        ...     files,
        ...     'salida.xlsx',
        ...     sheet_name='Ventas',
        ...     ignore_errors=True
        ... )
    """
    if not file_paths:
        raise EmptyDataError("La lista de archivos está vacía")

    logger.info(f"Combinando {len(file_paths)} archivos Excel")

    dataframes = []
    errors = []

    for file_path in file_paths:
        path = Path(file_path)

        # Verificar que el archivo existe
        if not path.exists():
            error_msg = f"Archivo no encontrado: {path}"
            if ignore_errors:
                logger.warning(error_msg)
                errors.append(error_msg)
                continue
            else:
                raise FileNotFoundError(error_msg)

        # Intentar leer el archivo
        try:
            df = pd.read_excel(path, sheet_name=sheet_name or 0)

            if df.empty:
                logger.warning(f"Archivo vacío (se omitirá): {path}")
                continue

            dataframes.append(df)
            logger.info(f"Leído: {path} ({len(df)} filas)")

        except Exception as e:
            error_msg = f"Error leyendo {path}: {e}"
            if ignore_errors:
                logger.warning(error_msg)
                errors.append(error_msg)
                continue
            else:
                raise FileOperationError(error_msg) from e

    # Verificar que se leyó al menos un archivo
    if not dataframes:
        raise EmptyDataError(
            "No se pudo leer ningún archivo. "
            f"Errores encontrados: {len(errors)}"
        )

    # Combinar todos los DataFrames
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Crear directorio de salida si no existe
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Guardar archivo combinado
    try:
        combined_df.to_excel(output_path, index=False)
        logger.info(
            f"Archivos combinados guardados en: {output_path} "
            f"({len(combined_df)} filas totales, {len(dataframes)} archivos procesados)"
        )

        if errors:
            logger.warning(f"Se encontraron {len(errors)} errores durante el proceso")

    except Exception as e:
        raise FileOperationError(f"Error guardando archivo combinado: {e}") from e

    return combined_df


def split_excel_by_column(
    file_path: Union[str, Path],
    column_name: str,
    output_dir: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None,
    prefix: str = "",
    suffix: str = ""
) -> dict:
    """Divide un Excel en múltiples archivos basándose en valores de una columna.

    Crea un archivo Excel separado por cada valor único encontrado en la
    columna especificada.

    Args:
        file_path: Ruta del archivo Excel a dividir
        column_name: Nombre de la columna para dividir
        output_dir: Directorio donde guardar los archivos resultantes
        sheet_name: Nombre o índice de la hoja a procesar (None = primera)
        prefix: Prefijo para nombres de archivos generados (default: "")
        suffix: Sufijo para nombres de archivos generados (default: "")

    Returns:
        Diccionario con {valor: ruta_archivo} para cada archivo creado

    Raises:
        FileNotFoundError: Si el archivo no existe
        KeyError: Si la columna no existe en el DataFrame
        EmptyDataError: Si el archivo está vacío
        FileOperationError: Si hay error al procesar

    Example:
        >>> # Dividir ventas.xlsx por región
        >>> files = split_excel_by_column(
        ...     'ventas.xlsx',
        ...     'Región',
        ...     'salida/'
        ... )
        >>> # Crea: salida/Norte.xlsx, salida/Sur.xlsx, etc.
        >>>
        >>> # Con prefijo y sufijo
        >>> files = split_excel_by_column(
        ...     'datos.xlsx',
        ...     'Categoría',
        ...     'resultados/',
        ...     prefix='cat_',
        ...     suffix='_2024'
        ... )
        >>> # Crea: resultados/cat_A_2024.xlsx, resultados/cat_B_2024.xlsx, etc.
    """
    file_path = Path(file_path)

    # Validar que el archivo existe
    if not file_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

    logger.info(f"Dividiendo Excel por columna: {column_name}")

    # Leer el archivo
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name or 0)
    except Exception as e:
        raise FileOperationError(f"Error leyendo archivo {file_path}: {e}") from e

    # Validar que el DataFrame no esté vacío
    if df.empty:
        raise EmptyDataError(f"El archivo {file_path} está vacío")

    # Validar que la columna existe
    if column_name not in df.columns:
        raise KeyError(
            f"Columna '{column_name}' no encontrada. "
            f"Columnas disponibles: {', '.join(df.columns)}"
        )

    # Crear directorio de salida
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Diccionario para almacenar archivos creados
    created_files = {}

    # Obtener valores únicos de la columna
    unique_values = df[column_name].unique()

    logger.info(
        f"Encontrados {len(unique_values)} valores únicos en '{column_name}'"
    )

    # Dividir y guardar
    for value in unique_values:
        # Filtrar datos para este valor
        filtered_df = df[df[column_name] == value]

        # Generar nombre de archivo (sanitizar el valor para nombre de archivo)
        safe_value = str(value).replace('/', '_').replace('\\', '_')
        file_name = f"{prefix}{safe_value}{suffix}.xlsx"
        output_file = output_dir / file_name

        # Guardar archivo
        try:
            filtered_df.to_excel(output_file, index=False)
            created_files[value] = output_file
            logger.info(
                f"Archivo creado: {output_file} "
                f"({len(filtered_df)} filas para '{value}')"
            )
        except Exception as e:
            logger.error(f"Error guardando {output_file}: {e}")
            raise FileOperationError(
                f"Error guardando archivo para '{value}': {e}"
            ) from e

    logger.info(
        f"División completada: {len(created_files)} archivos creados en {output_dir}"
    )

    return created_files


def compare_excel_files(
    file1: Union[str, Path],
    file2: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None
) -> dict:
    """Compara dos archivos Excel y retorna las diferencias.

    Args:
        file1: Ruta del primer archivo
        file2: Ruta del segundo archivo
        sheet_name: Hoja a comparar (None = primera hoja)

    Returns:
        Diccionario con información de diferencias:
        - 'are_equal': bool
        - 'shape_equal': bool
        - 'columns_equal': bool
        - 'diff_rows': int (número de filas diferentes)

    Example:
        >>> result = compare_excel_files('version1.xlsx', 'version2.xlsx')
        >>> if result['are_equal']:
        ...     print('Los archivos son idénticos')
        ... else:
        ...     print(f"Diferencias en {result['diff_rows']} filas")
    """
    logger.info(f"Comparando: {file1} vs {file2}")

    # Leer ambos archivos
    df1 = pd.read_excel(file1, sheet_name=sheet_name or 0)
    df2 = pd.read_excel(file2, sheet_name=sheet_name or 0)

    # Comparar
    result = {
        'are_equal': df1.equals(df2),
        'shape_equal': df1.shape == df2.shape,
        'columns_equal': list(df1.columns) == list(df2.columns),
        'shape1': df1.shape,
        'shape2': df2.shape,
        'diff_rows': 0
    }

    # Si las formas son iguales, contar filas diferentes
    if result['shape_equal']:
        comparison = df1 != df2
        result['diff_rows'] = comparison.any(axis=1).sum()

    logger.info(f"Comparación completada: iguales={result['are_equal']}")

    return result
