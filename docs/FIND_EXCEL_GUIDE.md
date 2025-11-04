# Guía del Módulo find_excel_and_extract_sheets

## Descripción

El módulo `find_excel_and_extract_sheets` es una utilidad simplificada para la búsqueda automática y extracción masiva de hojas de archivos Excel.

**Versión 2.0** - Simplificado y optimizado para máxima facilidad de uso.

## Características Principales

### 🔍 Búsqueda Inteligente
- Búsqueda recursiva en directorios
- Filtrado por tamaño de archivo (mínimo/máximo)
- Exclusión de archivos por patrones
- Soporte para múltiples formatos Excel (.xlsx, .xls, .xlsm, .xlsb)

### ⚡ Procesamiento Simple
- **Secuencial**: Procesa archivos uno por uno (más seguro)
- **Paralelo**: Procesa múltiples archivos simultáneamente (más rápido)

### 📊 Monitoreo y Logging
- Logging detallado del progreso
- Estadísticas de rendimiento
- Manejo robusto de errores
- Informes de resumen automáticos

## Instalación

El módulo está integrado en el proyecto y usa las dependencias existentes:

```python
from find_excel_and_extract_sheets import find_and_extract_excel_sheets
```

## Uso Básico

### 1. Procesamiento Rápido (Una Línea)

```python
from find_excel_and_extract_sheets import find_and_extract_excel_sheets

# Buscar y procesar automáticamente
result = find_and_extract_excel_sheets("COMPUTADOR 1")

print(f"Procesados: {result['successful']}/{result['total_files']}")
print(f"Tiempo: {result['total_time']:.2f} segundos")
```

### 2. Escanear Directorio (Sin Procesar)

```python
from find_excel_and_extract_sheets import scan_directory

# Solo escanear, sin procesar
info = scan_directory("COMPUTADOR 1")

print(f"Archivos encontrados: {info['total_files']}")
print(f"Tamaño total: {info['total_size_mb']:.2f} MB")
for file in info['files']:
    print(f"  - {file['name']} ({file['size_mb']:.2f} MB)")
```

## Modos de Procesamiento

### Modo Paralelo (Por Defecto - Recomendado)

Procesa múltiples archivos simultáneamente. Más rápido para la mayoría de casos.

```python
result = find_and_extract_excel_sheets(
    search_directory="mi_directorio",
    parallel=True,        # Procesamiento paralelo (default)
    max_workers=4         # 4 archivos a la vez
)
```

### Modo Secuencial

Procesa archivos uno por uno. Más lento pero más estable para archivos muy grandes.

```python
result = find_and_extract_excel_sheets(
    search_directory="mi_directorio",
    parallel=False       # Procesamiento secuencial
)
```

## Configuración Avanzada

### Filtros de Archivos

```python
result = find_and_extract_excel_sheets(
    search_directory="mi_directorio",
    min_size_mb=0.01,          # Mínimo 10KB
    max_size_mb=50.0,          # Máximo 50MB
    exclude_patterns=[         # Excluir archivos que contengan:
        "temp",                # "temp" en nombre/ruta
        "backup",              # "backup" en nombre/ruta
        "~$",                  # Archivos temporales de Excel
    ],
    recursive=True             # Buscar en subdirectorios
)
```

### Directorio de Salida Personalizado

```python
result = find_and_extract_excel_sheets(
    search_directory="mi_directorio",
    output_directory="resultados/extracciones"  # Carpeta personalizada
)
```

### Parámetros de Extracción

```python
result = find_and_extract_excel_sheets(
    search_directory="mi_directorio",
    with_index=True,      # Añadir índice numérico (01_, 02_)
    clean_names=True      # Limpiar caracteres inválidos
)
```

## Uso Avanzado con ExcelProcessor

Para casos que requieran control total:

```python
from find_excel_and_extract_sheets import ExcelProcessor

# Crear procesador personalizado
processor = ExcelProcessor(
    output_base_dir="salida_personalizada/",
    min_size_mb=0.1,
    max_size_mb=100.0,
    exclude_patterns=['old', 'archive'],
    max_workers=6
)

# Buscar archivos
excel_files = processor.find_excel_files("mi_directorio", recursive=True)
print(f"Encontrados: {len(excel_files)} archivos")

# Ver detalles antes de procesar
for file in excel_files:
    print(f"{file['path'].name}: {file['size_mb']:.2f} MB")

# Procesar con control total
result = processor.process_files(
    excel_files,
    parallel=True,
    with_index=True,
    clean_names=True
)
```

## Estructura de Resultados

El resultado es un diccionario con la siguiente estructura:

```python
{
    "total_files": 10,           # Total de archivos procesados
    "successful": 9,             # Archivos procesados exitosamente
    "failed": 1,                 # Archivos que fallaron
    "success_rate": 90.0,        # Tasa de éxito (%)
    "total_time": 15.3,          # Tiempo total en segundos
    "results": [                 # Lista de resultados individuales
        {
            "excel_file": {...},      # Info del archivo
            "success": True,          # Si fue exitoso
            "output_dir": Path(...),  # Directorio de salida
            "files_created": [...],   # Archivos creados
            "processing_time": 1.5    # Tiempo de procesamiento
        },
        # ...
    ]
}
```

## Ejemplos Prácticos

### Ejemplo 1: Procesamiento Corporativo

```python
# Procesar informes mensuales con filtros
result = find_and_extract_excel_sheets(
    search_directory="informes_2024",
    output_directory="data/procesados",
    parallel=True,
    max_workers=4,
    exclude_patterns=['borrador', 'temp', 'old'],
    min_size_mb=0.05,
    max_size_mb=25.0,
    with_index=True
)

# Revisar resultados
print(f"\n📊 Resultados:")
print(f"✅ Exitosos: {result['successful']}")
print(f"❌ Fallidos: {result['failed']}")
print(f"⏱️  Tiempo: {result['total_time']:.1f}s")

# Ver archivos con error
if result['failed'] > 0:
    print(f"\n❌ Archivos con problemas:")
    for r in result['results']:
        if not r['success']:
            print(f"  - {r['excel_file']['path'].name}: {r.get('error')}")
```

### Ejemplo 2: Escaneo Previo

```python
# Primero escanear para ver qué hay
info = scan_directory("COMPUTADOR 1", recursive=True)

print(f"📁 Archivos encontrados: {info['total_files']}")
print(f"💾 Espacio total: {info['total_size_mb']:.1f} MB")

# Si hay archivos, procesar
if info['total_files'] > 0:
    result = find_and_extract_excel_sheets(
        "COMPUTADOR 1",
        parallel=True,
        max_workers=4
    )
```

### Ejemplo 3: Procesamiento Conservador

```python
# Para archivos delicados o grandes
result = find_and_extract_excel_sheets(
    search_directory="archivos_importantes",
    parallel=False,           # Secuencial para mayor estabilidad
    max_size_mb=200.0,       # Archivos grandes permitidos
    with_index=True,         # Mantener orden
    clean_names=True         # Normalizar nombres
)
```

## Rendimiento

### Recomendaciones

| Escenario | Modo | Max Workers | Notas |
|-----------|------|-------------|-------|
| Pocos archivos grandes (>10MB) | Secuencial | 1 | Más estable |
| Muchos archivos pequeños (<5MB) | Paralelo | 4-8 | Más rápido |
| Volumen mixto | Paralelo | 2-4 | Balanceado |
| Red lenta/problemas | Secuencial | 1 | Mejor debugging |

### Optimización

```python
import time

# Medir rendimiento
start = time.time()
result = find_and_extract_excel_sheets(
    "mi_directorio",
    parallel=True,
    max_workers=4
)
elapsed = time.time() - start

print(f"Tiempo: {elapsed:.2f}s")
print(f"Velocidad: {result['total_files'] / elapsed:.2f} archivos/s")
```

## Manejo de Errores

El módulo maneja automáticamente:

- ✅ Archivos corruptos (se registra y continúa)
- ✅ Permisos insuficientes (se omite y continúa)
- ✅ Archivos bloqueados (se registra como error)
- ✅ Directorio no existe (lanza FileNotFoundError)

```python
try:
    result = find_and_extract_excel_sheets("directorio_inexistente")
except FileNotFoundError as e:
    print(f"Error: {e}")

# Revisar archivos fallidos
result = find_and_extract_excel_sheets("mi_directorio")
if result['failed'] > 0:
    for r in result['results']:
        if not r['success']:
            print(f"Error: {r['excel_file']['path'].name}")
            print(f"  Razón: {r.get('error', 'Desconocido')}")
```

## Integración con Otros Módulos

```python
from find_excel_and_extract_sheets import find_and_extract_excel_sheets
from excel_handler import ExcelHandler
import pandas as pd

# Extraer hojas
result = find_and_extract_excel_sheets("datos/")

# Procesar cada hoja extraída
for r in result['results']:
    if r['success']:
        for file_name in r['files_created']:
            file_path = r['output_dir'] / file_name

            # Usar pandas
            df = pd.read_excel(file_path)
            print(f"{file_name}: {len(df)} filas")

            # O usar ExcelHandler
            handler = ExcelHandler(file_path)
            # ... procesar
```

## Logging

El módulo usa el sistema de logging del proyecto:

```python
from logger import setup_logger

# Ver logs detallados durante el procesamiento
logger = setup_logger("find_excel", level="DEBUG")

result = find_and_extract_excel_sheets("mi_directorio")
```

Los logs incluyen:
- 🔍 Búsqueda de archivos
- 📄 Procesamiento individual
- ✅/❌ Estado de cada archivo
- 📊 Resumen final
- ⚠️ Advertencias y errores

## Comparación con Versión Anterior

### Versión 1.0 (Anterior - Compleja)
- 4 archivos: models.py, finder.py, processor.py, utils.py
- 3 estrategias: Sequential, Parallel, Batch
- Dataclasses complejas
- Más código, más difícil de entender

### Versión 2.0 (Actual - Simplificada) ✅
- 1 archivo: core.py
- 2 modos: Sequential, Parallel
- Dicts simples
- Menos código, más fácil de usar

**Resultado:** Misma funcionalidad, 60% menos código, más fácil de mantener.

## Preguntas Frecuentes

### ¿Cuándo usar modo paralelo vs secuencial?

- **Paralelo**: Default, bueno para la mayoría de casos
- **Secuencial**: Archivos muy grandes (>50MB) o problemas de estabilidad

### ¿Cómo excluir archivos temporales?

```python
result = find_and_extract_excel_sheets(
    "directorio",
    exclude_patterns=["~$", ".tmp", "temp"]
)
```

### ¿Cómo limitar el tamaño de archivos?

```python
result = find_and_extract_excel_sheets(
    "directorio",
    min_size_mb=0.01,   # Mínimo 10KB
    max_size_mb=50.0    # Máximo 50MB
)
```

### ¿Los resultados incluyen imágenes/formatos?

No, solo se extrae la **data** (valores de celdas). No se copian:
- Imágenes
- Gráficos
- Estilos avanzados
- Macros/VBA

Para preservar formato, usar `openpyxl` directamente.
