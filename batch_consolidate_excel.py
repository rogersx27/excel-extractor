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
from logger.pretty import (
    log_header,
    log_section,
    log_info,
    log_success,
    log_error,
    log_warning,
    log_item,
    log_stats,
    log_blank,
    log_separator,
    format_number,
    format_duration,
    indent
)

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
        log_error(logger, f"El directorio no existe: {directory}")
        sys.exit(1)

    if not directory.is_dir():
        log_error(logger, f"La ruta no es un directorio: {directory}")
        sys.exit(1)

    # Información inicial
    log_blank(logger)
    log_header(logger, "CONSOLIDACIÓN BATCH DE ARCHIVOS EXCEL", icon="🚀")
    
    log_section(logger, "Configuración", icon="⚙️")
    with indent():
        log_item(logger, "Directorio", directory)
        log_item(logger, "Patrón", args.pattern)
        log_item(logger, "Recursivo", "Sí" if not args.no_recursive else "No")
        log_item(logger, "Paralelo", "Sí" if args.parallel else "No")
        if args.parallel:
            log_item(logger, "Workers", args.workers)
        if args.dry_run:
            log_item(logger, "Modo", "DRY-RUN (simulación)", bullet="└─")
        
    log_blank(logger)

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
            log_blank(logger)
            log_section(logger, "ARCHIVOS CONSOLIDADOS EXITOSAMENTE", icon="✅")

            successful_results = [r for r in result['results'] if r['success']]

            # Agrupar por directorio
            from collections import defaultdict
            by_directory = defaultdict(list)
            for r in successful_results:
                dir_name = r['input_file'].parent.name
                by_directory[dir_name].append(r)

            for dir_name, files in by_directory.items():
                log_blank(logger)
                log_section(logger, f"{dir_name}/", icon="📂")
                
                with indent():
                    for r in files:
                        log_success(logger, r['input_file'].name)
                        if not args.dry_run:
                            with indent():
                                log_item(logger, "Filas extraídas", format_number(r['rows_extracted']))
                                log_item(logger, "Tiempo", f"{r['processing_time']:.2f}s", bullet="└─")

        # Mostrar errores si los hay
        if result['failed'] > 0:
            log_blank(logger)
            log_section(logger, "ARCHIVOS CON ERRORES", icon="❌")

            failed_results = [r for r in result['results'] if not r['success'] and r.get('error')]
            
            with indent():
                for r in failed_results:
                    log_blank(logger)
                    log_error(logger, r['input_file'].name)
                    with indent():
                        log_item(logger, "Error", r['error'], bullet="└─")

        # Resumen final
        log_blank(logger)
        log_stats(logger, {
            "Directorios procesados": result['directories_processed'],
            "Total archivos": format_number(result['total_files']),
            "Exitosos": format_number(result['successful']),
            "Fallidos": result['failed'],
            "Tasa de éxito": f"{result['success_rate']:.1f}%",
            "Tiempo total": format_duration(result['total_time'])
        }, title="RESUMEN FINAL")

        if result['total_files'] > 0:
            avg_time = result['total_time'] / result['total_files']
            log_blank(logger)
            with indent():
                log_item(logger, "Tiempo promedio", f"{avg_time:.2f}s por archivo", bullet="└─")

        # Información de salida
        if not args.dry_run and result['successful'] > 0:
            log_blank(logger)
            log_section(logger, "Archivos consolidados guardados en:", icon="📁")
            with indent():
                log_item(logger, "Ubicación", directory / args.subdir, bullet="└─")

        # Código de salida
        sys.exit(0 if result['failed'] == 0 else 1)

    except KeyboardInterrupt:
        log_blank(logger, lines=2)
        log_warning(logger, "Proceso interrumpido por el usuario")
        sys.exit(130)

    except Exception as e:
        log_blank(logger, lines=2)
        log_error(logger, f"Error durante el procesamiento: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
