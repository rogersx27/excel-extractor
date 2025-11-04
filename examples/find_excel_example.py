"""Ejemplo de uso del módulo find_excel_and_extract_sheets.

Este ejemplo demuestra cómo usar el nuevo módulo para buscar archivos
Excel y extraer sus hojas de forma optimizada.
"""
import sys
from pathlib import Path

# Añadir src al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from find_excel_and_extract_sheets import (
    find_and_extract_excel_sheets,
    scan_directory_info,
    ProcessingStrategy
)
from logger import setup_logger

# Configurar logging
logger = setup_logger(__name__)


def ejemplo_1_escanear_directorio():
    """Ejemplo 1: Escanear directorio para ver qué archivos Excel hay."""
    logger.info("=== Ejemplo 1: Escanear directorio ===")
    
    search_dir = Path("COMPUTADOR 1")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Escanear directorio
    info = scan_directory_info(search_dir, recursive=True)
    
    logger.info(f"📊 Información del directorio '{search_dir}':")
    logger.info(f"   Total de archivos Excel: {info['total_files']}")
    logger.info(f"   Tamaño total: {info['total_size_mb']:.2f} MB")
    
    if info['files']:
        logger.info("   Archivos encontrados:")
        for file_info in info['files']:
            logger.info(f"     - {file_info['name']} ({file_info['size_mb']:.2f} MB)")


def ejemplo_2_procesamiento_secuencial():
    """Ejemplo 2: Procesamiento secuencial (uno por uno)."""
    logger.info("=== Ejemplo 2: Procesamiento secuencial ===")
    
    search_dir = Path("COMPUTADOR 1")
    output_dir = Path("data/extracted_sequential")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Procesar secuencialmente
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        strategy=ProcessingStrategy.SEQUENTIAL,
        with_index=True,
        clean_names=True,
        max_size_mb=50.0  # Limitar a archivos de máximo 50MB
    )
    
    logger.info(f"✅ Resultado secuencial:")
    logger.info(f"   Procesados: {result.successful}/{result.total_files}")
    logger.info(f"   Tiempo: {result.total_time:.2f} segundos")
    logger.info(f"   Tasa de éxito: {result.success_rate:.1f}%")


def ejemplo_3_procesamiento_paralelo():
    """Ejemplo 3: Procesamiento paralelo (más rápido)."""
    logger.info("=== Ejemplo 3: Procesamiento paralelo ===")
    
    search_dir = Path("COMPUTADOR 1")
    output_dir = Path("data/extracted_parallel")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Procesar en paralelo con 2 workers
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        strategy=ProcessingStrategy.PARALLEL,
        max_workers=2,  # 2 archivos simultáneos
        with_index=True,
        clean_names=True,
        min_size_mb=0.001,  # Mínimo 1KB
        max_size_mb=100.0   # Máximo 100MB
    )
    
    logger.info(f"⚡ Resultado paralelo:")
    logger.info(f"   Procesados: {result.successful}/{result.total_files}")
    logger.info(f"   Tiempo: {result.total_time:.2f} segundos")
    logger.info(f"   Tasa de éxito: {result.success_rate:.1f}%")


def ejemplo_4_procesamiento_con_filtros():
    """Ejemplo 4: Procesamiento con filtros avanzados."""
    logger.info("=== Ejemplo 4: Procesamiento con filtros ===")
    
    search_dir = Path("COMPUTADOR 1")
    output_dir = Path("data/extracted_filtered")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Procesar con filtros específicos
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        strategy=ProcessingStrategy.PARALLEL,
        max_workers=3,
        recursive=True,
        # Filtros de archivos
        min_size_mb=0.01,   # Mínimo 10KB
        max_size_mb=25.0,   # Máximo 25MB
        exclude_patterns=[  # Excluir archivos que contengan estos patrones
            "temp",
            "backup", 
            "~$",       # Archivos temporales de Excel
            ".tmp"
        ],
        # Parámetros de extracción
        with_index=True,
        clean_names=True
    )
    
    logger.info(f"🔍 Resultado filtrado:")
    logger.info(f"   Procesados: {result.successful}/{result.total_files}")
    logger.info(f"   Tiempo: {result.total_time:.2f} segundos")
    
    # Mostrar detalles de archivos fallidos
    if result.failed > 0:
        logger.info("❌ Archivos con errores:")
        for r in result.results:
            if not r.success:
                logger.info(f"   - {r.excel_file.path.name}: {r.error_message}")


def ejemplo_5_procesamiento_por_lotes():
    """Ejemplo 5: Procesamiento por lotes (optimizado para memoria)."""
    logger.info("=== Ejemplo 5: Procesamiento por lotes ===")
    
    search_dir = Path("COMPUTADOR 1")
    output_dir = Path("data/extracted_batch")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Procesar por lotes (útil cuando hay muchos archivos)
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        strategy=ProcessingStrategy.BATCH,
        max_workers=2,      # Workers por lote
        with_index=True,
        clean_names=True
    )
    
    logger.info(f"📦 Resultado por lotes:")
    logger.info(f"   Procesados: {result.successful}/{result.total_files}")
    logger.info(f"   Tiempo: {result.total_time:.2f} segundos")
    
    # Estadísticas detalladas
    if result.results:
        tiempos = [r.processing_time for r in result.results if r.success]
        if tiempos:
            tiempo_promedio = sum(tiempos) / len(tiempos)
            logger.info(f"   Tiempo promedio por archivo: {tiempo_promedio:.2f} segundos")


def ejemplo_6_procesamiento_hojas_especificas():
    """Ejemplo 6: Extraer solo hojas específicas."""
    logger.info("=== Ejemplo 6: Hojas específicas ===")
    
    search_dir = Path("COMPUTADOR 1")
    output_dir = Path("data/extracted_specific_sheets")
    
    if not search_dir.exists():
        logger.warning(f"Directorio no existe: {search_dir}")
        return
    
    # Definir hojas específicas que nos interesan
    # (intentará extraer estas hojas si existen)
    hojas_deseadas = ['Sheet1', 'Hoja1', 'Datos', 'Data', 'Resumen']
    
    # Nota: extract_excel_sheets no tiene parámetro sheet_names directo,
    # pero podemos usar una función wrapper personalizada
    result = find_and_extract_excel_sheets(
        search_directory=search_dir,
        output_directory=output_dir,
        strategy=ProcessingStrategy.PARALLEL,
        max_workers=2,
        with_index=False,    # Sin índice para nombres más limpios
        clean_names=True
    )
    
    logger.info(f"📋 Resultado hojas específicas:")
    logger.info(f"   Procesados: {result.successful}/{result.total_files}")


def ejecutar_todos_los_ejemplos():
    """Ejecuta todos los ejemplos del módulo."""
    logger.info("\n" + "="*80)
    logger.info("🚀 EJECUTANDO EJEMPLOS DE FIND_EXCEL_AND_EXTRACT_SHEETS")
    logger.info("="*80 + "\n")
    
    ejemplos = [
        ejemplo_1_escanear_directorio,
        ejemplo_2_procesamiento_secuencial,
        ejemplo_3_procesamiento_paralelo,
        ejemplo_4_procesamiento_con_filtros,
        ejemplo_5_procesamiento_por_lotes,
        ejemplo_6_procesamiento_hojas_especificas,
    ]
    
    for i, ejemplo in enumerate(ejemplos, 1):
        try:
            print(f"\n{'─'*80}")
            ejemplo()
            print(f"{'─'*80}\n")
        except Exception as e:
            logger.error(f"❌ Error en ejemplo {i}: {e}")
    
    logger.info("\n" + "="*80)
    logger.info("✅ TODOS LOS EJEMPLOS COMPLETADOS")
    logger.info("="*80)


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejecutar_todos_los_ejemplos()
    
    # O ejecutar un ejemplo específico:
    # ejemplo_1_escanear_directorio()
    # ejemplo_3_procesamiento_paralelo()
