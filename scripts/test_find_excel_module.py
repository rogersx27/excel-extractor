"""Script de prueba para el módulo find_excel_and_extract_sheets.

Este script verifica que el nuevo módulo funciona correctamente
sin procesar archivos reales.
"""
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from find_excel_and_extract_sheets import (
    ProcessingStrategy,
    ExcelFinder,
    ExcelBatchProcessor,
    ExcelFile
)
from logger import setup_logger

logger = setup_logger(__name__)


def test_excel_finder():
    """Prueba el buscador de archivos Excel."""
    logger.info("🧪 Probando ExcelFinder...")
    
    # Crear finder con configuración de prueba
    finder = ExcelFinder(
        min_size_mb=0.001,  # 1KB mínimo
        max_size_mb=50.0,   # 50MB máximo
        exclude_patterns=['temp', 'backup']
    )
    
    logger.info(f"✓ ExcelFinder creado con filtros:")
    logger.info(f"  - Tamaño: {finder.min_size_bytes/1024:.1f}KB - {finder.max_size_bytes/1024/1024:.1f}MB")
    logger.info(f"  - Exclusiones: {finder.exclude_patterns}")
    
    # Probar validación de archivos
    test_files = [
        Path("test.xlsx"),
        Path("test.xls"), 
        Path("test.pdf"),  # No debería ser válido
        Path("test.txt")   # No debería ser válido
    ]
    
    logger.info("✓ Validación de extensiones:")
    for test_file in test_files:
        # Simular que el archivo existe creando uno temporal pequeño
        try:
            test_file.touch()
            is_valid = finder._is_valid_excel_file(test_file)
            logger.info(f"  - {test_file.name}: {'✓' if is_valid else '✗'}")
            test_file.unlink()  # Limpiar archivo temporal
        except:
            pass


def test_processing_strategies():
    """Prueba las estrategias de procesamiento."""
    logger.info("🧪 Probando estrategias de procesamiento...")
    
    strategies = [
        ProcessingStrategy.SEQUENTIAL,
        ProcessingStrategy.PARALLEL,
        ProcessingStrategy.BATCH
    ]
    
    for strategy in strategies:
        logger.info(f"✓ Estrategia disponible: {strategy.value}")


def test_excel_file_dataclass():
    """Prueba la clase ExcelFile."""
    logger.info("🧪 Probando clase ExcelFile...")
    
    # Crear archivo temporal para prueba
    test_path = Path("test_excel.xlsx")
    test_content = b"PK\x03\x04" + b"0" * 1000  # Simular contenido Excel (1KB)
    
    try:
        test_path.write_bytes(test_content)
        
        excel_file = ExcelFile(
            path=test_path,
            size_bytes=test_path.stat().st_size
        )
        
        logger.info(f"✓ ExcelFile creado:")
        logger.info(f"  - Archivo: {excel_file.path.name}")
        logger.info(f"  - Tamaño: {excel_file.size_bytes} bytes ({excel_file.size_mb:.3f} MB)")
        
        test_path.unlink()  # Limpiar
        
    except Exception as e:
        logger.error(f"❌ Error en prueba ExcelFile: {e}")


def test_batch_processor():
    """Prueba el procesador por lotes."""
    logger.info("🧪 Probando ExcelBatchProcessor...")
    
    # Crear procesador con configuración de prueba
    processor = ExcelBatchProcessor(
        output_base_dir=Path("data/test_output"),
        max_workers=2,
        chunk_size=5
    )
    
    logger.info(f"✓ ExcelBatchProcessor creado:")
    logger.info(f"  - Directorio salida: {processor.output_base_dir}")
    logger.info(f"  - Max workers: {processor.max_workers}")
    logger.info(f"  - Chunk size: {processor.chunk_size}")


def run_all_tests():
    """Ejecuta todas las pruebas."""
    logger.info("\n" + "="*60)
    logger.info("🧪 EJECUTANDO PRUEBAS DEL MÓDULO")
    logger.info("="*60 + "\n")
    
    tests = [
        test_excel_finder,
        test_processing_strategies,
        test_excel_file_dataclass,
        test_batch_processor
    ]
    
    for test in tests:
        try:
            test()
            logger.info("")
        except Exception as e:
            logger.error(f"❌ Error en prueba {test.__name__}: {e}")
    
    logger.info("="*60)
    logger.info("✅ PRUEBAS COMPLETADAS")
    logger.info("="*60)


if __name__ == "__main__":
    run_all_tests()
