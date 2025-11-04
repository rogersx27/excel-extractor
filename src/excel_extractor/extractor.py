"""Módulo para extraer hojas individuales de archivos Excel.

Este módulo proporciona funcionalidad para tomar un archivo Excel con
múltiples hojas y extraer cada hoja en un archivo Excel separado.
"""
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd

from logger import setup_logger

# Configurar logger para este módulo
logger = setup_logger(__name__, level="INFO")


class ExcelSheetExtractor:
    """Extractor de hojas de Excel a archivos individuales."""

    def __init__(self, excel_file: Path, output_base_dir: Optional[Path] = None):
        """
        Inicializa el extractor.

        Args:
            excel_file: Ruta al archivo Excel a procesar
            output_base_dir: Directorio base donde crear carpeta de salida
                           (default: data/)

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el archivo no es un Excel válido
        """
        self.excel_file = Path(excel_file)
        self.output_base_dir = output_base_dir

        # Validaciones
        self._validate_file()

        # Configurar directorio de salida
        self._setup_output_dir()

        # Estado
        self.sheets_data: Optional[Dict[str, pd.DataFrame]] = None
        self.files_created: List[str] = []

    def _validate_file(self):
        """Valida que el archivo existe y es un Excel válido."""
        if not self.excel_file.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.excel_file}")

        valid_extensions = ['.xlsx', '.xls', '.xlsm', '.xlsb']
        if self.excel_file.suffix.lower() not in valid_extensions:
            raise ValueError(
                f"Archivo no es un Excel válido: {self.excel_file.suffix}. "
                f"Extensiones válidas: {', '.join(valid_extensions)}"
            )

    def _setup_output_dir(self):
        """Configura el directorio de salida."""
        if self.output_base_dir is None:
            from config import DATA_DIR
            self.output_base_dir = DATA_DIR

        # Crear carpeta con nombre del archivo (sin extensión)
        folder_name = self.excel_file.stem
        self.output_dir = self.output_base_dir / folder_name

    def load_sheets(self) -> Dict[str, pd.DataFrame]:
        """
        Carga todas las hojas del Excel en memoria.

        Returns:
            dict: Diccionario {nombre_hoja: DataFrame}
        """
        logger.info(f"📂 Procesando archivo: {self.excel_file.name}")
        logger.info("📖 Leyendo hojas del archivo Excel...")

        try:
            self.sheets_data = pd.read_excel(
                self.excel_file,
                sheet_name=None,
                engine='openpyxl'
            )

            total_sheets = len(self.sheets_data)
            logger.info(f"📊 Total de hojas encontradas: {total_sheets}")

            return self.sheets_data

        except Exception as e:
            logger.error(f"Error al leer el archivo Excel: {e}", exc_info=True)
            raise

    def extract_all_sheets(
        self,
        with_index: bool = True,
        clean_names: bool = True
    ) -> Dict:
        """
        Extrae todas las hojas en archivos Excel separados.

        Args:
            with_index: Si True, añade índice numérico (01_, 02_, etc.)
            clean_names: Si True, limpia caracteres inválidos de nombres

        Returns:
            dict: Información del proceso
                {
                    'total_sheets': int,
                    'output_dir': Path,
                    'files_created': list[str]
                }
        """
        # Cargar hojas si no están cargadas
        if self.sheets_data is None:
            self.load_sheets()

        # Crear directorio de salida
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Carpeta de salida: {self.output_dir}")

        total_sheets = len(self.sheets_data)
        self.files_created = []

        # Procesar cada hoja
        for index, (sheet_name, df) in enumerate(self.sheets_data.items(), start=1):
            # Generar nombre de archivo
            file_name = self._generate_filename(
                sheet_name,
                index if with_index else None,
                clean_names
            )

            output_file = self.output_dir / file_name

            # Log de progreso
            logger.info(f"  [{index}/{total_sheets}] Extrayendo: {sheet_name} -> {file_name}")

            # Información sobre la hoja
            if df.empty:
                logger.warning(f"    ⚠️  La hoja '{sheet_name}' está vacía")
            else:
                rows, cols = df.shape
                logger.info(f"    ✓ Datos: {rows} filas x {cols} columnas")

            # Guardar hoja
            self._save_sheet(df, output_file, sheet_name)
            self.files_created.append(file_name)

        # Resumen
        self._log_summary(total_sheets)

        return {
            'total_sheets': total_sheets,
            'output_dir': self.output_dir,
            'files_created': self.files_created
        }

    def extract_specific_sheets(
        self,
        sheet_names: List[str],
        with_index: bool = True,
        clean_names: bool = True
    ) -> Dict:
        """
        Extrae solo hojas específicas.

        Args:
            sheet_names: Lista de nombres de hojas a extraer
            with_index: Si True, añade índice numérico
            clean_names: Si True, limpia caracteres inválidos

        Returns:
            dict: Información del proceso
        """
        # Cargar hojas si no están cargadas
        if self.sheets_data is None:
            self.load_sheets()

        # Validar que las hojas existen
        available_sheets = set(self.sheets_data.keys())
        requested_sheets = set(sheet_names)
        missing_sheets = requested_sheets - available_sheets

        if missing_sheets:
            raise ValueError(
                f"Hojas no encontradas: {', '.join(missing_sheets)}. "
                f"Hojas disponibles: {', '.join(available_sheets)}"
            )

        # Crear directorio de salida
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"📁 Carpeta de salida: {self.output_dir}")

        self.files_created = []
        total = len(sheet_names)

        # Procesar solo las hojas solicitadas
        for index, sheet_name in enumerate(sheet_names, start=1):
            df = self.sheets_data[sheet_name]

            file_name = self._generate_filename(
                sheet_name,
                index if with_index else None,
                clean_names
            )

            output_file = self.output_dir / file_name

            logger.info(f"  [{index}/{total}] Extrayendo: {sheet_name} -> {file_name}")

            if not df.empty:
                rows, cols = df.shape
                logger.info(f"    ✓ Datos: {rows} filas x {cols} columnas")

            self._save_sheet(df, output_file, sheet_name)
            self.files_created.append(file_name)

        self._log_summary(total)

        return {
            'total_sheets': total,
            'output_dir': self.output_dir,
            'files_created': self.files_created
        }

    def get_sheet_names(self) -> List[str]:
        """
        Obtiene los nombres de todas las hojas del Excel.

        Returns:
            list: Lista de nombres de hojas
        """
        if self.sheets_data is None:
            self.load_sheets()

        return list(self.sheets_data.keys())

    def _generate_filename(
        self,
        sheet_name: str,
        index: Optional[int] = None,
        clean: bool = True
    ) -> str:
        """
        Genera nombre de archivo para una hoja.

        Args:
            sheet_name: Nombre de la hoja
            index: Índice opcional (ej: 1 -> "01_")
            clean: Si True, limpia caracteres inválidos

        Returns:
            str: Nombre de archivo generado
        """
        from .utils import clean_filename

        # Agregar índice si se especifica
        if index is not None:
            file_name = f"{index:02d}_{sheet_name}.xlsx"
        else:
            file_name = f"{sheet_name}.xlsx"

        # Limpiar nombre si se requiere
        if clean:
            file_name = clean_filename(file_name)

        return file_name

    def _save_sheet(self, df: pd.DataFrame, output_file: Path, sheet_name: str):
        """
        Guarda un DataFrame en archivo Excel.

        Args:
            df: DataFrame a guardar
            output_file: Ruta del archivo de salida
            sheet_name: Nombre de la hoja en el Excel
        """
        try:
            df.to_excel(output_file, index=False, sheet_name=sheet_name)
        except Exception as e:
            logger.error(f"Error al guardar {output_file}: {e}", exc_info=True)
            raise

    def _log_summary(self, total_sheets: int):
        """
        Muestra resumen del proceso.

        Args:
            total_sheets: Total de hojas procesadas
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ Proceso completado exitosamente")
        logger.info(f"{'='*60}")
        logger.info(f"📊 Total de hojas procesadas: {total_sheets}")
        logger.info(f"📁 Archivos creados en: {self.output_dir}")
        logger.info(f"📝 Archivos generados:")
        for file in self.files_created:
            logger.info(f"   - {file}")


def extract_excel_sheets(
    excel_file: Path,
    output_base_dir: Optional[Path] = None,
    sheet_names: Optional[List[str]] = None,
    with_index: bool = True,
    clean_names: bool = True
) -> Dict:
    """
    Función helper para extraer hojas de Excel (interfaz simplificada).

    Args:
        excel_file: Ruta al archivo Excel
        output_base_dir: Directorio base de salida
        sheet_names: Lista de hojas específicas (None = todas)
        with_index: Añadir índice numérico a nombres
        clean_names: Limpiar caracteres inválidos

    Returns:
        dict: Información del proceso

    Example:
        >>> from excel_extractor import extract_excel_sheets
        >>> from pathlib import Path
        >>>
        >>> result = extract_excel_sheets(Path("datos.xlsx"))
        >>> print(f"Procesadas {result['total_sheets']} hojas")
    """
    extractor = ExcelSheetExtractor(excel_file, output_base_dir)

    if sheet_names:
        return extractor.extract_specific_sheets(
            sheet_names,
            with_index=with_index,
            clean_names=clean_names
        )
    else:
        return extractor.extract_all_sheets(
            with_index=with_index,
            clean_names=clean_names
        )
