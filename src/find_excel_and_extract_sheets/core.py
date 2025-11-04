"""Módulo core simplificado para búsqueda y extracción de hojas Excel.

Este módulo combina la funcionalidad de búsqueda y procesamiento de archivos
Excel de forma simple y eficiente.
"""
import concurrent.futures
import time
from pathlib import Path
from typing import Dict, List, Optional, Union

from excel_extractor import extract_excel_sheets
from logger import setup_logger

# Configurar logger
logger = setup_logger(__name__)


class ExcelProcessor:
    """Procesador simplificado de archivos Excel."""

    # Extensiones de Excel soportadas
    EXCEL_EXTENSIONS = {".xlsx", ".xls", ".xlsm", ".xlsb"}

    def __init__(
        self,
        output_base_dir: Optional[Path] = None,
        min_size_mb: float = 0.001,
        max_size_mb: float = 100.0,
        exclude_patterns: Optional[List[str]] = None,
        max_workers: int = 4,
    ):
        """
        Inicializa el procesador de Excel.

        Args:
            output_base_dir: Directorio base para extracciones
            min_size_mb: Tamaño mínimo de archivo (MB)
            max_size_mb: Tamaño máximo de archivo (MB)
            exclude_patterns: Patrones a excluir en nombres/rutas
            max_workers: Workers para procesamiento paralelo
        """
        if output_base_dir is None:
            from config import DATA_DIR
            self.output_base_dir = DATA_DIR / "extracted_sheets"
        else:
            self.output_base_dir = Path(output_base_dir)

        self.min_size_bytes = int(min_size_mb * 1024 * 1024)
        self.max_size_bytes = int(max_size_mb * 1024 * 1024)
        self.exclude_patterns = exclude_patterns or []
        self.max_workers = max_workers

    def find_excel_files(
        self, search_path: Union[str, Path], recursive: bool = True
    ) -> List[Dict]:
        """
        Busca archivos Excel en un directorio.

        Args:
            search_path: Directorio donde buscar
            recursive: Buscar recursivamente en subdirectorios

        Returns:
            List[Dict]: Lista de archivos encontrados con metadata
        """
        search_path = Path(search_path)

        if not search_path.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {search_path}")

        logger.info(f"🔍 Buscando archivos Excel en: {search_path}")

        pattern = "**/*" if recursive else "*"
        excel_files = []

        for file_path in search_path.glob(pattern):
            if self._is_valid_excel(file_path):
                size_bytes = file_path.stat().st_size
                excel_files.append({
                    "path": file_path,
                    "size_bytes": size_bytes,
                    "size_mb": size_bytes / (1024 * 1024),
                })

        logger.info(f"✅ Archivos Excel encontrados: {len(excel_files)}")
        return excel_files

    def process_files(
        self,
        excel_files: List[Dict],
        parallel: bool = True,
        **extract_kwargs
    ) -> Dict:
        """
        Procesa una lista de archivos Excel.

        Args:
            excel_files: Lista de archivos a procesar
            parallel: Si True, procesa en paralelo; si False, secuencial
            **extract_kwargs: Argumentos para extract_excel_sheets

        Returns:
            Dict: Resultado del procesamiento con estadísticas
        """
        start_time = time.time()
        mode = "paralelo" if parallel else "secuencial"

        logger.info(f"🚀 Procesando {len(excel_files)} archivos (modo: {mode})")

        if parallel:
            results = self._process_parallel(excel_files, **extract_kwargs)
        else:
            results = self._process_sequential(excel_files, **extract_kwargs)

        total_time = time.time() - start_time
        successful = sum(1 for r in results if r["success"])
        failed = len(results) - successful

        batch_result = {
            "total_files": len(excel_files),
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / len(excel_files) * 100) if excel_files else 0,
            "total_time": total_time,
            "results": results,
        }

        self._log_summary(batch_result)
        return batch_result

    def _process_sequential(
        self, excel_files: List[Dict], **extract_kwargs
    ) -> List[Dict]:
        """Procesamiento secuencial."""
        results = []

        for i, excel_file in enumerate(excel_files, 1):
            logger.info(
                f"📄 [{i}/{len(excel_files)}] Procesando: {excel_file['path'].name}"
            )
            result = self._process_single_file(excel_file, **extract_kwargs)
            results.append(result)

        return results

    def _process_parallel(
        self, excel_files: List[Dict], **extract_kwargs
    ) -> List[Dict]:
        """Procesamiento paralelo."""
        results = []

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            future_to_file = {
                executor.submit(
                    self._process_single_file, excel_file, **extract_kwargs
                ): excel_file
                for excel_file in excel_files
            }

            for i, future in enumerate(
                concurrent.futures.as_completed(future_to_file), 1
            ):
                excel_file = future_to_file[future]
                try:
                    result = future.result()
                    status = "✅" if result["success"] else "❌"
                    logger.info(
                        f"{status} [{i}/{len(excel_files)}] {excel_file['path'].name}"
                    )
                except Exception as e:
                    logger.error(f"❌ Error: {excel_file['path'].name} - {e}")
                    result = {
                        "excel_file": excel_file,
                        "success": False,
                        "error": str(e),
                    }

                results.append(result)

        return results

    def _process_single_file(
        self, excel_file: Dict, **extract_kwargs
    ) -> Dict:
        """
        Procesa un único archivo Excel.

        Args:
            excel_file: Dict con información del archivo
            **extract_kwargs: Argumentos para extract_excel_sheets

        Returns:
            Dict: Resultado del procesamiento
        """
        start_time = time.time()

        try:
            extraction_result = extract_excel_sheets(
                excel_file["path"],
                output_base_dir=self.output_base_dir,
                **extract_kwargs
            )

            return {
                "excel_file": excel_file,
                "success": True,
                "output_dir": extraction_result["output_dir"],
                "files_created": extraction_result["files_created"],
                "processing_time": time.time() - start_time,
            }

        except Exception as e:
            logger.error(f"Error procesando {excel_file['path'].name}: {e}")
            return {
                "excel_file": excel_file,
                "success": False,
                "error": str(e),
                "processing_time": time.time() - start_time,
            }

    def _is_valid_excel(self, file_path: Path) -> bool:
        """
        Valida si un archivo es un Excel procesable.

        Args:
            file_path: Ruta del archivo

        Returns:
            bool: True si es válido
        """
        # Verificar que es archivo
        if not file_path.is_file():
            return False

        # Verificar extensión
        if file_path.suffix.lower() not in self.EXCEL_EXTENSIONS:
            return False

        # Verificar tamaño
        try:
            size = file_path.stat().st_size
            if size < self.min_size_bytes or size > self.max_size_bytes:
                return False
        except OSError:
            return False

        # Verificar patrones de exclusión
        file_str = str(file_path).lower()
        for pattern in self.exclude_patterns:
            if pattern.lower() in file_str:
                logger.debug(f"⏭️  Excluido: {file_path.name} (patrón: {pattern})")
                return False

        return True

    def _log_summary(self, result: Dict):
        """Registra resumen del procesamiento."""
        logger.info(f"\n{'='*80}")
        logger.info("📊 RESUMEN DEL PROCESAMIENTO")
        logger.info(f"{'='*80}")
        logger.info(f"📁 Total de archivos: {result['total_files']}")
        logger.info(f"✅ Exitosos: {result['successful']}")
        logger.info(f"❌ Fallidos: {result['failed']}")
        logger.info(f"📈 Tasa de éxito: {result['success_rate']:.1f}%")
        logger.info(f"⏱️  Tiempo total: {result['total_time']:.2f} segundos")

        if result["failed"] > 0:
            logger.info(f"\n❌ Archivos con errores:")
            for r in result["results"]:
                if not r["success"]:
                    logger.info(f"   - {r['excel_file']['path'].name}: {r.get('error', 'Error desconocido')}")


def find_and_extract_excel_sheets(
    search_directory: Union[str, Path],
    output_directory: Optional[Union[str, Path]] = None,
    recursive: bool = True,
    parallel: bool = True,
    max_workers: int = 4,
    min_size_mb: float = 0.001,
    max_size_mb: float = 100.0,
    exclude_patterns: Optional[List[str]] = None,
    **extract_kwargs,
) -> Dict:
    """
    Busca y extrae hojas de archivos Excel de forma automática.

    Args:
        search_directory: Directorio donde buscar
        output_directory: Directorio donde guardar extracciones
        recursive: Buscar recursivamente
        parallel: Procesamiento paralelo (True) o secuencial (False)
        max_workers: Workers para procesamiento paralelo
        min_size_mb: Tamaño mínimo de archivo
        max_size_mb: Tamaño máximo de archivo
        exclude_patterns: Patrones a excluir
        **extract_kwargs: Argumentos para extract_excel_sheets (with_index, clean_names, etc.)

    Returns:
        Dict: Resultado con estadísticas del procesamiento

    Example:
        >>> result = find_and_extract_excel_sheets(
        ...     "COMPUTADOR 1",
        ...     parallel=True,
        ...     max_workers=4,
        ...     with_index=True
        ... )
        >>> print(f"Procesados: {result['successful']}/{result['total_files']}")
    """
    # Crear procesador
    processor = ExcelProcessor(
        output_base_dir=Path(output_directory) if output_directory else None,
        min_size_mb=min_size_mb,
        max_size_mb=max_size_mb,
        exclude_patterns=exclude_patterns,
        max_workers=max_workers,
    )

    # Buscar archivos
    excel_files = processor.find_excel_files(search_directory, recursive)

    if not excel_files:
        logger.warning("⚠️  No se encontraron archivos Excel")
        return {
            "total_files": 0,
            "successful": 0,
            "failed": 0,
            "success_rate": 0.0,
            "total_time": 0.0,
            "results": [],
        }

    # Procesar archivos
    return processor.process_files(excel_files, parallel, **extract_kwargs)


def scan_directory(
    search_directory: Union[str, Path], recursive: bool = True
) -> Dict:
    """
    Escanea un directorio y retorna información sobre archivos Excel.

    Args:
        search_directory: Directorio a escanear
        recursive: Buscar recursivamente

    Returns:
        Dict: Información sobre archivos encontrados

    Example:
        >>> info = scan_directory("COMPUTADOR 1")
        >>> print(f"Encontrados: {info['total_files']} archivos")
        >>> print(f"Tamaño total: {info['total_size_mb']:.2f} MB")
    """
    processor = ExcelProcessor()
    excel_files = processor.find_excel_files(search_directory, recursive)

    if not excel_files:
        return {
            "total_files": 0,
            "total_size_mb": 0.0,
            "files": [],
        }

    total_size = sum(f["size_bytes"] for f in excel_files)

    return {
        "total_files": len(excel_files),
        "total_size_mb": total_size / (1024 * 1024),
        "files": [
            {
                "name": f["path"].name,
                "path": str(f["path"]),
                "size_mb": f["size_mb"],
            }
            for f in excel_files
        ],
    }
