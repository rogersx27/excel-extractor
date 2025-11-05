"""Procesamiento batch de múltiples archivos Excel para consolidación.

Este módulo proporciona la clase BatchConsolidator para procesar
directorios completos de archivos Excel extraídos, consolidando
cada uno automáticamente mientras preserva la estructura de carpetas.
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Union

from logger import setup_logger

from .consolidator import ExcelConsolidator

# Logger Nivel 2 - Coordinador: INFO con consola y archivo, orquesta batch processing
logger = setup_logger(
    __name__,
    level="INFO",
    console_output=True,
    file_output=True
)


class BatchConsolidator:
    """Consolidador batch para procesar directorios completos.

    Escanea recursivamente directorios con archivos Excel extraídos
    y los consolida automáticamente, excluyendo carpetas ya consolidadas
    y archivos temporales.

    Example:
        >>> batch = BatchConsolidator()
        >>> result = batch.consolidate_extracted_directory('data/extraido/')
        >>> print(f"Consolidados: {result['successful']}/{result['total_files']}")

        >>> # Con procesamiento paralelo
        >>> batch = BatchConsolidator(parallel=True, max_workers=4)
        >>> result = batch.consolidate_extracted_directory('data/')
    """

    # Patrones por defecto a excluir
    DEFAULT_EXCLUDE_PATTERNS = [
        "~$",           # Archivos temporales de Excel
        ".tmp",         # Archivos temporales
        "temp",         # Carpetas temporales
        "consolidado",  # Carpetas de consolidados (evitar duplicación)
        "backup",       # Carpetas de backup
        ".git",         # Control de versiones
    ]

    def __init__(
        self,
        output_subdir: str = "consolidado",
        suffix: str = "_consolidado",
        parallel: bool = False,
        max_workers: int = 4,
        exclude_patterns: Optional[List[str]] = None
    ):
        """Inicializa el consolidador batch.

        Args:
            output_subdir: Nombre del subdirectorio para consolidados (default: "consolidado")
            suffix: Sufijo para archivos consolidados (default: "_consolidado")
            parallel: Usar procesamiento paralelo (default: False)
            max_workers: Número de workers para paralelo (default: 4)
            exclude_patterns: Patrones adicionales a excluir (se suman a los defaults)

        Example:
            >>> batch = BatchConsolidator(parallel=True, max_workers=8)
        """
        self.output_subdir = output_subdir
        self.suffix = suffix
        self.parallel = parallel
        self.max_workers = max_workers

        # Combinar patrones de exclusión
        self.exclude_patterns = self.DEFAULT_EXCLUDE_PATTERNS.copy()
        if exclude_patterns:
            self.exclude_patterns.extend(exclude_patterns)

        self.results = []

        logger.info("BatchConsolidator inicializado")
        logger.info(f"  Paralelo: {parallel}")
        if parallel:
            logger.info(f"  Workers: {max_workers}")

    def find_excel_files(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        pattern: str = "*.xlsx"
    ) -> List[Path]:
        """Encuentra todos los archivos Excel en un directorio.

        Args:
            directory: Directorio a escanear
            recursive: Buscar recursivamente (default: True)
            pattern: Patrón de archivos (default: "*.xlsx")

        Returns:
            Lista de rutas a archivos Excel encontrados

        Example:
            >>> batch = BatchConsolidator()
            >>> files = batch.find_excel_files('data/extraido/')
            >>> print(f"Encontrados: {len(files)} archivos")
        """
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory}")

        logger.info(f"🔍 Buscando archivos Excel en: {directory}")
        logger.info(f"   Recursivo: {recursive}")
        logger.info(f"   Patrón: {pattern}")

        # Buscar archivos
        if recursive:
            files = list(directory.rglob(pattern))
        else:
            files = list(directory.glob(pattern))

        # Filtrar archivos excluidos
        filtered_files = []
        for file_path in files:
            # Verificar si algún patrón de exclusión coincide
            should_exclude = any(
                pattern in str(file_path)
                for pattern in self.exclude_patterns
            )

            if not should_exclude:
                filtered_files.append(file_path)
            else:
                logger.debug(f"Excluido: {file_path.name}")

        logger.info(f"✅ Encontrados: {len(filtered_files)} archivos")
        logger.info(f"🚫 Excluidos: {len(files) - len(filtered_files)} archivos")

        return filtered_files

    def consolidate_extracted_directory(
        self,
        directory: Union[str, Path],
        recursive: bool = True,
        pattern: str = "*.xlsx",
        dry_run: bool = False
    ) -> Dict:
        """Consolida todos los archivos Excel de un directorio extraído.

        Args:
            directory: Directorio con archivos extraídos
            recursive: Buscar recursivamente (default: True)
            pattern: Patrón de archivos (default: "*.xlsx")
            dry_run: Solo simular (no crear archivos) (default: False)

        Returns:
            Diccionario con resumen del procesamiento:
            {
                'total_files': int,
                'successful': int,
                'failed': int,
                'skipped': int,
                'results': [list of results],
                'total_time': float,
                'success_rate': float,
                'directories_processed': int
            }

        Example:
            >>> batch = BatchConsolidator()
            >>> result = batch.consolidate_extracted_directory('data/extraido/')
        """
        directory = Path(directory)
        start_time = time.time()

        logger.info(f"\n{'='*60}")
        logger.info(f"🚀 CONSOLIDACIÓN BATCH")
        logger.info(f"{'='*60}")
        logger.info(f"📁 Directorio: {directory}")
        logger.info(f"🔄 Recursivo: {recursive}")
        logger.info(f"🎯 Patrón: {pattern}")
        if dry_run:
            logger.info(f"🔍 MODO DRY-RUN (simulación)")
        logger.info(f"{'='*60}\n")

        # Buscar archivos
        files = self.find_excel_files(directory, recursive, pattern)

        if not files:
            logger.warning("⚠️  No se encontraron archivos para procesar")
            return {
                'total_files': 0,
                'successful': 0,
                'failed': 0,
                'skipped': 0,
                'results': [],
                'total_time': 0.0,
                'success_rate': 0.0,
                'directories_processed': 0
            }

        # Agrupar archivos por directorio para mejor reporte
        directories = set(f.parent for f in files)
        logger.info(f"📂 Directorios a procesar: {len(directories)}\n")

        # Procesar archivos
        if dry_run:
            # Modo simulación
            self.results = self._simulate_processing(files)
        elif self.parallel:
            # Procesamiento paralelo
            self._process_parallel(files)
        else:
            # Procesamiento secuencial
            self._process_sequential(files)

        # Generar resumen
        total_time = time.time() - start_time
        successful = sum(1 for r in self.results if r['success'])
        failed = sum(1 for r in self.results if not r['success'] and r.get('error'))
        skipped = len(files) - len(self.results)

        summary = {
            'total_files': len(files),
            'successful': successful,
            'failed': failed,
            'skipped': skipped,
            'results': self.results,
            'total_time': total_time,
            'success_rate': (successful / len(files) * 100) if files else 0,
            'directories_processed': len(directories)
        }

        # Log resumen
        self._log_summary(summary, dry_run)

        return summary

    def _process_sequential(self, files: List[Path]):
        """Procesa archivos secuencialmente.

        Args:
            files: Lista de archivos a procesar
        """
        total = len(files)

        for i, file_path in enumerate(files, start=1):
            logger.info(f"\n{'─'*60}")
            logger.info(f"[{i}/{total}] 📄 {file_path.name}")
            logger.info(f"{'─'*60}")

            # Crear consolidador
            consolidator = ExcelConsolidator(
                output_dir=None,  # Usar mismo directorio
                output_subdir=self.output_subdir,
                suffix=self.suffix
            )

            # Procesar archivo
            result = consolidator.consolidate_file(file_path)
            self.results.append(result)

    def _process_parallel(self, files: List[Path]):
        """Procesa archivos en paralelo.

        Args:
            files: Lista de archivos a procesar
        """
        total = len(files)
        logger.info(f"⚡ Procesamiento paralelo con {self.max_workers} workers\n")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Enviar todos los trabajos
            future_to_file = {
                executor.submit(self._process_file, file_path): file_path
                for file_path in files
            }

            # Procesar resultados conforme se completan
            completed = 0
            for future in as_completed(future_to_file):
                completed += 1
                file_path = future_to_file[future]

                try:
                    result = future.result()
                    self.results.append(result)

                    status = "✅" if result['success'] else "❌"
                    logger.info(
                        f"[{completed}/{total}] {status} {file_path.name}"
                    )

                except Exception as e:
                    logger.error(
                        f"[{completed}/{total}] ❌ {file_path.name}: {e}"
                    )
                    self.results.append({
                        'success': False,
                        'input_file': file_path,
                        'error': str(e)
                    })

    def _process_file(self, file_path: Path) -> Dict:
        """Procesa un archivo individual (para uso paralelo).

        Args:
            file_path: Ruta al archivo

        Returns:
            Diccionario con resultado
        """
        consolidator = ExcelConsolidator(
            output_dir=None,
            output_subdir=self.output_subdir,
            suffix=self.suffix
        )
        return consolidator.consolidate_file(file_path)

    def _simulate_processing(self, files: List[Path]) -> List[Dict]:
        """Simula el procesamiento (dry-run).

        Args:
            files: Lista de archivos

        Returns:
            Lista de resultados simulados
        """
        logger.info(f"🔍 Simulando procesamiento de {len(files)} archivos...\n")

        results = []
        for i, file_path in enumerate(files, start=1):
            # Determinar ruta de salida
            output_dir = file_path.parent / self.output_subdir
            output_file = output_dir / f"{file_path.stem}{self.suffix}{file_path.suffix}"

            logger.info(f"[{i}/{len(files)}] {file_path.name}")
            logger.info(f"  → {output_file}")

            results.append({
                'success': True,
                'input_file': file_path,
                'output_file': output_file,
                'simulated': True
            })

        return results

    def _log_summary(self, summary: Dict, dry_run: bool = False):
        """Registra el resumen del procesamiento.

        Args:
            summary: Diccionario con resumen
            dry_run: Si fue simulación
        """
        logger.info(f"\n{'='*60}")
        logger.info("📊 RESUMEN DE CONSOLIDACIÓN BATCH")
        logger.info(f"{'='*60}")
        logger.info(f"📁 Directorios procesados: {summary['directories_processed']}")
        logger.info(f"📄 Total archivos: {summary['total_files']}")
        logger.info(f"✅ Exitosos: {summary['successful']}")
        logger.info(f"❌ Fallidos: {summary['failed']}")
        logger.info(f"⏭️  Omitidos: {summary['skipped']}")
        logger.info(f"📈 Tasa de éxito: {summary['success_rate']:.1f}%")
        logger.info(f"⏱️  Tiempo total: {summary['total_time']:.2f}s")

        if summary['total_files'] > 0:
            avg_time = summary['total_time'] / summary['total_files']
            logger.info(f"⚡ Tiempo promedio: {avg_time:.2f}s por archivo")

        if dry_run:
            logger.info(f"\n⚠️  MODO DRY-RUN: No se crearon archivos")

    def get_summary(self) -> Dict:
        """Obtiene un resumen de todos los procesamientos realizados.

        Returns:
            Diccionario con estadísticas

        Example:
            >>> summary = batch.get_summary()
            >>> print(summary['total_rows_extracted'])
        """
        if not self.results:
            return {
                'total_processed': 0,
                'successful': 0,
                'failed': 0,
                'total_rows_extracted': 0
            }

        successful = sum(1 for r in self.results if r['success'])
        total_rows = sum(
            r.get('rows_extracted', 0)
            for r in self.results
            if r['success']
        )

        return {
            'total_processed': len(self.results),
            'successful': successful,
            'failed': len(self.results) - successful,
            'total_rows_extracted': total_rows,
            'results': self.results
        }

    def clear_results(self):
        """Limpia los resultados almacenados."""
        self.results = []
        logger.debug("Resultados limpiados")

    def __repr__(self) -> str:
        """Representación string del objeto."""
        return (
            f"BatchConsolidator("
            f"parallel={self.parallel}, "
            f"max_workers={self.max_workers}, "
            f"processed={len(self.results)})"
        )
