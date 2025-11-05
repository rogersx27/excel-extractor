"""Script CLI para consolidar archivos Excel extraídos.

Este script permite consolidar archivos Excel con estructuras simples o complejas,
extrayendo todas las tablas y generando archivos consolidados limpios.

Uso:
    # Consolidar un archivo específico
    python consolidate_excel.py archivo.xlsx

    # Consolidar un directorio completo
    python consolidate_excel.py directorio/

    # Con directorio de salida personalizado
    python consolidate_excel.py datos/ --output resultados/

    # Recursivo en subdirectorios
    python consolidate_excel.py datos/ --recursive

    # Análisis previo (sin consolidar)
    python consolidate_excel.py archivo.xlsx --analyze-only
"""

import argparse
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from excel_consolidator import ExcelConsolidator, analyze_file_completely
from logger import setup_logger

# Logger Nivel 1 - CLI: INFO con consola y archivo para interacción con usuario
logger = setup_logger(
    __name__,
    level="INFO",
    console_output=True,
    file_output=True
)


def main():
    """Función principal del script CLI."""

    parser = argparse.ArgumentParser(
        description="Consolida archivos Excel extraídos con estructuras simples o complejas.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Consolidar un archivo
  python consolidate_excel.py "data/extraido/02_RUTA 113.xlsx"

  # Consolidar directorio completo
  python consolidate_excel.py "data/COMPUTADOR 1_extraido/Ruta 886-113 nueva(Recuperado automáticamente)/"

  # Con directorio de salida personalizado
  python consolidate_excel.py datos/ --output consolidados/

  # Recursivo (buscar en subdirectorios)
  python consolidate_excel.py datos/ --recursive

  # Solo analizar estructura (sin consolidar)
  python consolidate_excel.py archivo.xlsx --analyze-only

  # Excluir patrones
  python consolidate_excel.py datos/ --exclude "~$" ".tmp" "backup"
        """,
    )

    # Argumento posicional
    parser.add_argument(
        "path",
        type=str,
        help="Ruta al archivo Excel o directorio a consolidar"
    )

    # Argumentos opcionales
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Directorio de salida para archivos consolidados (default: misma ubicación + /consolidado)"
    )

    parser.add_argument(
        "-s", "--suffix",
        type=str,
        default="_consolidado",
        help="Sufijo para archivos consolidados (default: _consolidado)"
    )

    parser.add_argument(
        "--subdir",
        type=str,
        default="consolidado",
        help="Nombre del subdirectorio de salida (default: consolidado)"
    )

    parser.add_argument(
        "-r", "--recursive",
        action="store_true",
        help="Buscar recursivamente en subdirectorios (solo para directorios)"
    )

    parser.add_argument(
        "-p", "--pattern",
        type=str,
        default="*.xlsx",
        help="Patrón de archivos a procesar (default: *.xlsx)"
    )

    parser.add_argument(
        "--exclude",
        nargs="+",
        default=["~$", ".tmp", "temp", "consolidado"],
        help="Patrones a excluir en nombres/rutas (default: ~$ .tmp temp consolidado)"
    )

    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Solo analizar estructura sin consolidar"
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

    # Validar ruta
    path = Path(args.path)
    if not path.exists():
        logger.error(f"❌ La ruta no existe: {path}")
        sys.exit(1)

    # Modo análisis solamente
    if args.analyze_only:
        logger.info(f"\n{'='*60}")
        logger.info("📊 MODO ANÁLISIS (sin consolidar)")
        logger.info(f"{'='*60}\n")

        if path.is_file():
            logger.info(f"Analizando archivo: {path.name}")
            analysis = analyze_file_completely(path)

            logger.info(f"\n📄 Archivo: {path.name}")
            logger.info(f"   Hojas: {analysis['total_sheets']}")

            for sheet, info in analysis['sheets'].items():
                logger.info(f"\n   📋 Hoja: {sheet}")
                logger.info(f"      Tipo: {info['type'].upper()}")
                logger.info(f"      Encabezados: {len(info['header_rows'])}")
                logger.info(f"      Filas totales: {info['total_rows']}")

                if info['header_rows']:
                    logger.info(f"      Encabezados en filas: {info['header_rows']}")
                if info['data_ranges']:
                    logger.info(f"      Rangos de datos: {info['data_ranges']}")
        else:
            logger.error("❌ Modo análisis solo soporta archivos individuales")
            sys.exit(1)

        sys.exit(0)

    # Modo consolidación
    logger.info(f"\n{'='*60}")
    logger.info("🚀 CONSOLIDADOR DE EXCEL")
    logger.info(f"{'='*60}\n")

    # Crear consolidador
    consolidator = ExcelConsolidator(
        output_dir=args.output,
        output_subdir=args.subdir,
        suffix=args.suffix
    )

    # Procesar archivo o directorio
    if path.is_file():
        # Consolidar archivo individual
        logger.info(f"📄 Consolidando archivo: {path.name}\n")
        result = consolidator.consolidate_file(path)

        if result['success']:
            logger.info(f"\n✅ CONSOLIDACIÓN EXITOSA")
            logger.info(f"   📊 Filas extraídas: {result['rows_extracted']}")
            logger.info(f"   📋 Columnas: {len(result['columns'])}")
            logger.info(f"   📁 Archivo guardado: {result['output_file']}")
            logger.info(f"   ⏱️  Tiempo: {result['processing_time']:.2f}s")
            sys.exit(0)
        else:
            logger.error(f"\n❌ ERROR EN CONSOLIDACIÓN")
            logger.error(f"   {result['error']}")
            sys.exit(1)

    elif path.is_dir():
        # Consolidar directorio
        logger.info(f"📁 Consolidando directorio: {path}\n")

        summary = consolidator.consolidate_directory(
            directory=path,
            pattern=args.pattern,
            recursive=args.recursive,
            exclude_patterns=args.exclude
        )

        # Mostrar detalles de archivos exitosos
        if summary['successful'] > 0:
            logger.info(f"\n{'='*60}")
            logger.info("✅ ARCHIVOS CONSOLIDADOS EXITOSAMENTE")
            logger.info(f"{'='*60}")

            for result in summary['results']:
                if result['success']:
                    logger.info(f"\n📄 {result['input_file'].name}")
                    logger.info(f"   📊 Filas: {result['rows_extracted']}")
                    logger.info(f"   📋 Columnas: {len(result['columns'])}")
                    logger.info(f"   ⏱️  Tiempo: {result['processing_time']:.2f}s")

        # Mostrar errores si los hay
        if summary['failed'] > 0:
            logger.info(f"\n{'='*60}")
            logger.info("❌ ARCHIVOS CON ERRORES")
            logger.info(f"{'='*60}")

            for result in summary['results']:
                if not result['success']:
                    logger.error(f"\n📄 {result['input_file'].name}")
                    logger.error(f"   Error: {result['error']}")

        # Código de salida
        sys.exit(0 if summary['failed'] == 0 else 1)

    else:
        logger.error(f"❌ La ruta debe ser un archivo o directorio: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
