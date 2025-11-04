# Guía del Extractor de Hojas Excel

Módulo para extraer hojas individuales de archivos Excel a archivos separados.

## Descripción

El módulo `excel_extractor` permite dividir un archivo Excel con múltiples hojas en archivos Excel individuales, uno por cada hoja. Es útil para:

- Dividir archivos Excel grandes en partes más manejables
- Distribuir hojas específicas a diferentes personas/equipos
- Procesar hojas de forma independiente
- Organizar datos por hoja

## Instalación de Dependencias

Las dependencias ya están en `requirements.txt`:
```bash
pip install pandas openpyxl
```

## Uso desde Línea de Comandos

### Uso básico

```bash
python src/extract_excel_sheets.py "archivo.xlsx"
```

Esto creará una carpeta `data/archivo/` con archivos:
- `01_Hoja1.xlsx`
- `02_Hoja2.xlsx`
- `03_Hoja3.xlsx`

### Opciones avanzadas

```bash
# Especificar directorio de salida
python src/extract_excel_sheets.py "archivo.xlsx" --output "resultados/"

# Extraer solo hojas específicas
python src/extract_excel_sheets.py "archivo.xlsx" --sheets "Ventas" "Clientes"

# Sin índice numérico en nombres de archivo
python src/extract_excel_sheets.py "archivo.xlsx" --no-index

# Modo verbose (más información)
python src/extract_excel_sheets.py "archivo.xlsx" -v
```

### Ayuda

```bash
python src/extract_excel_sheets.py --help
```

## Uso Programático (desde Python)

### Método 1: Función helper (simple)

```python
from excel_extractor import extract_excel_sheets
from pathlib import Path

# Extraer todas las hojas
result = extract_excel_sheets(Path("archivo.xlsx"))

print(f"Procesadas {result['total_sheets']} hojas")
print(f"Archivos en: {result['output_dir']}")
```

### Método 2: Clase ExcelSheetExtractor (control total)

```python
from excel_extractor import ExcelSheetExtractor
from pathlib import Path

# Crear extractor
extractor = ExcelSheetExtractor(
    excel_file=Path("archivo.xlsx"),
    output_base_dir=Path("resultados/")
)

# Ver hojas disponibles
sheet_names = extractor.get_sheet_names()
print(f"Hojas: {sheet_names}")

# Extraer todas las hojas
result = extractor.extract_all_sheets(
    with_index=True,      # Agregar índice numérico
    clean_names=True      # Limpiar caracteres inválidos
)

# Extraer solo hojas específicas
result = extractor.extract_specific_sheets(
    sheet_names=["Ventas", "Clientes"],
    with_index=True
)
```

## Ejemplos Completos

### Ejemplo 1: Extraer y procesar cada hoja

```python
from excel_extractor import ExcelSheetExtractor
from pathlib import Path
import pandas as pd

# Extraer hojas
extractor = ExcelSheetExtractor(Path("ventas.xlsx"))
result = extractor.extract_all_sheets()

# Procesar cada archivo generado
for file_name in result['files_created']:
    file_path = result['output_dir'] / file_name
    df = pd.read_excel(file_path)
    print(f"{file_name}: {len(df)} filas")
```

### Ejemplo 2: Extraer solo hojas con datos

```python
from excel_extractor import ExcelSheetExtractor
from pathlib import Path

extractor = ExcelSheetExtractor(Path("archivo.xlsx"))

# Cargar hojas
extractor.load_sheets()

# Filtrar hojas con datos
sheets_with_data = [
    name for name, df in extractor.sheets_data.items()
    if not df.empty
]

# Extraer solo las que tienen datos
result = extractor.extract_specific_sheets(sheets_with_data)
```

### Ejemplo 3: Personalizar nombres de archivo

```python
from excel_extractor import ExcelSheetExtractor
from pathlib import Path

extractor = ExcelSheetExtractor(Path("archivo.xlsx"))

# Sin índice, sin limpieza de nombres
result = extractor.extract_all_sheets(
    with_index=False,
    clean_names=False
)

# Con índice, con limpieza
result = extractor.extract_all_sheets(
    with_index=True,
    clean_names=True
)
```

### Ejemplo 4: Automatizar para múltiples archivos

```python
from excel_extractor import extract_excel_sheets
from pathlib import Path

# Procesar todos los Excel en una carpeta
excel_files = Path("datos/").glob("*.xlsx")

for excel_file in excel_files:
    print(f"\nProcesando: {excel_file.name}")
    try:
        result = extract_excel_sheets(excel_file)
        print(f"✓ {result['total_sheets']} hojas extraídas")
    except Exception as e:
        print(f"✗ Error: {e}")
```

## Características

### ✅ Lo que hace
- Extrae todas las hojas de un Excel
- Preserva data completa (valores, encabezados, estructura)
- Limpia nombres de archivo inválidos automáticamente
- Crea carpeta con nombre del archivo original
- Nomenclatura ordenada con índices (01_, 02_, etc.)
- Logging detallado del proceso
- Manejo robusto de errores

### ⚠️ Lo que NO hace
- **No copia imágenes** (solo data)
- **No copia estilos avanzados** (colores, fuentes, bordes)
- **No copia gráficos** (solo tablas de datos)
- **No copia fórmulas** (copia valores resultantes)
- **No copia macros/VBA**

Si necesitas preservar formato, usa `openpyxl` directamente.

## Formato de Salida

### Estructura de carpetas

```
data/
└── nombre_archivo/
    ├── 01_Hoja1.xlsx
    ├── 02_Hoja2.xlsx
    ├── 03_Hoja3.xlsx
    └── ...
```

### Nomenclatura

Por defecto:
- `01_NombreHoja.xlsx` - Con índice (recomendado)
- `NombreHoja.xlsx` - Sin índice (con `--no-index`)

Caracteres inválidos (`< > : " / \ | ? *`) se reemplazan con `_`

## API Reference

### `extract_excel_sheets()`

```python
def extract_excel_sheets(
    excel_file: Path,
    output_base_dir: Optional[Path] = None,
    sheet_names: Optional[List[str]] = None,
    with_index: bool = True,
    clean_names: bool = True
) -> Dict
```

**Parámetros:**
- `excel_file`: Ruta al archivo Excel
- `output_base_dir`: Directorio base de salida (default: `data/`)
- `sheet_names`: Lista de hojas a extraer (None = todas)
- `with_index`: Añadir índice numérico
- `clean_names`: Limpiar caracteres inválidos

**Retorna:**
```python
{
    'total_sheets': int,           # Número de hojas procesadas
    'output_dir': Path,            # Directorio de salida
    'files_created': List[str]     # Lista de archivos creados
}
```

### Clase `ExcelSheetExtractor`

#### Métodos principales

```python
# Constructor
ExcelSheetExtractor(excel_file: Path, output_base_dir: Optional[Path] = None)

# Cargar hojas
load_sheets() -> Dict[str, pd.DataFrame]

# Obtener nombres de hojas
get_sheet_names() -> List[str]

# Extraer todas las hojas
extract_all_sheets(with_index: bool = True, clean_names: bool = True) -> Dict

# Extraer hojas específicas
extract_specific_sheets(
    sheet_names: List[str],
    with_index: bool = True,
    clean_names: bool = True
) -> Dict
```

## Logging

El módulo usa el sistema de logging del proyecto. Los logs se guardan en:
- Consola: con colores
- Archivo: `logs/YYYY-MM-DD.log`

Niveles de log:
- `INFO`: Progreso del proceso
- `WARNING`: Hojas vacías u otros avisos
- `ERROR`: Errores durante el proceso

## Manejo de Errores

```python
from excel_extractor import extract_excel_sheets
from pathlib import Path

try:
    result = extract_excel_sheets(Path("archivo.xlsx"))
except FileNotFoundError:
    print("Archivo no encontrado")
except ValueError:
    print("Archivo no es un Excel válido")
except Exception as e:
    print(f"Error: {e}")
```

## Solución de Problemas

### Error: "Archivo no encontrado"

Verifica la ruta del archivo:
```python
from pathlib import Path
archivo = Path("datos/archivo.xlsx")
print(archivo.exists())  # Debe ser True
```

### Error: "Archivo no es un Excel válido"

Solo se aceptan: `.xlsx`, `.xls`, `.xlsm`, `.xlsb`

### Hojas vacías

El módulo procesa hojas vacías pero muestra un warning:
```
⚠️  La hoja 'HojaVacia' está vacía
```

### Nombres de archivo muy largos

Los nombres se truncan automáticamente si son muy largos.

## Consejos

1. **Verificar hojas primero**: Usa `get_sheet_names()` para ver qué hojas hay antes de extraer

2. **Procesar selectivamente**: Si solo necesitas algunas hojas, usa `sheet_names` para ser más eficiente

3. **Verificar data**: Revisa que las hojas tengan datos antes de procesar

4. **Usar with_index**: Mantiene el orden original de las hojas

5. **Logs**: Revisa los logs para ver detalles del proceso

## Integración con otros módulos

### Con excel_handler

```python
from excel_extractor import extract_excel_sheets
from excel_handler import ExcelHandler
from pathlib import Path

# Extraer hojas
result = extract_excel_sheets(Path("original.xlsx"))

# Procesar cada hoja extraída
for file_name in result['files_created']:
    file_path = result['output_dir'] / file_name
    handler = ExcelHandler(file_path)
    # ... procesar con excel_handler
```

### Con pandas

```python
from excel_extractor import ExcelSheetExtractor
import pandas as pd

extractor = ExcelSheetExtractor(Path("datos.xlsx"))
extractor.load_sheets()

# Acceder directamente a los DataFrames
for sheet_name, df in extractor.sheets_data.items():
    # Análisis con pandas
    print(f"{sheet_name}: {df.describe()}")
```
