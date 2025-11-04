# Excel Handler - Documentación y Referencia de API

## Tabla de Contenidos

- [Introducción](#introducción)
- [Instalación](#instalación)
- [Arquitectura](#arquitectura)
- [Guía Rápida](#guía-rápida)
- [Referencia de API](#referencia-de-api)
  - [QuickExcel](#quickexcel)
  - [ExcelHandler](#excelhandler)
  - [Utilidades](#utilidades)
- [Excepciones](#excepciones)
- [Mejores Prácticas](#mejores-prácticas)

---

## Introducción

`excel_handler` es un módulo Python para manipulación avanzada de archivos Excel con una API limpia, segura y fácil de usar.

### Características

- **Dos APIs especializadas**: QuickExcel (operaciones simples) y ExcelHandler (manipulación avanzada)
- **Context managers**: Gestión automática de recursos para prevenir memory leaks
- **Lazy loading**: Carga automática de archivos bajo demanda
- **Validaciones robustas**: Excepciones personalizadas con mensajes descriptivos
- **Type hints completos**: Soporte para IDEs y type checkers
- **Logging integrado**: Sistema de logging con archivos por fecha y colores en consola
- **Utilidades batch**: Combinar, dividir y comparar múltiples archivos

### Formatos Soportados

- `.xlsx` - Excel 2007+ (formato principal)
- `.xlsm` - Excel con macros
- `.xltx` - Plantillas Excel
- `.xltm` - Plantillas Excel con macros

---

## Instalación

```bash
# Dependencias requeridas
pip install pandas openpyxl xlsxwriter

# El módulo está en src/excel_handler/
```

---

## Arquitectura

```
excel_handler/
├── __init__.py          # API pública y exports
├── quick.py             # QuickExcel - Operaciones rápidas sin estado
├── handler.py           # ExcelHandler - Manipulación avanzada con estado
├── utils.py             # Utilidades: merge, split, compare
└── exceptions.py        # Excepciones personalizadas del dominio
```

### Decisión de API: ¿QuickExcel o ExcelHandler?

| Caso de Uso | API Recomendada |
|-------------|----------------|
| Leer un Excel rápidamente | **QuickExcel** |
| Escribir un DataFrame | **QuickExcel** |
| Crear archivo formateado | **QuickExcel** |
| Múltiples hojas (escritura única) | **QuickExcel** |
| Manipular hojas existentes | **ExcelHandler** |
| Múltiples operaciones en mismo archivo | **ExcelHandler** |
| Extraer rangos específicos | **ExcelHandler** |
| Modificar estructura de hojas | **ExcelHandler** |

---

## Guía Rápida

### Leer y Escribir (QuickExcel)

```python
from excel_handler import QuickExcel
import pandas as pd

# Leer Excel
df = QuickExcel.read('datos.xlsx')
df = QuickExcel.read('datos.xlsx', sheet='Ventas')

# Leer todas las hojas
sheets = QuickExcel.read_all_sheets('reporte.xlsx')

# Escribir DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
QuickExcel.write(df, 'salida.xlsx', sheet_name='Datos')

# Múltiples hojas
data = {'Ventas': df_ventas, 'Gastos': df_gastos}
QuickExcel.write_multiple_sheets(data, 'finanzas.xlsx')

# Con formato profesional
QuickExcel.create_formatted(df, 'reporte.xlsx', auto_filter=True, freeze_panes=True)
```

### Manipulación Avanzada (ExcelHandler)

```python
from excel_handler import ExcelHandler
import pandas as pd

# Context manager (SIEMPRE recomendado)
with ExcelHandler('reporte.xlsx') as excel:
    # Listar hojas
    print(excel.sheet_names)

    # Agregar hojas
    excel.add_sheet('Resumen', df_resumen)
    excel.add_sheet('Detalle', df_detalle)

    # Renombrar
    excel.rename_sheet('Sheet1', 'Principal')

    # Eliminar
    if excel.sheet_exists('Temporal'):
        excel.delete_sheet('Temporal')

    # Extraer datos
    df = excel.extract_sheet_to_dataframe('Ventas')
    rango = excel.extract_range('Principal', 1, 1, 10, 5)

    # Guardar
    excel.save()
# Auto-close garantizado
```

### Utilidades

```python
from excel_handler import merge_excel_files, split_excel_by_column, compare_excel_files

# Combinar archivos
archivos = ['enero.xlsx', 'febrero.xlsx', 'marzo.xlsx']
df_combined = merge_excel_files(archivos, 'trimestre.xlsx')

# Dividir por columna
split_excel_by_column('ventas.xlsx', column_name='Región', output_dir='por_region/')

# Comparar archivos
diff = compare_excel_files('v1.xlsx', 'v2.xlsx')
print(f"¿Iguales? {diff['are_equal']}")
```

---

## Referencia de API

### QuickExcel

Clase con métodos estáticos para operaciones rápidas de una línea.

#### `QuickExcel.read()`

Lee un archivo Excel y retorna un DataFrame.

```python
@staticmethod
def read(
    file_path: Union[str, Path],
    sheet: Optional[Union[str, int]] = 0,
    **kwargs
) -> pd.DataFrame
```

**Parámetros:**
- `file_path` (str | Path): Ruta al archivo Excel
- `sheet` (str | int, opcional): Nombre o índice de hoja (default: 0 = primera hoja)
- `**kwargs`: Argumentos adicionales para `pd.read_excel` (usecols, skiprows, nrows, etc.)

**Retorna:** `pd.DataFrame` con los datos

**Excepciones:**
- `FileNotFoundError`: Si el archivo no existe
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
# Leer primera hoja
df = QuickExcel.read('datos.xlsx')

# Leer hoja específica por nombre
df = QuickExcel.read('datos.xlsx', sheet='Ventas')

# Leer hoja por índice
df = QuickExcel.read('datos.xlsx', sheet=1)

# Con opciones adicionales
df = QuickExcel.read('datos.xlsx', sheet='Ventas', skiprows=2, usecols='A:D')
```

---

#### `QuickExcel.read_all_sheets()`

Lee todas las hojas de un Excel en un diccionario.

```python
@staticmethod
def read_all_sheets(file_path: Union[str, Path]) -> Dict[str, pd.DataFrame]
```

**Parámetros:**
- `file_path` (str | Path): Ruta al archivo Excel

**Retorna:** `Dict[str, DataFrame]` - Diccionario con {nombre_hoja: DataFrame}

**Excepciones:**
- `FileNotFoundError`: Si el archivo no existe
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
sheets = QuickExcel.read_all_sheets('reporte.xlsx')

for name, df in sheets.items():
    print(f"Hoja: {name}")
    print(f"Dimensiones: {df.shape}")
    print(f"Columnas: {list(df.columns)}\n")
```

---

#### `QuickExcel.write()`

Escribe un DataFrame a un archivo Excel.

```python
@staticmethod
def write(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    sheet_name: str = 'Sheet1',
    index: bool = False,
    **kwargs
)
```

**Parámetros:**
- `df` (DataFrame): DataFrame a escribir
- `file_path` (str | Path): Ruta del archivo de salida
- `sheet_name` (str, opcional): Nombre de la hoja (default: 'Sheet1')
- `index` (bool, opcional): Incluir índice del DataFrame (default: False)
- `**kwargs`: Argumentos adicionales para `df.to_excel`

**Excepciones:**
- `EmptyDataError`: Si el DataFrame está vacío o es None
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Escritura básica
QuickExcel.write(df, 'salida.xlsx')

# Con nombre de hoja personalizado
QuickExcel.write(df, 'salida.xlsx', sheet_name='Datos')

# Con índice
QuickExcel.write(df, 'salida.xlsx', sheet_name='Datos', index=True)
```

---

#### `QuickExcel.write_multiple_sheets()`

Escribe múltiples DataFrames en diferentes hojas de un mismo archivo.

```python
@staticmethod
def write_multiple_sheets(
    data: Dict[str, pd.DataFrame],
    file_path: Union[str, Path],
    index: bool = False
)
```

**Parámetros:**
- `data` (dict): Diccionario {nombre_hoja: DataFrame}
- `file_path` (str | Path): Ruta del archivo de salida
- `index` (bool, opcional): Incluir índice (default: False)

**Excepciones:**
- `EmptyDataError`: Si el diccionario está vacío
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
data = {
    'Ventas': df_ventas,
    'Clientes': df_clientes,
    'Productos': df_productos
}

QuickExcel.write_multiple_sheets(data, 'reporte_completo.xlsx')
```

---

#### `QuickExcel.create_formatted()`

Crea un Excel con formato profesional (encabezados estilizados, columnas ajustadas, filtros).

```python
@staticmethod
def create_formatted(
    df: pd.DataFrame,
    file_path: Union[str, Path],
    sheet_name: str = 'Sheet1',
    auto_filter: bool = True,
    freeze_panes: bool = True,
    header_bg_color: str = '#4472C4'
)
```

**Parámetros:**
- `df` (DataFrame): DataFrame a escribir
- `file_path` (str | Path): Ruta del archivo de salida
- `sheet_name` (str, opcional): Nombre de la hoja (default: 'Sheet1')
- `auto_filter` (bool, opcional): Activar filtros (default: True)
- `freeze_panes` (bool, opcional): Congelar primera fila (default: True)
- `header_bg_color` (str, opcional): Color de fondo encabezados (default: '#4472C4' azul)

**Excepciones:**
- `EmptyDataError`: Si el DataFrame está vacío
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
df = pd.DataFrame({
    'Empleado': ['Ana', 'Luis', 'María'],
    'Departamento': ['IT', 'Ventas', 'IT'],
    'Salario': [50000, 45000, 52000]
})

QuickExcel.create_formatted(
    df,
    'reporte_salarios.xlsx',
    sheet_name='Salarios 2024',
    auto_filter=True,
    freeze_panes=True,
    header_bg_color='#2E75B6'  # Azul personalizado
)
```

---

### ExcelHandler

Clase para manipulación avanzada con gestión de estado. **Usar siempre con context manager**.

#### Constructor

```python
def __init__(
    file_path: Union[str, Path],
    validate: bool = True
)
```

**Parámetros:**
- `file_path` (str | Path): Ruta al archivo Excel (existente o nuevo)
- `validate` (bool, opcional): Validar extensión (default: True)

**Excepciones:**
- `InvalidFileFormatError`: Si la extensión no es válida

**Ejemplo:**
```python
# Uso con context manager (RECOMENDADO)
with ExcelHandler('datos.xlsx') as excel:
    excel.add_sheet('Nueva')
    excel.save()

# Uso manual (NO RECOMENDADO)
excel = ExcelHandler('datos.xlsx')
excel.add_sheet('Nueva')
excel.save()
excel.close()  # No olvidar
```

---

#### Propiedades

##### `sheet_names`

Lista los nombres de todas las hojas del archivo.

```python
@property
def sheet_names() -> List[str]
```

**Retorna:** `List[str]` - Lista de nombres de hojas

**Ejemplo:**
```python
with ExcelHandler('reporte.xlsx') as excel:
    print(f"Hojas disponibles: {excel.sheet_names}")
    # Output: ['Ventas', 'Clientes', 'Productos']
```

---

##### `wb`

Acceso al workbook de openpyxl con lazy loading automático.

```python
@property
def wb() -> Workbook
```

**Retorna:** `Workbook` de openpyxl

**Nota:** La carga se realiza automáticamente en el primer acceso.

---

#### Métodos

##### `sheet_exists()`

Verifica si una hoja existe en el workbook.

```python
def sheet_exists(sheet_name: str) -> bool
```

**Parámetros:**
- `sheet_name` (str): Nombre de la hoja a verificar

**Retorna:** `bool` - True si existe, False en caso contrario

**Ejemplo:**
```python
with ExcelHandler('datos.xlsx') as excel:
    if excel.sheet_exists('Temporal'):
        print("La hoja temporal existe")
        excel.delete_sheet('Temporal')
```

---

##### `add_sheet()`

Añade una nueva hoja al Excel.

```python
def add_sheet(
    sheet_name: str,
    data: Optional[pd.DataFrame] = None,
    index: int = None,
    overwrite: bool = False
)
```

**Parámetros:**
- `sheet_name` (str): Nombre de la nueva hoja
- `data` (DataFrame, opcional): DataFrame con datos para la hoja
- `index` (int, opcional): Posición donde insertar (None = al final)
- `overwrite` (bool, opcional): Sobrescribir si existe (default: False)

**Excepciones:**
- `SheetAlreadyExistsError`: Si la hoja existe y overwrite=False

**Ejemplo:**
```python
with ExcelHandler('reporte.xlsx') as excel:
    # Hoja vacía
    excel.add_sheet('Resumen')

    # Con datos
    df = pd.DataFrame({'Ventas': [100, 200, 300]})
    excel.add_sheet('Datos', df)

    # En posición específica (0 = primera)
    excel.add_sheet('Portada', df_portada, index=0)

    # Sobrescribir existente
    excel.add_sheet('Ventas', df_nuevas_ventas, overwrite=True)

    excel.save()
```

---

##### `delete_sheet()`

Elimina una hoja del Excel.

```python
def delete_sheet(sheet_name: str)
```

**Parámetros:**
- `sheet_name` (str): Nombre de la hoja a eliminar

**Excepciones:**
- `SheetNotFoundError`: Si la hoja no existe

**Ejemplo:**
```python
with ExcelHandler('datos.xlsx') as excel:
    # Eliminar hoja
    excel.delete_sheet('Temporal')

    # Con verificación previa
    if excel.sheet_exists('Borrador'):
        excel.delete_sheet('Borrador')

    excel.save()
```

---

##### `rename_sheet()`

Renombra una hoja del Excel.

```python
def rename_sheet(old_name: str, new_name: str)
```

**Parámetros:**
- `old_name` (str): Nombre actual de la hoja
- `new_name` (str): Nuevo nombre para la hoja

**Excepciones:**
- `SheetNotFoundError`: Si la hoja no existe
- `SheetAlreadyExistsError`: Si el nuevo nombre ya existe

**Ejemplo:**
```python
with ExcelHandler('datos.xlsx') as excel:
    excel.rename_sheet('Sheet1', 'Principal')
    excel.rename_sheet('datos_2023', 'Histórico 2023')
    excel.save()
```

---

##### `extract_sheet_to_dataframe()`

Extrae una hoja específica como DataFrame.

```python
def extract_sheet_to_dataframe(
    sheet_name: Union[str, int],
    **kwargs
) -> pd.DataFrame
```

**Parámetros:**
- `sheet_name` (str | int): Nombre o índice de la hoja
- `**kwargs`: Argumentos adicionales para `pd.read_excel`

**Retorna:** `pd.DataFrame` con los datos de la hoja

**Excepciones:**
- `SheetNotFoundError`: Si la hoja no existe (cuando es string)

**Ejemplo:**
```python
with ExcelHandler('reporte.xlsx') as excel:
    # Por nombre
    df = excel.extract_sheet_to_dataframe('Ventas')

    # Por índice
    df = excel.extract_sheet_to_dataframe(0)

    # Con opciones
    df = excel.extract_sheet_to_dataframe('Datos', skiprows=2, usecols='A:F')

    print(df.head())
```

---

##### `extract_range()`

Extrae un rango específico de celdas.

```python
def extract_range(
    sheet_name: str,
    start_row: int,
    start_col: int,
    end_row: int,
    end_col: int
) -> List[List[Any]]
```

**Parámetros:**
- `sheet_name` (str): Nombre de la hoja
- `start_row` (int): Fila inicial (1-indexed)
- `start_col` (int): Columna inicial (1-indexed)
- `end_row` (int): Fila final (1-indexed)
- `end_col` (int): Columna final (1-indexed)

**Retorna:** `List[List[Any]]` - Lista de listas con valores

**Excepciones:**
- `SheetNotFoundError`: Si la hoja no existe

**Nota:** Los índices son 1-based (openpyxl estándar).

**Ejemplo:**
```python
with ExcelHandler('datos.xlsx') as excel:
    # Extraer rango A1:C5
    data = excel.extract_range('Ventas', 1, 1, 5, 3)

    # Procesar datos
    for row in data:
        print(row)

    # Convertir a DataFrame
    import pandas as pd
    df = pd.DataFrame(data[1:], columns=data[0])
```

---

##### `save()`

Guarda los cambios en el archivo Excel.

```python
def save(file_path: Optional[Union[str, Path]] = None)
```

**Parámetros:**
- `file_path` (str | Path, opcional): Ruta alternativa para guardar (default: ruta original)

**Excepciones:**
- `FileOperationError`: Si hay error al guardar (permisos, archivo abierto, etc.)

**Ejemplo:**
```python
with ExcelHandler('original.xlsx') as excel:
    excel.add_sheet('Nueva')

    # Guardar en archivo original
    excel.save()

    # Guardar como copia
    excel.save('copia.xlsx')
```

---

##### `close()`

Cierra el workbook y libera recursos.

```python
def close()
```

**Nota:** No es necesario llamarlo manualmente si usas context manager.

**Ejemplo:**
```python
# Con context manager (RECOMENDADO)
with ExcelHandler('datos.xlsx') as excel:
    excel.add_sheet('Nueva')
    excel.save()
# close() se llama automáticamente

# Sin context manager (NO RECOMENDADO)
excel = ExcelHandler('datos.xlsx')
excel.add_sheet('Nueva')
excel.save()
excel.close()  # IMPORTANTE: no olvidar
```

---

### Utilidades

Funciones independientes para operaciones con múltiples archivos.

#### `merge_excel_files()`

Combina múltiples archivos Excel en uno solo (concatenación vertical).

```python
def merge_excel_files(
    file_paths: List[Union[str, Path]],
    output_path: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None,
    ignore_errors: bool = False
) -> pd.DataFrame
```

**Parámetros:**
- `file_paths` (list): Lista de rutas de archivos a combinar
- `output_path` (str | Path): Ruta del archivo de salida
- `sheet_name` (str | int, opcional): Hoja a leer (None = primera)
- `ignore_errors` (bool, opcional): Ignorar archivos con errores (default: False)

**Retorna:** `pd.DataFrame` - DataFrame combinado

**Excepciones:**
- `FileNotFoundError`: Si algún archivo no existe (si ignore_errors=False)
- `EmptyDataError`: Si no se pudieron leer archivos
- `FileOperationError`: Si hay error al procesar

**Ejemplo:**
```python
from excel_handler import merge_excel_files

# Combinar archivos mensuales
archivos = [
    'ventas_enero.xlsx',
    'ventas_febrero.xlsx',
    'ventas_marzo.xlsx'
]

df_trimestre = merge_excel_files(
    archivos,
    'ventas_Q1_2024.xlsx',
    sheet_name='Ventas'
)

print(f"Total filas combinadas: {len(df_trimestre)}")

# Con manejo de errores
df = merge_excel_files(
    archivos,
    'salida.xlsx',
    ignore_errors=True  # Continúa aunque falle algún archivo
)
```

---

#### `split_excel_by_column()`

Divide un Excel en múltiples archivos basándose en valores de una columna.

```python
def split_excel_by_column(
    file_path: Union[str, Path],
    column_name: str,
    output_dir: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None,
    prefix: str = "",
    suffix: str = ""
) -> dict
```

**Parámetros:**
- `file_path` (str | Path): Ruta del archivo a dividir
- `column_name` (str): Nombre de la columna para dividir
- `output_dir` (str | Path): Directorio de salida
- `sheet_name` (str | int, opcional): Hoja a procesar (None = primera)
- `prefix` (str, opcional): Prefijo para nombres de archivo
- `suffix` (str, opcional): Sufijo para nombres de archivo

**Retorna:** `dict` - {valor: ruta_archivo} para cada archivo creado

**Excepciones:**
- `FileNotFoundError`: Si el archivo no existe
- `KeyError`: Si la columna no existe
- `EmptyDataError`: Si el archivo está vacío
- `FileOperationError`: Si hay error al procesar

**Ejemplo:**
```python
from excel_handler import split_excel_by_column

# Dividir por región
archivos = split_excel_by_column(
    'ventas_nacional.xlsx',
    column_name='Región',
    output_dir='salida/regiones/'
)
# Crea: salida/regiones/Norte.xlsx, Sur.xlsx, Este.xlsx, Oeste.xlsx

print(f"Archivos creados: {len(archivos)}")
for region, archivo in archivos.items():
    print(f"  {region}: {archivo}")

# Con prefijo y sufijo
archivos = split_excel_by_column(
    'datos.xlsx',
    column_name='Categoría',
    output_dir='resultados/',
    prefix='cat_',
    suffix='_2024'
)
# Crea: cat_A_2024.xlsx, cat_B_2024.xlsx, etc.
```

---

#### `compare_excel_files()`

Compara dos archivos Excel y retorna las diferencias.

```python
def compare_excel_files(
    file1: Union[str, Path],
    file2: Union[str, Path],
    sheet_name: Optional[Union[str, int]] = None
) -> dict
```

**Parámetros:**
- `file1` (str | Path): Ruta del primer archivo
- `file2` (str | Path): Ruta del segundo archivo
- `sheet_name` (str | int, opcional): Hoja a comparar (None = primera)

**Retorna:** `dict` con información de diferencias:
- `are_equal` (bool): ¿Son idénticos?
- `shape_equal` (bool): ¿Tienen mismas dimensiones?
- `columns_equal` (bool): ¿Tienen mismas columnas?
- `shape1` (tuple): Dimensiones del archivo 1
- `shape2` (tuple): Dimensiones del archivo 2
- `diff_rows` (int): Número de filas diferentes

**Ejemplo:**
```python
from excel_handler import compare_excel_files

# Comparar versiones
diff = compare_excel_files('version1.xlsx', 'version2.xlsx')

if diff['are_equal']:
    print("Los archivos son idénticos")
else:
    print(f"Archivos diferentes:")
    print(f"  Mismas dimensiones: {diff['shape_equal']}")
    print(f"  Mismas columnas: {diff['columns_equal']}")
    print(f"  Filas diferentes: {diff['diff_rows']}")
    print(f"  Shape archivo 1: {diff['shape1']}")
    print(f"  Shape archivo 2: {diff['shape2']}")
```

---

## Excepciones

Todas las excepciones heredan de `ExcelHandlerError` para captura general.

### Jerarquía

```
ExcelHandlerError (base)
├── SheetNotFoundError
├── InvalidFileFormatError
├── SheetAlreadyExistsError
├── FileOperationError
└── EmptyDataError
```

### `ExcelHandlerError`

Excepción base para todos los errores del módulo.

**Uso:**
```python
from excel_handler import ExcelHandlerError

try:
    # Operaciones Excel
    pass
except ExcelHandlerError as e:
    print(f"Error en Excel Handler: {e}")
```

---

### `SheetNotFoundError`

La hoja especificada no existe en el archivo.

**Se lanza cuando:**
- Intentas acceder a una hoja inexistente
- Intentas eliminar/renombrar una hoja que no existe

**Ejemplo:**
```python
from excel_handler import ExcelHandler, SheetNotFoundError

try:
    with ExcelHandler('datos.xlsx') as excel:
        excel.delete_sheet('HojaInexistente')
except SheetNotFoundError as e:
    print(e)
    # Output: "Hoja 'HojaInexistente' no encontrada. Hojas disponibles: Sheet1, Ventas"
```

---

### `InvalidFileFormatError`

El formato del archivo no es válido o no está soportado.

**Se lanza cuando:**
- La extensión del archivo no es `.xlsx`, `.xlsm`, `.xltx` o `.xltm`
- El archivo está corrupto

**Ejemplo:**
```python
from excel_handler import ExcelHandler, InvalidFileFormatError

try:
    excel = ExcelHandler('documento.pdf')
except InvalidFileFormatError as e:
    print(e)
    # Output: "Extensión no soportada: .pdf. Extensiones válidas: .xlsx, .xlsm, ..."
```

---

### `SheetAlreadyExistsError`

Intento de crear una hoja con un nombre que ya existe.

**Se lanza cuando:**
- Agregas una hoja con nombre duplicado sin `overwrite=True`
- Renombras a un nombre que ya existe

**Ejemplo:**
```python
from excel_handler import ExcelHandler, SheetAlreadyExistsError

try:
    with ExcelHandler('datos.xlsx') as excel:
        excel.add_sheet('Ventas')  # Ya existe
except SheetAlreadyExistsError as e:
    print(e)
    # Output: "La hoja 'Ventas' ya existe. Use overwrite=True para sobrescribirla."
```

---

### `FileOperationError`

Error durante operaciones de archivo (I/O).

**Se lanza cuando:**
- No hay permisos de lectura/escritura
- El archivo está abierto en otra aplicación
- Disco lleno
- Errores de red (archivos en red)

**Ejemplo:**
```python
from excel_handler import ExcelHandler, FileOperationError

try:
    with ExcelHandler('protegido.xlsx') as excel:
        excel.add_sheet('Nueva')
        excel.save()
except FileOperationError as e:
    print(e)
    # Output: "No se puede guardar el archivo protegido.xlsx.
    #          Puede estar abierto en Excel u otra aplicación."
```

---

### `EmptyDataError`

Intento de escribir datos vacíos o DataFrame sin filas.

**Se lanza cuando:**
- Escribes un DataFrame vacío o None
- Intentas combinar archivos vacíos

**Ejemplo:**
```python
from excel_handler import QuickExcel, EmptyDataError
import pandas as pd

try:
    df_vacio = pd.DataFrame()
    QuickExcel.write(df_vacio, 'salida.xlsx')
except EmptyDataError as e:
    print(e)
    # Output: "No se pueden escribir datos vacíos al archivo Excel"
```

---

## Mejores Prácticas

### 1. Context Manager Siempre

```python
# ✅ CORRECTO - Auto-close garantizado
with ExcelHandler('datos.xlsx') as excel:
    excel.add_sheet('Nueva')
    excel.save()

# ❌ EVITAR - Puede causar memory leaks
excel = ExcelHandler('datos.xlsx')
excel.add_sheet('Nueva')
excel.save()
excel.close()  # Fácil olvidarlo
```

### 2. Validar Antes de Operar

```python
# ✅ CORRECTO
with ExcelHandler('datos.xlsx') as excel:
    if excel.sheet_exists('Temporal'):
        excel.delete_sheet('Temporal')

    if not df.empty:
        excel.add_sheet('Datos', df)

# ❌ PUEDE FALLAR
with ExcelHandler('datos.xlsx') as excel:
    excel.delete_sheet('Temporal')  # SheetNotFoundError si no existe
    excel.add_sheet('Datos', df)     # EmptyDataError si df vacío
```

### 3. Manejo de Excepciones Específico

```python
# ✅ CORRECTO - Captura específica
from excel_handler import ExcelHandler, SheetNotFoundError, FileOperationError

try:
    with ExcelHandler('datos.xlsx') as excel:
        excel.rename_sheet('Viejo', 'Nuevo')
        excel.save()
except SheetNotFoundError as e:
    print(f"Hoja no encontrada: {e}")
except FileOperationError as e:
    print(f"Error al guardar: {e}")
except Exception as e:
    print(f"Error inesperado: {e}")

# ⚠️ FUNCIONA PERO MENOS INFORMATIVO
try:
    # operaciones
    pass
except Exception as e:
    print(f"Error: {e}")
```

### 4. Usar pathlib para Rutas

```python
from pathlib import Path

# ✅ CORRECTO
output_dir = Path('data/reports/2024')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / 'reporte.xlsx'
QuickExcel.write(df, output_file)

# ⚠️ FUNCIONA PERO MENOS ROBUSTO
QuickExcel.write(df, 'data/reports/2024/reporte.xlsx')
```

### 5. Logging Apropiado

```python
from logger import setup_logger

logger = setup_logger(__name__)

# Las operaciones ya loguean automáticamente
with ExcelHandler('datos.xlsx') as excel:
    logger.info("Iniciando procesamiento de hojas")
    excel.add_sheet('Resumen', df)
    logger.info("Hoja agregada exitosamente")
    excel.save()

# Los logs se guardan en logs/YYYY-MM-DD.log
```

### 6. Separar Lectura de Escritura

```python
# ✅ CORRECTO
# Leer
df = QuickExcel.read('entrada.xlsx')

# Procesar
df_procesado = df[df['Valor'] > 100]

# Escribir
QuickExcel.write(df_procesado, 'salida.xlsx')

# ❌ EVITAR - No mezclar APIs sin necesidad
with ExcelHandler('entrada.xlsx') as excel:
    df = excel.extract_sheet_to_dataframe('Datos')
# Mejor usar QuickExcel.read() para esto
```

### 7. Validar Extensiones de Archivo

```python
from pathlib import Path

# ✅ CORRECTO
archivo = Path('datos.xlsx')
if archivo.suffix.lower() in ['.xlsx', '.xlsm']:
    df = QuickExcel.read(archivo)
else:
    print(f"Formato no soportado: {archivo.suffix}")

# El módulo también valida automáticamente
try:
    QuickExcel.read('documento.pdf')
except InvalidFileFormatError as e:
    print(f"Error: {e}")
```

### 8. Operaciones Batch Eficientes

```python
from pathlib import Path

# ✅ CORRECTO - Usar utilidades
archivos = list(Path('data/').glob('*.xlsx'))
df_combined = merge_excel_files(archivos, 'combinado.xlsx', ignore_errors=True)

# ❌ INEFICIENTE
dfs = []
for archivo in Path('data/').glob('*.xlsx'):
    df = QuickExcel.read(archivo)
    dfs.append(df)
df_combined = pd.concat(dfs)
QuickExcel.write(df_combined, 'combinado.xlsx')
```

---

## Resumen de Decisiones

| Necesito... | Usar... | Método/Función |
|-------------|---------|----------------|
| Leer archivo rápido | QuickExcel | `.read()` |
| Escribir archivo rápido | QuickExcel | `.write()` |
| Archivo con formato | QuickExcel | `.create_formatted()` |
| Múltiples hojas (escritura) | QuickExcel | `.write_multiple_sheets()` |
| Manipular hojas | ExcelHandler | `.add_sheet()`, `.delete_sheet()`, `.rename_sheet()` |
| Extraer rango | ExcelHandler | `.extract_range()` |
| Combinar archivos | Utilidad | `merge_excel_files()` |
| Dividir por columna | Utilidad | `split_excel_by_column()` |
| Comparar archivos | Utilidad | `compare_excel_files()` |

---

## Información del Módulo

- **Dependencias:** pandas, openpyxl, xlsxwriter, colorlog

---
