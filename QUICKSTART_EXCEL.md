# Guía Rápida: Empezar a Trabajar con Excel

## Instalación Rápida (5 minutos)

### 1. Crear y activar entorno virtual
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar instalación
```bash
python scripts/test_excel_setup.py
```

---

## Primeros Pasos

### Ejemplo 1: Leer un Excel
```python
from excel_handler import ExcelHandler

# Leer Excel con pandas (más rápido)
df = ExcelHandler.read_excel_pandas('tu_archivo.xlsx')
print(df.head())

# Ver todas las hojas
sheets = ExcelHandler.read_all_sheets_pandas('tu_archivo.xlsx')
for nombre, df in sheets.items():
    print(f"Hoja: {nombre} - {len(df)} filas")
```

### Ejemplo 2: Crear un Excel
```python
import pandas as pd
from excel_handler import ExcelHandler

# Crear datos
data = {
    'Nombre': ['Juan', 'María', 'Pedro'],
    'Edad': [30, 25, 35],
    'Salario': [45000, 52000, 48000]
}
df = pd.DataFrame(data)

# Guardar en Excel
ExcelHandler.write_dataframe_to_excel(df, 'empleados.xlsx', sheet_name='Personal')
```

### Ejemplo 3: Excel con Formato Profesional
```python
import pandas as pd
from excel_handler import ExcelHandler

# Crear datos
df = pd.DataFrame({
    'Producto': ['Laptop', 'Mouse', 'Teclado'],
    'Precio': [1000, 25, 75],
    'Stock': [10, 50, 30]
})

# Guardar con formato bonito
ExcelHandler.create_formatted_excel(
    df,
    'productos_formateado.xlsx',
    sheet_name='Inventario',
    auto_filter=True,
    freeze_panes=True
)
```

### Ejemplo 4: Múltiples Hojas
```python
from excel_handler import ExcelHandler
import pandas as pd

# Crear varios DataFrames
df_ventas = pd.DataFrame({'Mes': ['Ene', 'Feb'], 'Total': [10000, 15000]})
df_gastos = pd.DataFrame({'Mes': ['Ene', 'Feb'], 'Total': [5000, 7000]})

# Guardar en un solo archivo
data = {
    'Ventas': df_ventas,
    'Gastos': df_gastos
}
ExcelHandler.write_multiple_sheets(data, 'reporte_mensual.xlsx')
```

### Ejemplo 5: Manipular Hojas
```python
from excel_handler import ExcelHandler

# Abrir Excel existente
handler = ExcelHandler('reporte.xlsx')
handler.read_excel_openpyxl()

# Ver hojas actuales
print(handler.get_sheet_names())

# Añadir nueva hoja
import pandas as pd
df_nuevo = pd.DataFrame({'Dato': [1, 2, 3]})
handler.add_sheet('NuevaHoja', df_nuevo)

# Renombrar hoja
handler.rename_sheet('Sheet1', 'Datos_Principales')

# Eliminar hoja
handler.delete_sheet('HojaVieja')

# Guardar cambios
handler.save()
handler.close()
```

---

## Casos de Uso Comunes

### Combinar Múltiples Archivos Excel
```python
from excel_handler import merge_excel_files

files = ['enero.xlsx', 'febrero.xlsx', 'marzo.xlsx']
df_combined = merge_excel_files(files, 'trimestre.xlsx')
print(f"Total de filas combinadas: {len(df_combined)}")
```

### Dividir Excel por Categoría
```python
from excel_handler import split_excel_by_column

# Divide el Excel en múltiples archivos según la columna 'Región'
split_excel_by_column('ventas.xlsx', 'Región', 'salida/')
# Crea: salida/Norte.xlsx, salida/Sur.xlsx, etc.
```

### Extraer Rango Específico
```python
from excel_handler import ExcelHandler

handler = ExcelHandler('datos.xlsx')
handler.read_excel_openpyxl()

# Extraer filas 2-10, columnas 1-5
data = handler.extract_range('Hoja1', start_row=2, start_col=1, end_row=10, end_col=5)
print(data)

handler.close()
```

### Procesar y Analizar Datos
```python
import pandas as pd
from excel_handler import ExcelHandler

# Leer datos
df = ExcelHandler.read_excel_pandas('ventas.xlsx')

# Analizar
resumen = df.groupby('Categoria').agg({
    'Ventas': 'sum',
    'Cantidad': 'sum'
})

# Guardar análisis
data = {
    'Datos_Originales': df,
    'Resumen': resumen
}
ExcelHandler.write_multiple_sheets(data, 'analisis.xlsx')
```

---

## Ejemplos Listos para Ejecutar

El proyecto incluye 10 ejemplos completos que puedes ejecutar:

```bash
# Ejecutar todos los ejemplos
python src/excel_examples.py
```

Los ejemplos cubren:
1. Crear Excel básico
2. Excel con formato profesional
3. Múltiples hojas
4. Leer y procesar
5. Manipular hojas
6. Extraer hojas específicas
7. Combinar múltiples archivos
8. Dividir Excel por categoría
9. Extraer rangos específicos
10. Procesamiento avanzado

---

## Consejos Rápidos

### ¿Qué librería usar?
- **Para leer datos rápidamente:** `pandas` o `python-calamine`
- **Para crear reportes bonitos:** `xlsxwriter` o `openpyxl`
- **Para modificar Excel existente:** `openpyxl`
- **Para archivos muy grandes:** `python-calamine`

### Optimización
```python
# Leer solo columnas específicas
df = pd.read_excel('archivo.xlsx', usecols=['A', 'B', 'C'])

# Leer solo primeras N filas
df = pd.read_excel('archivo.xlsx', nrows=1000)

# Leer sin encabezados
df = pd.read_excel('archivo.xlsx', header=None)
```

### Manejo de Errores
```python
try:
    df = ExcelHandler.read_excel_pandas('archivo.xlsx')
except FileNotFoundError:
    print("Archivo no encontrado")
except Exception as e:
    print(f"Error: {e}")
```

---

## Documentación Completa

Para más detalles, consulta:
- `docs/EXCEL_GUIDE.md` - Guía completa con todas las librerías
- `src/excel_handler.py` - Módulo principal (con docstrings)
- `src/excel_examples.py` - 10 ejemplos prácticos completos

---

## Soporte y Recursos

### Documentación de las librerías:
- pandas: https://pandas.pydata.org/docs/
- openpyxl: https://openpyxl.readthedocs.io/
- xlsxwriter: https://xlsxwriter.readthedocs.io/

### Ayuda rápida:
```python
# Ver ayuda de cualquier función
help(ExcelHandler.read_excel_pandas)
help(ExcelHandler.create_formatted_excel)
```

---

## Siguiente Paso

¡Empieza con los ejemplos!

```bash
python src/excel_examples.py
```

O crea tu propio script en `src/mi_excel.py` y experimenta.
