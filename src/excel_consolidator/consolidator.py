"""Consolidador principal de archivos Excel.

Este módulo proporciona la clase ExcelConsolidator para consolidar
archivos Excel extraídos en archivos limpios con datos normalizados.
"""

import time
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd

from logger import setup_logger

from .detector import detect_structure
from .extractor import extract_data
from .utils import create_output_filename, ensure_output_directory

# Logger Nivel 2 - Coordinador: INFO con consola y archivo, orquesta consolidación
logger = setup_logger(
    __name__,
    level="INFO",
    console_output=True,
    file_output=True
)


class ExcelConsolidator:
    """Consolidador de archivos Excel.

    Procesa archivos Excel con estructuras simples o complejas,
    extrae los datos y los consolida en archivos limpios.

    Example:
        >>> consolidator = ExcelConsolidator()
        >>> result = consolidator.consolidate_file('datos.xlsx')
        >>> print(f"Consolidado: {result['output_file']}")

        >>> # Con context manager
        >>> with ExcelConsolidator(output_dir='consolidado/') as cons:
        ...     cons.consolidate_directory('extraido/')
    """

    def __init__(
        self,
        output_dir: Optional[Union[str, Path]] = None,
        output_subdir: str = "consolidado",
        suffix: str = "_consolidado",
    ):
        """Inicializa el consolidador.

        Args:
            output_dir: Directorio base de salida (None = mismo que entrada)
            output_subdir: Subdirectorio dentro de output_dir (default: "consolidado")
            suffix: Sufijo para archivos consolidados (default: "_consolidado")

        Example:
            >>> cons = ExcelConsolidator(output_dir='resultados/')
        """
        self.output_dir = Path(output_dir) if output_dir else None
        self.output_subdir = output_subdir
        self.suffix = suffix
        self.results = []

        logger.info("ExcelConsolidator inicializado")

    def consolidate_file(
        self,
        file_path: Union[str, Path],
        sheet_name: Optional[str] = None,
        output_path: Optional[Union[str, Path]] = None,
    ) -> Dict:
        """Consolida un archivo Excel.

        Args:
            file_path: Ruta al archivo Excel a consolidar
            sheet_name: Nombre de la hoja (None = primera hoja)
            output_path: Ruta de salida personalizada (opcional)

        Returns:
            Diccionario con resultado del proceso:
            {
                'success': bool,
                'input_file': Path,
                'output_file': Path,
                'rows_extracted': int,
                'columns': list,
                'structure_type': str,
                'processing_time': float,
                'error': str (si hubo error)
            }

        Example:
            >>> result = consolidator.consolidate_file('datos.xlsx')
            >>> if result['success']:
            ...     print(f"Éxito: {result['rows_extracted']} filas")
        """
        file_path = Path(file_path)
        start_time = time.time()

        logger.info(f"{'='*60}")
        logger.info(f"Consolidando: {file_path.name}")
        logger.info(f"{'='*60}")

        result = {
            "success": False,
            "input_file": file_path,
            "output_file": None,
            "rows_extracted": 0,
            "columns": [],
            "structure_type": "unknown",
            "processing_time": 0.0,
            "error": None,
        }

        try:
            # 1. Validar que el archivo existe
            if not file_path.exists():
                raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

            # 2. Detectar estructura
            logger.info("📊 Detectando estructura...")
            structure_info = detect_structure(file_path, sheet_name)
            result["structure_type"] = structure_info["type"]

            # 3. Extraer datos
            logger.info("📤 Extrayendo datos...")
            df = extract_data(file_path, sheet_name, structure_info)

            if df.empty:
                logger.warning("⚠️  No se extrajeron datos del archivo")
                result["error"] = "No se extrajeron datos"
                return result

            result["rows_extracted"] = len(df)
            result["columns"] = df.columns.tolist()

            # 4. Determinar ruta de salida
            if output_path:
                output_file = Path(output_path)
            else:
                output_file = self._get_output_path(file_path)

            # Asegurar que el directorio de salida existe
            output_file.parent.mkdir(parents=True, exist_ok=True)

            # 5. Guardar archivo consolidado
            logger.info(f"💾 Guardando archivo consolidado...")
            df.to_excel(output_file, index=False, engine="openpyxl")

            result["output_file"] = output_file
            result["success"] = True

            # Tiempo de procesamiento
            result["processing_time"] = time.time() - start_time

            logger.info(f"✅ Consolidación exitosa!")
            logger.info(f"   📊 Filas extraídas: {result['rows_extracted']}")
            logger.info(f"   📋 Columnas: {len(result['columns'])}")
            logger.info(f"   📁 Guardado en: {output_file}")
            logger.info(f"   ⏱️  Tiempo: {result['processing_time']:.2f}s")

        except Exception as e:
            logger.error(f"❌ Error consolidando {file_path.name}: {e}")
            result["error"] = str(e)
            result["processing_time"] = time.time() - start_time

        finally:
            self.results.append(result)

        return result

    def consolidate_directory(
        self,
        directory: Union[str, Path],
        pattern: str = "*.xlsx",
        recursive: bool = False,
        exclude_patterns: Optional[List[str]] = None,
    ) -> Dict:
        """Consolida todos los archivos Excel de un directorio.

        Args:
            directory: Directorio con archivos Excel
            pattern: Patrón de archivos (default: "*.xlsx")
            recursive: Buscar recursivamente (default: False)
            exclude_patterns: Patrones a excluir (ej: ["~$", ".tmp"])

        Returns:
            Diccionario con resumen del procesamiento:
            {
                'total_files': int,
                'successful': int,
                'failed': int,
                'results': [list of results],
                'total_time': float
            }

        Example:
            >>> summary = consolidator.consolidate_directory('extraido/')
            >>> print(f"Procesados: {summary['successful']}/{summary['total_files']}")
        """
        directory = Path(directory)
        start_time = time.time()

        logger.info(f"\n{'='*60}")
        logger.info(f"CONSOLIDANDO DIRECTORIO: {directory}")
        logger.info(f"{'='*60}\n")

        # Validar directorio
        if not directory.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory}")

        # Buscar archivos
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))

        # Filtrar archivos excluidos
        if exclude_patterns:
            files = [
                f
                for f in files
                if not any(pattern in str(f) for pattern in exclude_patterns)
            ]

        logger.info(f"📁 Archivos encontrados: {len(files)}")

        if not files:
            logger.warning("⚠️  No se encontraron archivos para procesar")
            return {
                "total_files": 0,
                "successful": 0,
                "failed": 0,
                "results": [],
                "total_time": 0.0,
            }

        # Procesar cada archivo
        for i, file_path in enumerate(files, start=1):
            logger.info(f"\n[{i}/{len(files)}] Procesando: {file_path.name}")
            self.consolidate_file(file_path)

        # Generar resumen
        total_time = time.time() - start_time
        successful = sum(1 for r in self.results if r["success"])
        failed = len(self.results) - successful

        summary = {
            "total_files": len(files),
            "successful": successful,
            "failed": failed,
            "results": self.results,
            "total_time": total_time,
            "success_rate": (successful / len(files) * 100) if files else 0,
        }

        # Log resumen
        logger.info(f"\n{'='*60}")
        logger.info("📊 RESUMEN DE CONSOLIDACIÓN")
        logger.info(f"{'='*60}")
        logger.info(f"Total archivos: {summary['total_files']}")
        logger.info(f"✅ Exitosos: {summary['successful']}")
        logger.info(f"❌ Fallidos: {summary['failed']}")
        logger.info(f"📈 Tasa de éxito: {summary['success_rate']:.1f}%")
        logger.info(f"⏱️  Tiempo total: {summary['total_time']:.2f}s")

        return summary

    def _get_output_path(self, input_path: Path) -> Path:
        """Determina la ruta de salida para un archivo.

        Args:
            input_path: Ruta del archivo de entrada

        Returns:
            Path del archivo de salida

        Example:
            >>> cons = ExcelConsolidator()
            >>> output = cons._get_output_path(Path('extraido/datos.xlsx'))
            >>> # Retorna: extraido/consolidado/datos_consolidado.xlsx
        """
        if self.output_dir:
            # Usar directorio de salida personalizado
            base_dir = self.output_dir
        else:
            # Usar el directorio padre del archivo de entrada
            base_dir = input_path.parent

        # Crear subdirectorio "consolidado"
        output_dir = ensure_output_directory(base_dir, self.output_subdir)

        # Crear nombre de archivo
        output_filename = create_output_filename(input_path, self.suffix)

        return output_dir / output_filename

    def get_summary(self) -> Dict:
        """Obtiene un resumen de todos los procesamientos realizados.

        Returns:
            Diccionario con estadísticas y resultados

        Example:
            >>> consolidator.consolidate_file('file1.xlsx')
            >>> consolidator.consolidate_file('file2.xlsx')
            >>> summary = consolidator.get_summary()
            >>> print(summary['total_processed'])
        """
        if not self.results:
            return {"total_processed": 0, "successful": 0, "failed": 0, "results": []}

        successful = sum(1 for r in self.results if r["success"])

        return {
            "total_processed": len(self.results),
            "successful": successful,
            "failed": len(self.results) - successful,
            "total_rows": sum(r["rows_extracted"] for r in self.results),
            "results": self.results,
        }

    def clear_results(self):
        """Limpia los resultados almacenados.

        Example:
            >>> consolidator.clear_results()
        """
        self.results = []
        logger.debug("Resultados limpiados")

    # Context manager support
    def __enter__(self):
        """Permite usar with statement."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Limpia recursos al salir del contexto."""
        return False

    def __repr__(self) -> str:
        """Representación string del objeto."""
        return (
            f"ExcelConsolidator("
            f"output_dir={self.output_dir}, "
            f"processed={len(self.results)})"
        )
