"""Script CLI reutilizable para procesar archivos Excel de cualquier directorio.

Este script busca y extrae todas las hojas de los archivos Excel
encontrados en un directorio especificado.

Uso:
    python process_excel_directory.py "COMPUTADOR 1"
    python process_excel_directory.py "mis_datos" --output "resultados/"
    python process_excel_directory.py "informes/" --parallel --workers 8
"""

import argparse
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from find_excel_and_extract_sheets import find_and_extract_excel_sheets, scan_directory
from logger import setup_logger

# Configurar logger
logger = setup_logger(__name__, level="INFO")


def main():
    """Procesa archivos Excel de un directorio."""

    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Procesa archivos Excel de un directorio, extrayendo sus hojas en archivos separados.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Básico - procesar directorio
  python process_excel_directory.py "COMPUTADOR 1"

  # Con directorio de salida personalizado
  python process_excel_directory.py "datos/" --output "resultados/"

  # Procesamiento secuencial (más seguro para archivos grandes)
  python process_excel_directory.py "archivos/" --sequential

  # Procesamiento paralelo con más workers
  python process_excel_directory.py "informes/" --workers 8

  # Con filtros de tamaño
  python process_excel_directory.py "datos/" --min-size 0.1 --max-size 50

  # Excluir patrones específicos
  python process_excel_directory.py "datos/" --exclude "temp" "backup" "~$"

  # Sin escaneo previo (más rápido)
  python process_excel_directory.py "datos/" --no-scan
        """,
    )

    # Argumento posicional
    parser.add_argument(
        "directory", type=str, help="Directorio donde buscar archivos Excel"
    )

    # Argumentos opcionales
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Directorio de salida para las extracciones (default: data/[nombre_directorio]_extraido)",
    )

    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="No buscar recursivamente en subdirectorios",
    )

    parser.add_argument(
        "--sequential",
        action="store_true",
        help="Procesamiento secuencial en lugar de paralelo",
    )

    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=4,
        help="Número de workers para procesamiento paralelo (default: 4)",
    )

    parser.add_argument(
        "--min-size",
        type=float,
        default=0.001,
        help="Tamaño mínimo de archivo en MB (default: 0.001 = 1KB)",
    )

    parser.add_argument(
        "--max-size",
        type=float,
        default=100.0,
        help="Tamaño máximo de archivo en MB (default: 100.0)",
    )

    parser.add_argument(
        "--exclude",
        nargs="+",
        default=["~$", ".tmp", "temp"],
        help="Patrones a excluir en nombres/rutas (default: ~$ .tmp temp)",
    )

    parser.add_argument(
        "--no-index",
        action="store_true",
        help="No añadir índice numérico a los archivos extraídos",
    )

    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="No limpiar caracteres inválidos de nombres de archivo",
    )

    parser.add_argument(
        "--no-scan",
        action="store_true",
        help="No escanear antes de procesar (procesamiento directo)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Modo verbose con información detallada",
    )

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        import logging

        logger.setLevel(logging.DEBUG)

    # Validar directorio
    search_dir = Path(args.directory)
    if not search_dir.exists():
        logger.error(f"❌ El directorio no existe: {search_dir}")
        sys.exit(1)

    # Determinar directorio de salida
    if args.output:
        output_dir = args.output
    else:
        # Por defecto: data/[nombre_directorio]_extraido
        dir_name = search_dir.name if search_dir.name else "archivos"
        output_dir = f"data/{dir_name}_extraido"

    # 1. Escaneo previo (opcional)
    if not args.no_scan:
        logger.info("📊 Escaneando directorio...")
        info = scan_directory(search_dir, recursive=not args.no_recursive)

        logger.info(f"\n{'='*60}")
        logger.info("📁 ARCHIVOS ENCONTRADOS")
        logger.info(f"{'='*60}")
        logger.info(f"Total: {info['total_files']} archivos Excel")
        logger.info(f"Tamaño total: {info['total_size_mb']:.2f} MB")

        if info["total_files"] > 0:
            logger.info(f"\nArchivos:")
            for file in info["files"]:
                logger.info(f"  - {file['name']} ({file['size_mb']:.2f} MB)")
        else:
            logger.warning("⚠️  No se encontraron archivos Excel")
            sys.exit(0)

        logger.info(f"\n{'='*60}")
        logger.info("🚀 INICIANDO PROCESAMIENTO")
        logger.info(f"{'='*60}\n")

    # 2. Procesar archivos
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        recursive=not args.no_recursive,
        parallel=not args.sequential,
        max_workers=args.workers,
        min_size_mb=args.min_size,
        max_size_mb=args.max_size,
        exclude_patterns=args.exclude,
        with_index=not args.no_index,
        clean_names=not args.no_clean,
    )

    # 3. Mostrar resumen final
    logger.info(f"\n{'='*60}")
    logger.info("✅ PROCESAMIENTO COMPLETADO")
    logger.info(f"{'='*60}")
    logger.info(f"📊 Total archivos: {result['total_files']}")
    logger.info(f"✅ Exitosos: {result['successful']}")
    logger.info(f"❌ Fallidos: {result['failed']}")
    logger.info(f"📈 Tasa de éxito: {result['success_rate']:.1f}%")
    logger.info(f"⏱️  Tiempo total: {result['total_time']:.2f} segundos")

    # 4. Mostrar detalles de archivos procesados
    if result["successful"] > 0:
        logger.info(f"\n✅ Archivos procesados exitosamente:")
        for r in result["results"]:
            if r["success"]:
                logger.info(f"\n  📄 {r['excel_file']['path'].name}")
                logger.info(f"     Hojas extraídas: {len(r['files_created'])}")
                logger.info(f"     Ubicación: {r['output_dir']}")
                logger.info(f"     Tiempo: {r['processing_time']:.2f}s")

    # 5. Mostrar errores si los hay
    if result["failed"] > 0:
        logger.info(f"\n❌ Archivos con errores:")
        for r in result["results"]:
            if not r["success"]:
                logger.info(f"  - {r['excel_file']['path'].name}")
                logger.info(f"    Error: {r.get('error', 'Desconocido')}")

    # 6. Código de salida
    sys.exit(0 if result["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
