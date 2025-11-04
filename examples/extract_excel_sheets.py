"""Script CLI para extraer hojas individuales de un archivo Excel.

Este script proporciona una interfaz de línea de comandos para el módulo
excel_extractor, permitiendo extraer hojas de archivos Excel fácilmente.

Uso:
    python src/extract_excel_sheets.py "ruta/al/archivo.xlsx"
    python src/extract_excel_sheets.py "COMPUTADOR 1/F-SC-04 Control de clientes SWX113.xlsx"

Características:
- Crea una carpeta con el nombre del archivo original
- Extrae cada hoja en un archivo separado
- Nomenclatura: 01_NombreHoja.xlsx, 02_NombreHoja.xlsx, etc.
- Preserva toda la data (valores, encabezados, estructura)
- Ignora imágenes y estilos avanzados (solo data)
"""
import argparse
import sys
from pathlib import Path

from excel_extractor import extract_excel_sheets
from logger import setup_logger

# Configurar logger
logger = setup_logger(__name__, level="INFO")


def main():
    """Función principal del script CLI."""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Extrae hojas individuales de un archivo Excel en archivos separados.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python src/extract_excel_sheets.py "archivo.xlsx"
  python src/extract_excel_sheets.py "COMPUTADOR 1/F-SC-04 Control de clientes SWX113.xlsx"
  python src/extract_excel_sheets.py "datos/ventas.xlsx" --output "resultados/"
  python src/extract_excel_sheets.py "archivo.xlsx" --sheets "Hoja1" "Hoja2"

El script creará una carpeta con el nombre del archivo y guardará cada hoja
en un archivo Excel separado con formato: 01_NombreHoja.xlsx, 02_NombreHoja.xlsx
        """
    )

    parser.add_argument(
        'excel_file',
        type=str,
        help='Ruta al archivo Excel a procesar'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Directorio base de salida (default: data/)'
    )

    parser.add_argument(
        '-s', '--sheets',
        nargs='+',
        default=None,
        help='Hojas específicas a extraer (default: todas)'
    )

    parser.add_argument(
        '--no-index',
        action='store_true',
        help='No añadir índice numérico a los nombres de archivo'
    )

    parser.add_argument(
        '--no-clean',
        action='store_true',
        help='No limpiar caracteres inválidos de nombres de archivo'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Modo verbose con información detallada'
    )

    args = parser.parse_args()

    # Configurar nivel de logging
    if args.verbose:
        import logging
        logger.setLevel(logging.DEBUG)

    # Convertir ruta del archivo a Path
    excel_path = Path(args.excel_file)

    # Directorio de salida
    output_dir = Path(args.output) if args.output else None

    try:
        # Ejecutar extracción usando el módulo
        result = extract_excel_sheets(
            excel_file=excel_path,
            output_base_dir=output_dir,
            sheet_names=args.sheets,
            with_index=not args.no_index,
            clean_names=not args.no_clean
        )

        # Éxito
        sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)

    except ValueError as e:
        logger.error(f"❌ {e}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"❌ Error inesperado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
