"""Ejemplo de uso de Pretty Logging.

Este script demuestra todas las funciones de pretty logging disponibles.

Uso:
    python examples/pretty_logging_example.py
"""
import sys
import time
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from logger import (
    setup_cli_logger,
    setup_logger,
    # Formato básico
    log_header,
    log_section,
    log_subsection,
    log_info,
    log_success,
    log_error,
    log_warning,
    log_blank,
    log_separator,
    # Estructuras
    log_dict,
    log_list,
    log_stats,
    log_table,
    # Context helpers
    log_file_info,
    log_sheet_info,
    # Indentación
    indent,
    # Formatters
    format_number,
    format_bytes,
    format_duration,
)


def main():
    """Ejecuta ejemplos de pretty logging."""

    # Configurar logger
    logger = setup_cli_logger(setup_logger, __name__)

    # ========================================================================
    # Ejemplo 1: Headers y Secciones
    # ========================================================================
    log_blank(logger)
    log_header(logger, "PRETTY LOGGING - EJEMPLOS", icon="🎨")

    log_section(logger, "Ejemplo 1: Formato Básico", icon="📝")

    with indent():
        log_info(logger, "Este es un mensaje informativo")
        log_success(logger, "Operación completada exitosamente")
        log_warning(logger, "Esto es una advertencia")
        log_error(logger, "Esto es un error (no te preocupes, es un ejemplo)")

    # ========================================================================
    # Ejemplo 2: Listas y Diccionarios
    # ========================================================================
    log_blank(logger)
    log_section(logger, "Ejemplo 2: Datos Estructurados", icon="🗂️")

    with indent():
        # Diccionario
        user_data = {
            "Nombre": "Juan Pérez",
            "Email": "juan@example.com",
            "Rol": "Administrador",
            "Activo": True
        }
        log_dict(logger, user_data, title="Información de Usuario")

        log_blank(logger)

        # Lista
        files = ["ventas_enero.xlsx", "ventas_febrero.xlsx", "ventas_marzo.xlsx"]
        log_list(logger, files, title="Archivos Procesados")

    # ========================================================================
    # Ejemplo 3: Estadísticas
    # ========================================================================
    log_blank(logger)
    log_section(logger, "Ejemplo 3: Estadísticas", icon="📊")

    with indent():
        stats = {
            "Archivos procesados": format_number(1234),
            "Total de filas": format_number(567890),
            "Tamaño total": format_bytes(12582912),
            "Tiempo de procesamiento": format_duration(145.7),
            "Errores": 0,
            "Estado": "✅ Completado"
        }
        log_stats(logger, stats)

    # ========================================================================
    # Ejemplo 4: Tablas
    # ========================================================================
    log_blank(logger)
    log_section(logger, "Ejemplo 4: Tablas", icon="📋")

    with indent():
        headers = ["Archivo", "Filas", "Estado"]
        rows = [
            ["ventas.xlsx", format_number(1250), "✅ OK"],
            ["clientes.xlsx", format_number(890), "✅ OK"],
            ["productos.xlsx", format_number(450), "⚠️  Warnings"]
        ]
        log_table(logger, headers, rows)

    # ========================================================================
    # Ejemplo 5: Información de Archivos Excel
    # ========================================================================
    log_blank(logger)
    log_section(logger, "Ejemplo 5: Información de Excel", icon="📄")

    with indent():
        # Archivo
        log_file_info(logger, "ventas_2024.xlsx", {
            "Tamaño": format_bytes(2621440),
            "Hojas": 3,
            "Formato": "XLSX"
        })

        # Hojas
        log_blank(logger)
        log_sheet_info(logger, "Enero", {
            "Tipo": "SIMPLE",
            "Filas": format_number(1250),
            "Columnas": 8,
            "Encabezados": 1
        })

        log_blank(logger)
        log_sheet_info(logger, "Febrero", {
            "Tipo": "COMPLEX",
            "Filas": format_number(2340),
            "Columnas": 8,
            "Encabezados": 5
        })

    # ========================================================================
    # Ejemplo 6: Indentación Jerárquica
    # ========================================================================
    log_blank(logger)
    log_section(logger, "Ejemplo 6: Jerarquías con Indentación", icon="🌳")

    with indent():
        log_subsection(logger, "Procesando directorio: data/")

        with indent():
            log_file_info(logger, "archivo1.xlsx", {"Hojas": 2})

            with indent():
                log_success(logger, "Hoja 'Ventas' procesada")
                log_success(logger, "Hoja 'Resumen' procesada")

            log_blank(logger)
            log_file_info(logger, "archivo2.xlsx", {"Hojas": 1})

            with indent():
                log_success(logger, "Hoja 'Datos' procesada")

    # ========================================================================
    # Ejemplo 7: Simulación de Proceso Completo
    # ========================================================================
    log_blank(logger)
    log_separator(logger)
    log_blank(logger)
    log_header(logger, "SIMULACIÓN DE PROCESO REAL", icon="🚀")

    log_section(logger, "Iniciando consolidación de archivos...")

    with indent():
        # Simular análisis
        log_info(logger, "Analizando estructura de archivos...")
        time.sleep(0.5)
        log_success(logger, "Estructura analizada: 3 archivos encontrados")

        log_blank(logger)

        # Simular procesamiento
        log_section(logger, "Procesando archivos", icon="⚙️")

        with indent():
            for i in range(1, 4):
                filename = f"archivo_{i}.xlsx"
                log_info(logger, f"Procesando {filename}...")
                time.sleep(0.3)

                with indent():
                    log_success(logger, f"{format_number(1000 + i * 100)} filas extraídas")

        log_blank(logger)

        # Resultado final
        log_stats(logger, {
            "Archivos procesados": 3,
            "Total de filas": format_number(3300),
            "Tiempo total": format_duration(2.1),
            "Estado": "✅ Completado exitosamente"
        }, title="Resultado Final")

    # ========================================================================
    # Finalización
    # ========================================================================
    log_blank(logger)
    log_separator(logger)
    log_blank(logger)
    log_success(logger, "🎉 Todos los ejemplos ejecutados correctamente!")
    log_blank(logger)


if __name__ == "__main__":
    main()
