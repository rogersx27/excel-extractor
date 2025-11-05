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
from logger import (
    setup_logger,
    setup_cli_logger,
    log_header,
    log_section,
    log_file_info,
    log_sheet_info,
    log_success,
    log_error,
    log_item,
    log_stats,
    log_blank,
    indent,
    format_number,
)

# Logger Nivel 1 - CLI: Configuración dinámica desde variables de entorno
logger = setup_cli_logger(setup_logger, __name__)


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
        log_error(logger, f"La ruta no existe: {path}")
        sys.exit(1)

    # Modo análisis solamente
    if args.analyze_only:
        log_blank(logger)
        log_header(logger, "MODO ANÁLISIS (sin consolidar)", icon="📊")

        if path.is_file():
            # Analizar archivo
            analysis = analyze_file_completely(path)

            # Mostrar información del archivo
            log_file_info(logger, path.name, {"Hojas": analysis['total_sheets']})

            # Mostrar información de cada hoja
            for sheet, info in analysis['sheets'].items():
                log_blank(logger)

                sheet_data = {
                    "Tipo": info['type'].upper(),
                    "Encabezados": len(info['header_rows']),
                    "Filas totales": format_number(info['total_rows']),
                }

                if info['header_rows']:
                    sheet_data["Encabezados en filas"] = info['header_rows']
                if info['data_ranges']:
                    sheet_data["Rangos de datos"] = f"{len(info['data_ranges'])} rangos"

                log_sheet_info(logger, sheet, sheet_data)

            log_blank(logger)
            log_success(logger, "Análisis completado")
        else:
            log_error(logger, "Modo análisis solo soporta archivos individuales")
            sys.exit(1)

        sys.exit(0)

    # Modo consolidación
    log_blank(logger)
    log_header(logger, "CONSOLIDADOR DE EXCEL", icon="🚀")

    # Crear consolidador
    consolidator = ExcelConsolidator(
        output_dir=args.output,
        output_subdir=args.subdir,
        suffix=args.suffix
    )

    # Procesar archivo o directorio
    if path.is_file():
        # Consolidar archivo individual
        log_section(logger, f"Consolidando archivo: {path.name}", icon="📄")
        log_blank(logger)

        result = consolidator.consolidate_file(path)

        if result['success']:
            log_blank(logger)
            log_stats(logger, {
                "Estado": "✅ Exitoso",
                "Filas extraídas": format_number(result['rows_extracted']),
                "Columnas": len(result['columns']),
                "Archivo guardado": result['output_file'].name,
                "Tiempo": f"{result['processing_time']:.2f}s"
            }, title="Resultado de Consolidación")
            sys.exit(0)
        else:
            log_blank(logger)
            log_error(logger, f"Error en consolidación: {result['error']}")
            sys.exit(1)

    elif path.is_dir():
        # Consolidar directorio
        log_section(logger, f"Consolidando directorio: {path}", icon="📁")
        log_blank(logger)

        summary = consolidator.consolidate_directory(
            directory=path,
            pattern=args.pattern,
            recursive=args.recursive,
            exclude_patterns=args.exclude
        )

        # Mostrar resumen general
        log_blank(logger)
        log_stats(logger, {
            "Total archivos": summary['total_files'],
            "Exitosos": f"✅ {summary['successful']}",
            "Fallidos": f"❌ {summary['failed']}",
            "Omitidos": summary['skipped'],
        }, title="Resumen General")

        # Mostrar detalles de archivos exitosos
        if summary['successful'] > 0:
            log_blank(logger)
            log_section(logger, "Archivos Consolidados Exitosamente", icon="✅")

            with indent():
                for result in summary['results']:
                    if result['success']:
                        log_blank(logger)
                        log_file_info(logger, result['input_file'].name, {
                            "Filas": format_number(result['rows_extracted']),
                            "Columnas": len(result['columns']),
                            "Tiempo": f"{result['processing_time']:.2f}s"
                        })

        # Mostrar errores si los hay
        if summary['failed'] > 0:
            log_blank(logger)
            log_section(logger, "Archivos con Errores", icon="❌")

            with indent():
                for result in summary['results']:
                    if not result['success']:
                        log_blank(logger)
                        log_error(logger, f"{result['input_file'].name}: {result['error']}")

        # Código de salida
        sys.exit(0 if summary['failed'] == 0 else 1)

    else:
        log_error(logger, f"La ruta debe ser un archivo o directorio: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
