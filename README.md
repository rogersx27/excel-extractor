# Excel Extractor

Sistema avanzado de procesamiento y consolidación de archivos Excel con capacidad de detección inteligente de estructuras complejas.

## Descripción del Proyecto

**Excel Extractor** es un proyecto Python especializado en la **manipulación avanzada de archivos Excel y procesamiento de datos**. Está diseñado específicamente para manejar archivos Excel con múltiples hojas, tablas anidadas y estructuras complejas, proporcionando un pipeline completo desde la extracción hasta la consolidación de datos.

### Características Principales

- **Extracción Automática**: Descubre y extrae hojas de Excel de forma recursiva
- **Detección de Estructuras**: Identifica automáticamente estructuras simples, complejas y con patrones FECHA
- **Consolidación Inteligente**: Consolida múltiples tablas apiladas en archivos únicos normalizados
- **Procesamiento en Paralelo**: Soporte para procesamiento paralelo de grandes volúmenes de archivos
- **Registro Detallado**: Sistema de logging con rotación diaria y salida coloreada
- **Manejo Robusto de Errores**: Jerarquía de excepciones personalizadas y degradación elegante

## Arquitectura del Sistema

El proyecto está organizado en **4 subsistemas principales**:

### 1. Excel Handler (`src/excel_handler/`)
Biblioteca completa de manipulación de Excel con dos APIs:

- **QuickExcel** (`quick.py`): Operaciones sin estado para tareas simples
  - Lectura rápida de archivos Excel (una o todas las hojas)
  - Escritura de DataFrames a Excel
  - Creación de archivos con formato (auto-filtro, paneles congelados)
  - Exportación multi-hoja

- **ExcelHandler** (`handler.py`): Operaciones con estado para manipulaciones complejas
  - Soporte de context manager para gestión de recursos
  - Carga diferida (lazy loading) de libros de trabajo
  - Agregar/eliminar/renombrar hojas
  - Extracción de rangos específicos de datos
  - Manipulación multi-hoja

- **Utilidades** (`utils.py`):
  - `merge_excel_files()`: Combina múltiples archivos Excel
  - `split_excel_by_column()`: Divide Excel por valores de columna
  - `compare_excel_files()`: Compara dos archivos Excel

### 2. Excel Extractor (`src/excel_extractor/`)
Divide archivos Excel multi-hoja en archivos individuales:

- **ExcelSheetExtractor** (`extractor.py`): Clase principal de extracción
  - Extrae todas o hojas específicas de archivos Excel
  - Crea un archivo por hoja con indexación numérica opcional
  - Sanitiza nombres de archivo y maneja casos extremos
  - Proporciona metadatos detallados de extracción

### 3. Excel Consolidator (`src/excel_consolidator/`)
El módulo más sofisticado - consolida archivos Excel extraídos con estructuras complejas:

- **Detector de Estructuras** (`detector.py`):
  - Identifica tipos de estructura: SIMPLE, COMPLEX, COMPLEX_FECHA
  - Detecta filas de encabezado y rangos de datos
  - Detección especial de patrones para bloques "FECHA:"
  - Analiza estructura completa del archivo

- **Extractor de Datos** (`extractor.py`):
  - Extrae datos de estructuras simples (tabla única)
  - Extrae datos de estructuras complejas (múltiples tablas apiladas)
  - Manejo especial de estructuras con patrón FECHA
  - Limpieza y normalización de datos extraídos

- **Consolidador** (`consolidator.py`):
  - Clase principal para consolidar archivos individuales
  - Procesa directorios de archivos extraídos
  - Soporte de context manager
  - Estadísticas detalladas de procesamiento

- **Consolidador por Lotes** (`batch.py`):
  - Procesamiento por lotes paralelo y secuencial
  - Procesa árboles completos de directorios
  - Seguimiento de progreso y manejo de errores

### 4. Excel Finder & Processor (`src/find_excel_and_extract_sheets/`)
Descubrimiento y procesamiento automatizado de archivos Excel:

- **ExcelProcessor** (`core.py`):
  - Escaneo recursivo de directorios para archivos Excel
  - Modos de procesamiento paralelo/secuencial
  - Filtrado por tamaño de archivo (mín/máx)
  - Exclusión basada en patrones
  - Extracción por lotes con seguimiento de progreso

## Scripts CLI

El proyecto incluye tres scripts CLI principales en el directorio raíz:

### 1. `process_excel_directory.py`
Encuentra y extrae hojas de archivos Excel en un directorio.

```bash
# Uso básico
python process_excel_directory.py "COMPUTADOR 1"

# Con procesamiento paralelo
python process_excel_directory.py "data/" --parallel --workers 8

# Con exclusiones
python process_excel_directory.py "files/" --exclude "temp" "backup"

# Con filtro de tamaño
python process_excel_directory.py "data/" --min-size 100 --max-size 10000
```

**Opciones**:
- `--parallel`: Procesamiento paralelo
- `--workers N`: Número de trabajadores (por defecto: 4)
- `--exclude`: Patrones a excluir
- `--min-size / --max-size`: Filtro de tamaño en KB

### 2. `consolidate_excel.py`
Consolida archivos Excel individuales con estructuras complejas.

```bash
# Consolidar un archivo
python consolidate_excel.py archivo.xlsx

# Consolidar directorio
python consolidate_excel.py directorio/ --recursive

# Solo analizar estructura (sin consolidar)
python consolidate_excel.py archivo.xlsx --analyze-only

# Especificar salida
python consolidate_excel.py archivo.xlsx --output salida.xlsx
```

**Opciones**:
- `--recursive / -r`: Procesar subdirectorios
- `--analyze-only`: Solo analizar, no consolidar
- `--output / -o`: Ruta de archivo de salida

### 3. `batch_consolidate_excel.py`
Consolidación por lotes con procesamiento paralelo.

```bash
# Consolidación por lotes
python batch_consolidate_excel.py "data/extraido/"

# Con procesamiento paralelo
python batch_consolidate_excel.py "data/" --parallel --workers 8

# Modo dry-run (prueba sin ejecutar)
python batch_consolidate_excel.py "data/" --dry-run
```

**Opciones**:
- `--parallel`: Habilitar procesamiento paralelo
- `--workers N`: Número de trabajadores
- `--dry-run`: Simular sin consolidar

## Flujo de Trabajo

El proyecto implementa un **pipeline de tres etapas**:

### Etapa 1: Descubrimiento y Extracción
```
Directorio → Encontrar Excel → Extraer Hojas → Archivos Individuales
```
**Script**: `process_excel_directory.py`

### Etapa 2: Análisis de Estructura
```
Archivo Extraído → Detectar Estructura → Identificar Tablas/Encabezados
```
**Módulo**: `excel_consolidator.detector`

### Etapa 3: Consolidación
```
Estructura Compleja → Extraer Tablas → Consolidar → Archivo Limpio
```
**Scripts**: `consolidate_excel.py`, `batch_consolidate_excel.py`

## Tipos de Estructuras Detectadas

El sistema puede identificar y procesar tres tipos de estructuras:

### 1. SIMPLE
- Una tabla con un encabezado
- Datos contiguos bajo el encabezado
- Estructura más común

### 2. COMPLEX
- Múltiples tablas apiladas verticalmente
- Cada tabla tiene su propio encabezado repetido
- Datos no contiguos entre tablas

### 3. COMPLEX_FECHA
- Múltiples bloques de datos marcados con "FECHA:"
- Cada bloque representa datos para una fecha específica
- Requiere procesamiento especial para extraer fechas

## Instalación y Configuración

### 1. Crear y Activar Entorno Virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar Dependencias

```bash
# Instalar dependencias de producción
pip install -r requirements.txt
```

### 3. Configurar Variables de Entorno (Opcional)

Crear archivo `.env` en el directorio raíz:

```env
DEBUG=False
LOG_LEVEL=INFO
```

## Librerías Excel Incluidas

El proyecto incluye múltiples librerías Excel, cada una optimizada para casos específicos:

- **pandas** (≥2.2.0): Análisis de datos y operaciones básicas de E/S
- **openpyxl** (≥3.1.2): Manipulación completa de .xlsx con estilos y formato
- **xlsxwriter** (≥3.2.0): Creación de archivos Excel con formato profesional
- **xlrd** (≥2.0.1): Lectura de formato .xls antiguo (Excel 97-2003)
- **xlwt** (≥1.3.0): Escritura de archivos .xls
- **pyxlsb** (≥1.0.10): Lectura de archivos binarios .xlsb
- **python-calamine** (≥0.2.0): Lectura ultra-rápida para archivos grandes

### Guía de Selección:
- Análisis de datos → usar **pandas**
- Preservar/modificar formato → usar **openpyxl**
- Crear reportes con formato → usar **xlsxwriter**
- Lectura de archivos grandes → usar **python-calamine**
- Archivos .xls antiguos → usar **xlrd/xlwt**

## Estructura del Proyecto

```
ExcelExtractor/
├── src/
│   ├── excel_handler/              # Manipulación general de Excel
│   │   ├── handler.py              # Clase ExcelHandler
│   │   ├── quick.py                # Utilidades QuickExcel
│   │   ├── utils.py                # Funciones helper
│   │   └── exceptions.py           # Excepciones personalizadas
│   ├── excel_extractor/            # Extracción de hojas
│   │   ├── extractor.py            # ExcelSheetExtractor
│   │   └── utils.py                # Utilidades
│   ├── excel_consolidator/         # Consolidación de datos
│   │   ├── consolidator.py         # Consolidador principal
│   │   ├── batch.py                # Procesamiento por lotes
│   │   ├── detector.py             # Detección de estructura
│   │   ├── extractor.py            # Extracción de datos
│   │   └── utils.py                # Funciones helper
│   ├── find_excel_and_extract_sheets/  # Descubrimiento de archivos
│   │   └── core.py                 # ExcelProcessor
│   ├── logger/                     # Sistema de logging
│   │   └── logging_config.py       # Configuración de logger
│   ├── config.py                   # Configuración
│   └── main.py                     # Punto de entrada
├── tests/                          # Tests unitarios
├── docs/                           # Documentación
│   ├── EXCEL_HANDLER.md
│   ├── EXCEL_EXTRACTOR_GUIDE.md
│   ├── FIND_EXCEL_GUIDE.md
│   └── LOGGING_GUIDE.md
├── examples/                       # Scripts de ejemplo
├── scripts/                        # Scripts auxiliares
├── data/                           # Archivos de datos (runtime)
├── logs/                           # Archivos de log (runtime)
├── process_excel_directory.py     # CLI: Buscar y extraer
├── consolidate_excel.py           # CLI: Consolidar
├── batch_consolidate_excel.py     # CLI: Consolidación por lotes
├── requirements.txt               # Dependencias
├── pyproject.toml                # Configuración del proyecto
├── CLAUDE.md                      # Instrucciones para Claude Code
└── README.md                      # Este archivo
```

## Desarrollo

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Con reporte de cobertura
pytest --cov=src --cov-report=html

# Ver reporte de cobertura
# Abrir htmlcov/index.html en el navegador
```

### Formatear Código

```bash
# Formatear con black
black src/ tests/

# Ordenar imports
isort src/ tests/

# Verificar estilo con flake8
flake8 src/ tests/

# Análisis estático con pylint
pylint src/

# Type checking con mypy
mypy src/
```

## Herramientas de Calidad

El proyecto incluye configuración completa de herramientas de calidad en `pyproject.toml`:

- **black**: Formateador de código (line-length: 88)
- **isort**: Ordenador de imports (compatible con black)
- **pytest**: Framework de testing con cobertura
- **mypy**: Type checker estático
- **pylint**: Análisis estático de código
- **flake8**: Verificador de estilo

## Sistema de Logging

El proyecto incluye un sistema de logging avanzado con:

- **Rotación Diaria**: Archivos de log separados por fecha (YYYY-MM-DD.log)
- **Salida Coloreada**: Usando `colorlog` para mejor legibilidad en consola
- **Loggers por Módulo**: Cada módulo puede tener logging personalizado
- **Decorador de Funciones**: `@log_function_call` para logging automático

Los logs se almacenan en el directorio `logs/` con formato:
```
logs/
├── 2025-01-15.log
├── 2025-01-16.log
└── 2025-01-17.log
```

## Casos de Uso

Este proyecto está diseñado para:

1. **Proyectos de Migración de Datos**: Extraer y consolidar datos de archivos Excel heredados
2. **Procesamiento de Reportes**: Manejar reportes Excel complejos con múltiples tablas
3. **Normalización de Datos**: Convertir archivos Excel desordenados en datos estructurados limpios
4. **Procesamiento por Lotes**: Procesar cientos de archivos Excel automáticamente
5. **Pipelines ETL**: Primera etapa de extracción de datos desde fuentes Excel

## Características Únicas

### Detección de Estructuras Complejas
El consolidador puede detectar y manejar:
- Tablas simples (un encabezado, un bloque de datos)
- Tablas complejas (múltiples tablas apiladas con encabezados repetidos)
- Estructuras con patrón FECHA (bloques marcados con etiquetas "FECHA:")

### Extracción Inteligente de Datos
- Identifica automáticamente filas de encabezado
- Maneja rangos de datos no contiguos
- Preserva integridad de datos a través de múltiples tablas
- Normaliza nombres de columnas

### Procesamiento Paralelo
- ThreadPoolExecutor para operaciones I/O-bound
- Conteo de trabajadores configurable
- Seguimiento de progreso entre hilos

### Manejo Robusto de Errores
- Jerarquía de excepciones personalizadas
- Mensajes de error detallados
- Degradación elegante
- Logging comprehensivo

## Documentación Adicional

Para más información, consulta los siguientes documentos en el directorio `docs/`:

- **EXCEL_HANDLER.md**: Guía completa del módulo Excel Handler
- **EXCEL_EXTRACTOR_GUIDE.md**: Documentación del extractor de hojas
- **FIND_EXCEL_GUIDE.md**: Guía del procesador de descubrimiento
- **LOGGING_GUIDE.md**: Sistema de logging y configuración

## Ejemplos

El directorio `examples/` contiene scripts de ejemplo que demuestran el uso de cada módulo:

- `excel_examples.py`: Ejemplos de manipulación básica de Excel
- `extract_excel_sheets.py`: Ejemplos de extracción de hojas
- `find_excel_example.py`: Ejemplos de descubrimiento de archivos
- `logging_example.py`: Ejemplos de uso del sistema de logging

