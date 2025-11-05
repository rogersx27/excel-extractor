"""Script CLI para consolidación batch de directorios con archivos Excel extraídos.

Este script procesa directorios completos de archivos Excel extraídos,
consolidando cada archivo automáticamente y preservando la estructura
de subdirectorios.

Uso:
    # Consolidar directorio completo
    python batch_consolidate_excel.py "data/COMPUTADOR 1_extraido/"

    # Con procesamiento paralelo
    python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8

    # Solo simular (dry-run)
    python batch_consolidate_excel.py "data/extraido/" --dry-run

    # Sin recursión (solo archivos de primer nivel)
    python batch_consolidate_excel.py "data/extraido/" --no-recursive
"""

import argparse
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from excel_consolidator import BatchConsolidator
from logger import setup_logger, setup_cli_logger

# Logger Nivel 1 - CLI: Configuración dinámica desde variables de entorno
logger = setup_cli_logger(setup_logger, __name__)


def main():
    """Función principal del script CLI."""

    parser = argparse.ArgumentParser(
        description="Consolidación batch de directorios con archivos Excel extraídos.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Consolidar directorio completo
  python batch_consolidate_excel.py "data/COMPUTADOR 1_extraido/"

  # Con procesamiento paralelo (más rápido)
  python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8

  # Solo simular sin crear archivos
  python batch_consolidate_excel.py "data/extraido/" --dry-run

  # Sin buscar en subdirectorios
  python batch_consolidate_excel.py "data/extraido/" --no-recursive

  # Con patrón personalizado
  python batch_consolidate_excel.py "data/extraido/" --pattern "*.xls"

  # Excluir patrones adicionales
  python batch_consolidate_excel.py "data/extraido/" --exclude "backup" "old"
        """,
    )

    # Argumento posicional
    parser.add_argument(
        "directory",
        type=str,
        help="Directorio con archivos Excel extraídos a consolidar"
    )

    # Argumentos opcionales
    parser.add_argument(
        "--subdir",
        type=str,
        default="consolidado",
        help="Nombre del subdirectorio para consolidados (default: consolidado)"
    )

    parser.add_argument(
        "-s", "--suffix",
        type=str,
        default="_consolidado",
        help="Sufijo para archivos consolidados (default: _consolidado)"
    )

    parser.add_argument(
        "-p", "--pattern",
        type=str,
        default="*.xlsx",
        help="Patrón de archivos a procesar (default: *.xlsx)"
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="No buscar recursivamente en subdirectorios"
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Usar procesamiento paralelo (más rápido para muchos archivos)"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=4,
        help="Número de workers para procesamiento paralelo (default: 4)"
    )

    parser.add_argument(
        "--exclude",
        nargs="+",
        default=[],
        help="Patrones adicionales a excluir (se suman a defaults: ~$, .tmp, temp, consolidado)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo simular, no crear archivos (útil para ver qué se procesaría)"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose con información detallada"
    )

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)

    # Validar directorio
    directory = Path(args.directory)
    if not directory.exists():
        logger.error(f"❌ El directorio no existe: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        logger.error(f"❌ La ruta no es un directorio: {directory}")
        sys.exit(1)

    # Información inicial
    logger.info(f"\n{'='*60}")
    logger.info("🚀 CONSOLIDACIÓN BATCH DE ARCHIVOS EXCEL")
    logger.info(f"{'='*60}")
    logger.info(f"📁 Directorio: {directory}")
    logger.info(f"📋 Patrón: {args.pattern}")
    logger.info(f"🔄 Recursivo: {not args.no_recursive}")
    logger.info(f"⚡ Paralelo: {args.parallel}")
    if args.parallel:
        logger.info(f"👷 Workers: {args.workers}")
    if args.dry_run:
        logger.info(f"🔍 Modo: DRY-RUN (simulación)")
    logger.info(f"{'='*60}\n")

    # Crear consolidador batch
    batch = BatchConsolidator(
        output_subdir=args.subdir,
        suffix=args.suffix,
        parallel=args.parallel,
        max_workers=args.workers,
        exclude_patterns=args.exclude
    )

    try:
        # Procesar directorio
        result = batch.consolidate_extracted_directory(
            directory=directory,
            recursive=not args.no_recursive,
            pattern=args.pattern,
            dry_run=args.dry_run
        )

        # Mostrar archivos procesados exitosamente
        if result['successful'] > 0:
            logger.info(f"\n{'='*60}")
            logger.info("✅ ARCHIVOS CONSOLIDADOS EXITOSAMENTE")
            logger.info(f"{'='*60}")

            successful_results = [r for r in result['results'] if r['success']]

            # Agrupar por directorio
            from collections import defaultdict
            by_directory = defaultdict(list)
            for r in successful_results:
                dir_name = r['input_file'].parent.name
                by_directory[dir_name].append(r)

            for dir_name, files in by_directory.items():
                logger.info(f"\n📂 {dir_name}/")
                for r in files:
                    logger.info(f"  ✅ {r['input_file'].name}")
                    if not args.dry_run:
                        logger.info(f"     📊 {r['rows_extracted']} filas extraídas")
                        logger.info(f"     ⏱️  {r['processing_time']:.2f}s")

        # Mostrar errores si los hay
        if result['failed'] > 0:
            logger.info(f"\n{'='*60}")
            logger.info("❌ ARCHIVOS CON ERRORES")
            logger.info(f"{'='*60}")

            failed_results = [r for r in result['results'] if not r['success'] and r.get('error')]
            for r in failed_results:
                logger.error(f"\n📄 {r['input_file'].name}")
                logger.error(f"   Error: {r['error']}")

        # Resumen final
        logger.info(f"\n{'='*60}")
        logger.info("📊 RESUMEN FINAL")
        logger.info(f"{'='*60}")
        logger.info(f"📁 Directorios procesados: {result['directories_processed']}")
        logger.info(f"📄 Total archivos: {result['total_files']}")
        logger.info(f"✅ Exitosos: {result['successful']}")
        logger.info(f"❌ Fallidos: {result['failed']}")
        logger.info(f"📈 Tasa de éxito: {result['success_rate']:.1f}%")
        logger.info(f"⏱️  Tiempo total: {result['total_time']:.2f}s")

        if result['total_files'] > 0:
            avg_time = result['total_time'] / result['total_files']
            logger.info(f"⚡ Tiempo promedio: {avg_time:.2f}s por archivo")

        # Información de salida
        if not args.dry_run and result['successful'] > 0:
            logger.info(f"\n📁 Archivos consolidados guardados en:")
            logger.info(f"   {directory / args.subdir}/")

        # Código de salida
        sys.exit(0 if result['failed'] == 0 else 1)

    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  Proceso interrumpido por el usuario")
        sys.exit(130)

    except Exception as e:
        logger.error(f"\n\n❌ Error durante el procesamiento: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
