# Guía Completa para Trabajar con Excel en Python

Esta guía documenta las mejores librerías y prácticas para trabajar con archivos Excel.

## Librerías Incluidas

### 1. pandas - Análisis y Manipulación de Datos
**Uso principal:** Lectura/escritura rápida, análisis de datos, transformaciones

```python
import pandas as pd

# Leer Excel
df = pd.read_excel('archivo.xlsx', sheet_name='Hoja1')

# Escribir Excel
df.to_excel('salida.xlsx', sheet_name='Datos', index=False)

# Leer múltiples hojas
sheets = pd.read_excel('archivo.xlsx', sheet_name=None)
```

**Ventajas:**
- Muy rápido para grandes volúmenes de datos
- Integración perfecta con análisis de datos
- Funciones de agregación y transformación potentes

**Documentación:** https://pandas.pydata.org/docs/

---

### 2. openpyxl - Manipulación Completa de .xlsx
**Uso principal:** Formato, estilos, fórmulas, gráficos, lectura/escritura

```python
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill

# Leer Excel existente
wb = load_workbook('archivo.xlsx')
ws = wb['Hoja1']

# Acceder a celdas
valor = ws['A1'].value
ws['A1'] = 'Nuevo valor'

# Aplicar estilos
ws['A1'].font = Font(bold=True, color='FF0000')
ws['A1'].fill = PatternFill(start_color='FFFF00', fill_type='solid')

# Guardar
wb.save('archivo_modificado.xlsx')
```

**Ventajas:**
- Soporta estilos, colores, fuentes, bordes
- Maneja fórmulas de Excel
- Puede crear gráficos
- Mejor para preservar formato existente

**Documentación:** https://openpyxl.readthedocs.io/

---

### 3. xlsxwriter - Creación Avanzada de Excel
**Uso principal:** Crear archivos Excel con formato profesional desde cero

```python
import xlsxwriter

# Crear workbook
workbook = xlsxwriter.Workbook('reporte.xlsx')
worksheet = workbook.add_worksheet('Ventas')

# Definir formatos
header_format = workbook.add_format({
    'bold': True,
    'bg_color': '#4472C4',
    'font_color': 'white',
    'border': 1
})

# Escribir con formato
worksheet.write('A1', 'Encabezado', header_format)

# Añadir gráfico
chart = workbook.add_chart({'type': 'column'})
chart.add_series({'values': '=Ventas!$B$2:$B$10'})
worksheet.insert_chart('D2', chart)

workbook.close()
```

**Ventajas:**
- Formatos muy avanzados
- Gráficos profesionales
- Validación de datos
- Fórmulas complejas
- Solo escritura (no lee archivos)

**Documentación:** https://xlsxwriter.readthedocs.io/

---

### 4. xlrd / xlwt - Archivos .xls (Excel Antiguo)
**Uso principal:** Archivos Excel 97-2003 (.xls)

```python
import xlrd
import xlwt

# Leer .xls
book = xlrd.open_workbook('antiguo.xls')
sheet = book.sheet_by_index(0)
valor = sheet.cell_value(0, 0)

# Escribir .xls
workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('Hoja1')
worksheet.write(0, 0, 'Hola')
workbook.save('nuevo.xls')
```

**Ventajas:**
- Soporte para formato antiguo .xls
- Útil para sistemas legacy

**Documentación:**
- xlrd: https://xlrd.readthedocs.io/
- xlwt: https://xlwt.readthedocs.io/

---

### 5. pyxlsb - Archivos .xlsb (Excel Binario)
**Uso principal:** Leer archivos Excel binarios

```python
from pyxlsb import open_workbook

with open_workbook('archivo.xlsb') as wb:
    with wb.get_sheet(1) as sheet:
        for row in sheet.rows():
            print([item.v for item in row])
```

**Ventajas:**
- Lee archivos .xlsb (más comprimidos que .xlsx)
- Útil cuando el cliente usa formato binario

**Documentación:** https://github.com/willtrnr/pyxlsb

---

### 6. python-calamine - Lectura Ultra-Rápida
**Uso principal:** Lectura extremadamente rápida de Excel

```python
from python_calamine import CalaminePandasReader

# Leer Excel muy rápido
reader = CalaminePandasReader('archivo.xlsx')
df = reader.read_sheet(sheet_name='Hoja1')
```

**Ventajas:**
- Mucho más rápido que pandas para lectura
- Ideal para archivos grandes
- Solo lectura

**Documentación:** https://github.com/tafia/calamine

---

## Casos de Uso Comunes

### Caso 1: Lectura Rápida de Datos
**Mejor opción:** pandas o python-calamine

```python
# Para análisis de datos
df = pd.read_excel('datos.xlsx')

# Para lectura muy rápida
from python_calamine import CalaminePandasReader
reader = CalaminePandasReader('datos.xlsx')
df = reader.read_sheet()
```

### Caso 2: Crear Reportes Formateados
**Mejor opción:** xlsxwriter o openpyxl

```python
# Con xlsxwriter (más potente para crear)
writer = pd.ExcelWriter('reporte.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Datos', index=False)

workbook = writer.book
worksheet = writer.sheets['Datos']
header_format = workbook.add_format({'bold': True, 'bg_color': 'blue'})
# ... aplicar formatos
writer.close()
```

### Caso 3: Modificar Excel Existente
**Mejor opción:** openpyxl

```python
from openpyxl import load_workbook

wb = load_workbook('existente.xlsx')
ws = wb['Hoja1']
ws['A1'] = 'Modificado'
wb.save('existente.xlsx')
```

### Caso 4: Procesar Múltiples Archivos
**Mejor opción:** pandas + pathlib

```python
from pathlib import Path
import pandas as pd

# Leer todos los Excel de una carpeta
files = Path('datos/').glob('*.xlsx')
dfs = [pd.read_excel(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)
```

### Caso 5: Excel con Fórmulas
**Mejor opción:** openpyxl

```python
ws['C1'] = '=SUM(A1:B1)'
wb.save('con_formulas.xlsx')
```

---

## Comparativa Rápida

| Librería | Lectura | Escritura | Formato | Fórmulas | Velocidad | Uso Principal |
|----------|---------|-----------|---------|----------|-----------|---------------|
| **pandas** | ✅✅ | ✅✅ | ⚠️ | ❌ | ⚡⚡ | Análisis de datos |
| **openpyxl** | ✅ | ✅ | ✅✅ | ✅ | ⚡ | Formato y estilos |
| **xlsxwriter** | ❌ | ✅✅ | ✅✅✅ | ✅ | ⚡ | Crear reportes |
| **xlrd/xlwt** | ✅ | ✅ | ⚠️ | ❌ | ⚡ | Archivos .xls |
| **pyxlsb** | ✅ | ❌ | ❌ | ❌ | ⚡⚡ | Archivos .xlsb |
| **calamine** | ✅✅ | ❌ | ❌ | ❌ | ⚡⚡⚡ | Lectura rápida |

---

## Mejores Prácticas

### 1. Elegir la Librería Correcta
```python
# Para análisis → pandas
df = pd.read_excel('datos.xlsx')

# Para formato → openpyxl o xlsxwriter
wb = load_workbook('formato.xlsx')

# Para velocidad → python-calamine
reader = CalaminePandasReader('grande.xlsx')
```

### 2. Manejo de Memoria con Archivos Grandes
```python
# Leer por chunks
for chunk in pd.read_excel('grande.xlsx', chunksize=1000):
    procesar(chunk)

# Usar calamine para lectura
from python_calamine import CalaminePandasReader
reader = CalaminePandasReader('grande.xlsx')
df = reader.read_sheet()
```

### 3. Validar Datos Antes de Procesar
```python
import validators

# Validar antes de escribir
if validators.email(email):
    df.to_excel('salida.xlsx')
```

### 4. Manejo de Errores
```python
try:
    df = pd.read_excel('archivo.xlsx')
except FileNotFoundError:
    print("Archivo no encontrado")
except Exception as e:
    print(f"Error al leer Excel: {e}")
```

### 5. Usar Context Managers
```python
from openpyxl import load_workbook

# Buena práctica
with load_workbook('archivo.xlsx') as wb:
    ws = wb.active
    # trabajar con el archivo
    wb.save('archivo.xlsx')
# Se cierra automáticamente
```

---

## Recursos y Enlaces

### Documentación Oficial
- **pandas:** https://pandas.pydata.org/docs/
- **openpyxl:** https://openpyxl.readthedocs.io/
- **xlsxwriter:** https://xlsxwriter.readthedocs.io/
- **xlrd:** https://xlrd.readthedocs.io/
- **python-calamine:** https://github.com/tafia/calamine

### Tutoriales de la Comunidad
- Real Python Excel: https://realpython.com/openpyxl-excel-spreadsheets-python/
- pandas Excel: https://realpython.com/working-with-large-excel-files-in-pandas/
- Stack Overflow: https://stackoverflow.com/questions/tagged/openpyxl

### Ejemplos Avanzados
- Gráficos con xlsxwriter: https://xlsxwriter.readthedocs.io/chart_examples.html
- Estilos con openpyxl: https://openpyxl.readthedocs.io/en/stable/styles.html
- pandas Excel styling: https://pandas.pydata.org/docs/reference/api/pandas.io.formats.style.Styler.html

---

## Solución de Problemas Comunes

### Error: "No module named 'openpyxl'"
```bash
pip install openpyxl
```

### Error: "Excel file format cannot be determined"
```python
# Especificar el engine explícitamente
pd.read_excel('archivo.xlsx', engine='openpyxl')
```

### Error de Memoria con Archivos Grandes
```python
# Usar calamine para lectura rápida
from python_calamine import CalaminePandasReader
reader = CalaminePandasReader('grande.xlsx')
df = reader.read_sheet()
```

### Preservar Formato al Modificar
```python
# Usar openpyxl en modo "keep"
from openpyxl import load_workbook
wb = load_workbook('archivo.xlsx', keep_vba=True, keep_links=True)
# ... modificar
wb.save('archivo.xlsx')
```

---

## Ejemplo Completo: Pipeline de Procesamiento

```python
from pathlib import Path
import pandas as pd
from excel_handler import ExcelHandler

def pipeline_completo():
    # 1. Leer archivos de entrada
    input_dir = Path('data/raw')
    files = list(input_dir.glob('*.xlsx'))

    # 2. Combinar datos
    dfs = []
    for file in files:
        df = pd.read_excel(file)
        df['Origen'] = file.stem
        dfs.append(df)

    df_combined = pd.concat(dfs, ignore_index=True)

    # 3. Procesar y limpiar
    df_combined = df_combined.dropna()
    df_combined['Total'] = df_combined['Cantidad'] * df_combined['Precio']

    # 4. Análisis
    resumen = df_combined.groupby('Categoria').agg({
        'Total': 'sum',
        'Cantidad': 'sum'
    })

    # 5. Guardar resultados con formato
    output_path = Path('data/processed/reporte_final.xlsx')
    datos = {
        'Datos_Completos': df_combined,
        'Resumen': resumen
    }

    ExcelHandler.write_multiple_sheets(datos, output_path)

    print(f"✓ Pipeline completado: {output_path}")

if __name__ == "__main__":
    pipeline_completo()
```
