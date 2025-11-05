"""Operaciones rápidas de Excel sin gestión de estado.

Este módulo proporciona la clase QuickExcel para operaciones simples
de una línea que no requieren mantener archivos abiertos o gestionar estado.

Use QuickExcel para:
- Leer un archivo Excel rápidamente
- Escribir un DataFrame a Excel
- Crear archivos con formato básico

Use ExcelHandler (handler.py) para:
- Manipulación multi-hoja
- Operaciones complejas
- Modificar archivos existentes
"""
from pathlib import Path
from typing import Dict, Optional, Union

import pandas as pd
import xlsxwriter

from logger import setup_logger, setup_processor_logger
from .exceptions import EmptyDataError, InvalidFileFormatError

# Logger Nivel 3 - Procesador: Configuración dinámica desde variables de entorno
logger = setup_processor_logger(setup_logger, __name__)


class QuickExcel:
    """Operaciones rápidas de Excel sin gestión de estado.

    Todos los métodos son estáticos y no requieren instanciar la clase.
    Ideal para scripts simples y operaciones de una sola línea.

    Example:
        >>> # Lectura rápida
        >>> df = QuickExcel.read('ventas.xlsx')
        >>>
        >>> # Escritura rápida
        >>> QuickExcel.write(df, 'salida.xlsx')
        >>>
        >>> # Leer todas las hojas
        >>> sheets = QuickExcel.read_all_sheets('reporte.xlsx')
    """

    # Extensiones soportadas
    VALID_EXTENSIONS = {'.xlsx', '.xlsm', '.xltx', '.xltm', '.xls', '.xlsb'}

    @staticmethod
    def _validate_file_path(file_path: Union[str, Path], check_exists: bool = False) -> Path:
        """Valida que la ruta del archivo sea correcta.

        Args:
            file_path: Ruta del archivo a validar
            check_exists: Si True, verifica que el archivo exista

        Returns:
            Path object validado

        Raises:
            InvalidFileFormatError: Si la extensión no es válida
            FileNotFoundError: Si check_exists=True y el archivo no existe
        """
        path = Path(file_path)

        # Validar extensión
        if path.suffix.lower() not in QuickExcel.VALID_EXTENSIONS:
            raise InvalidFileFormatError(
                f"Extensión no soportada: {path.suffix}. "
                f"Extensiones válidas: {', '.join(QuickExcel.VALID_EXTENSIONS)}"
            )

        # Validar existencia si se requiere
        if check_exists and not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")

        return path

    @staticmethod
    def read(
        file_path: Union[str, Path],
        sheet: Optional[Union[str, int]] = 0,
        **kwargs
    ) -> pd.DataFrame:
        """Lee un archivo Excel y retorna un DataFrame.

        Args:
            file_path: Ruta al archivo Excel
            sheet: Nombre o índice de la hoja (default: primera hoja)
            **kwargs: Argumentos adicionales para pd.read_excel
                     (usecols, skiprows, nrows, etc.)

        Returns:
            DataFrame con los datos del Excel

        Raises:
            FileNotFoundError: Si el archivo no existe
            InvalidFileFormatError: Si la extensión no es válida

        Example:
            >>> # Leer primera hoja
            >>> df = QuickExcel.read('datos.xlsx')
            >>>
            >>> # Leer hoja específica
            >>> df = QuickExcel.read('datos.xlsx', sheet='Ventas')
            >>>
            >>> # Leer con opciones
            >>> df = QuickExcel.read('datos.xlsx', sheet=0, skiprows=2, usecols='A:D')
        """
        path = QuickExcel._validate_file_path(file_path, check_exists=True)
        logger.info(f"Leyendo Excel: {path} (hoja: {sheet})")

        try:
            return pd.read_excel(path, sheet_name=sheet, **kwargs)
        except Exception as e:
            logger.error(f"Error leyendo Excel {path}: {e}")
            raise

    @staticmethod
    def read_all_sheets(file_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
        """Lee todas las hojas de un Excel en un diccionario de DataFrames.

        Args:
            file_path: Ruta al archivo Excel

        Returns:
            Diccionario con {nombre_hoja: DataFrame}

        Raises:
            FileNotFoundError: Si el archivo no existe
            InvalidFileFormatError: Si la extensión no es válida

        Example:
            >>> sheets = QuickExcel.read_all_sheets('reporte.xlsx')
            >>> for name, df in sheets.items():
            ...     print(f"Hoja: {name}, Filas: {len(df)}")
        """
        path = QuickExcel._validate_file_path(file_path, check_exists=True)
        logger.info(f"Leyendo todas las hojas: {path}")

        try:
            return pd.read_excel(path, sheet_name=None)
        except Exception as e:
            logger.error(f"Error leyendo hojas de {path}: {e}")
            raise

    @staticmethod
    def write(
        df: pd.DataFrame,
        file_path: Union[str, Path],
        sheet_name: str = 'Sheet1',
        index: bool = False,
        **kwargs
    ):
        """Escribe un DataFrame a un archivo Excel.

        Args:
            df: DataFrame a escribir
            file_path: Ruta del archivo de salida
            sheet_name: Nombre de la hoja (default: 'Sheet1')
            index: Incluir el índice del DataFrame (default: False)
            **kwargs: Argumentos adicionales para df.to_excel

        Raises:
            EmptyDataError: Si el DataFrame está vacío
            InvalidFileFormatError: Si la extensión no es válida

        Example:
            >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            >>> QuickExcel.write(df, 'salida.xlsx')
            >>>
            >>> # Con nombre de hoja personalizado
            >>> QuickExcel.write(df, 'salida.xlsx', sheet_name='Datos')
        """
        # Validar que el DataFrame no esté vacío
        if df is None or df.empty:
            raise EmptyDataError("No se pueden escribir datos vacíos al archivo Excel")

        path = QuickExcel._validate_file_path(file_path)
        logger.info(f"Escribiendo DataFrame a {path} (hoja: {sheet_name})")

        # Crear directorio si no existe
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            df.to_excel(path, sheet_name=sheet_name, index=index, **kwargs)
            logger.info(f"Archivo creado exitosamente: {path}")
        except Exception as e:
            logger.error(f"Error escribiendo Excel {path}: {e}")
            raise

    @staticmethod
    def write_multiple_sheets(
        data: Dict[str, pd.DataFrame],
        file_path: Union[str, Path],
        index: bool = False
    ):
        """Escribe múltiples DataFrames en diferentes hojas de un mismo archivo.

        Args:
            data: Diccionario {nombre_hoja: DataFrame}
            file_path: Ruta del archivo de salida
            index: Incluir el índice del DataFrame (default: False)

        Raises:
            EmptyDataError: Si el diccionario está vacío
            InvalidFileFormatError: Si la extensión no es válida

        Example:
            >>> data = {
            ...     'Ventas': df_ventas,
            ...     'Clientes': df_clientes,
            ...     'Productos': df_productos
            ... }
            >>> QuickExcel.write_multiple_sheets(data, 'reporte.xlsx')
        """
        if not data:
            raise EmptyDataError("No se pueden escribir datos vacíos (diccionario vacío)")

        path = QuickExcel._validate_file_path(file_path)
        logger.info(f"Escribiendo {len(data)} hojas a {path}")

        # Crear directorio si no existe
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with pd.ExcelWriter(path, engine='openpyxl') as writer:
                for sheet_name, df in data.items():
                    if df is None or df.empty:
                        logger.warning(f"Hoja '{sheet_name}' está vacía, se omitirá")
                        continue
                    df.to_excel(writer, sheet_name=sheet_name, index=index)

            logger.info(f"Archivo multi-hoja creado exitosamente: {path}")
        except Exception as e:
            logger.error(f"Error escribiendo múltiples hojas a {path}: {e}")
            raise

    @staticmethod
    def create_formatted(
        df: pd.DataFrame,
        file_path: Union[str, Path],
        sheet_name: str = 'Sheet1',
        auto_filter: bool = True,
        freeze_panes: bool = True,
        header_bg_color: str = '#4472C4'
    ):
        """Crea un Excel con formato profesional básico.

        Aplica formato a encabezados, ajusta ancho de columnas,
        agrega autofiltro y congela paneles.

        Args:
            df: DataFrame a escribir
            file_path: Ruta del archivo de salida
            sheet_name: Nombre de la hoja (default: 'Sheet1')
            auto_filter: Activar autofiltro en encabezados (default: True)
            freeze_panes: Congelar primera fila (default: True)
            header_bg_color: Color de fondo para encabezados (default: azul)

        Raises:
            EmptyDataError: Si el DataFrame está vacío
            InvalidFileFormatError: Si la extensión no es válida

        Example:
            >>> df = pd.DataFrame({'Nombre': ['Juan', 'María'], 'Edad': [30, 25]})
            >>> QuickExcel.create_formatted(df, 'reporte_bonito.xlsx')
        """
        if df is None or df.empty:
            raise EmptyDataError("No se pueden escribir datos vacíos al archivo Excel")

        path = QuickExcel._validate_file_path(file_path)
        logger.info(f"Creando Excel formateado: {path}")

        # Crear directorio si no existe
        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            # Crear archivo con xlsxwriter
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Obtener objetos del workbook
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Formato para encabezados
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': header_bg_color,
                'font_color': 'white',
                'border': 1
            })

            # Aplicar formato a encabezados
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                # Ajustar ancho de columna
                column_len = max(df[value].astype(str).map(len).max(), len(value)) + 2
                worksheet.set_column(col_num, col_num, column_len)

            # Aplicar autofiltro
            if auto_filter:
                worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

            # Congelar paneles
            if freeze_panes:
                worksheet.freeze_panes(1, 0)

            writer.close()
            logger.info(f"Excel formateado creado exitosamente: {path}")

        except Exception as e:
            logger.error(f"Error creando Excel formateado {path}: {e}")
            raise
