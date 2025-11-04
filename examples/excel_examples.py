"""Ejemplos prácticos de uso del módulo excel_handler.

Este archivo contiene ejemplos de uso común para trabajar con Excel.
"""
import logging
from pathlib import Path

import pandas as pd
import numpy as np

from excel_handler import ExcelHandler, merge_excel_files, split_excel_by_column
from logger import setup_logger

# Configurar logging
logger = setup_logger(__name__)


def ejemplo_1_crear_excel_basico():
    """Ejemplo 1: Crear un archivo Excel básico con pandas."""
    logger.info("=== Ejemplo 1: Crear Excel básico ===")

    # Crear datos de ejemplo
    data = {
        'Nombre': ['Juan', 'María', 'Pedro', 'Ana', 'Luis'],
        'Edad': [30, 25, 35, 28, 32],
        'Ciudad': ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao'],
        'Salario': [45000, 52000, 48000, 51000, 47000]
    }
    df = pd.DataFrame(data)

    # Guardar en Excel
    output_path = Path('data/ejemplo_basico.xlsx')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ExcelHandler.write_dataframe_to_excel(df, output_path, sheet_name='Empleados')

    logger.info(f"✓ Excel básico creado: {output_path}")


def ejemplo_2_crear_excel_formateado():
    """Ejemplo 2: Crear un Excel con formato profesional."""
    logger.info("=== Ejemplo 2: Crear Excel formateado ===")

    # Crear datos de ventas
    np.random.seed(42)
    data = {
        'Fecha': pd.date_range('2024-01-01', periods=20, freq='D'),
        'Producto': np.random.choice(['Laptop', 'Mouse', 'Teclado', 'Monitor'], 20),
        'Cantidad': np.random.randint(1, 10, 20),
        'Precio_Unitario': np.random.uniform(10, 1000, 20).round(2),
    }
    df = pd.DataFrame(data)
    df['Total'] = (df['Cantidad'] * df['Precio_Unitario']).round(2)

    # Guardar con formato
    output_path = Path('data/ventas_formateado.xlsx')
    ExcelHandler.create_formatted_excel(
        df,
        output_path,
        sheet_name='Ventas',
        auto_filter=True,
        freeze_panes=True
    )

    logger.info(f"✓ Excel formateado creado: {output_path}")


def ejemplo_3_multiples_hojas():
    """Ejemplo 3: Crear un Excel con múltiples hojas."""
    logger.info("=== Ejemplo 3: Excel con múltiples hojas ===")

    # Crear diferentes DataFrames
    df_ventas = pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Ventas': [10000, 15000, 12000]
    })

    df_gastos = pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Gastos': [5000, 7000, 6000]
    })

    df_resumen = pd.DataFrame({
        'Mes': ['Enero', 'Febrero', 'Marzo'],
        'Beneficio': [5000, 8000, 6000]
    })

    # Guardar en un solo archivo con múltiples hojas
    data = {
        'Ventas': df_ventas,
        'Gastos': df_gastos,
        'Resumen': df_resumen
    }

    output_path = Path('data/reporte_completo.xlsx')
    ExcelHandler.write_multiple_sheets(data, output_path)

    logger.info(f"✓ Excel con {len(data)} hojas creado: {output_path}")


def ejemplo_4_leer_y_procesar():
    """Ejemplo 4: Leer y procesar un archivo Excel."""
    logger.info("=== Ejemplo 4: Leer y procesar Excel ===")

    # Primero crear un archivo de ejemplo
    df = pd.DataFrame({
        'Producto': ['A', 'B', 'C', 'D', 'E'],
        'Precio': [100, 200, 150, 300, 250],
        'Stock': [10, 5, 8, 3, 12]
    })
    input_path = Path('data/productos.xlsx')
    df.to_excel(input_path, index=False)

    # Leer el archivo
    df_leido = ExcelHandler.read_excel_pandas(input_path)
    logger.info(f"Datos leídos:\n{df_leido}")

    # Procesar: calcular valor total del inventario
    df_leido['Valor_Total'] = df_leido['Precio'] * df_leido['Stock']

    # Guardar resultado
    output_path = Path('data/productos_procesados.xlsx')
    ExcelHandler.write_dataframe_to_excel(df_leido, output_path)

    logger.info(f"✓ Excel procesado guardado: {output_path}")


def ejemplo_5_manipular_hojas():
    """Ejemplo 5: Manipular hojas de un Excel existente."""
    logger.info("=== Ejemplo 5: Manipular hojas ===")

    # Crear archivo inicial
    input_path = Path('data/ejemplo_hojas.xlsx')
    df1 = pd.DataFrame({'A': [1, 2, 3]})
    df2 = pd.DataFrame({'B': [4, 5, 6]})
    ExcelHandler.write_multiple_sheets({'Hoja1': df1, 'Hoja2': df2}, input_path)

    # Manipular hojas
    handler = ExcelHandler(input_path)
    handler.read_excel_openpyxl()

    # Ver hojas actuales
    logger.info(f"Hojas actuales: {handler.get_sheet_names()}")

    # Añadir nueva hoja
    df_nueva = pd.DataFrame({'C': [7, 8, 9]})
    handler.add_sheet('Hoja3', df_nueva)

    # Renombrar hoja
    handler.rename_sheet('Hoja1', 'Datos_Iniciales')

    # Guardar cambios
    handler.save()
    handler.close()

    # Verificar cambios
    handler2 = ExcelHandler(input_path)
    handler2.read_excel_openpyxl()
    logger.info(f"✓ Hojas después de manipular: {handler2.get_sheet_names()}")
    handler2.close()


def ejemplo_6_extraer_hojas():
    """Ejemplo 6: Extraer hojas específicas."""
    logger.info("=== Ejemplo 6: Extraer hojas específicas ===")

    # Crear archivo con múltiples hojas
    input_path = Path('data/ventas_mensuales.xlsx')
    data = {
        'Enero': pd.DataFrame({'Ventas': [100, 200, 300]}),
        'Febrero': pd.DataFrame({'Ventas': [150, 250, 350]}),
        'Marzo': pd.DataFrame({'Ventas': [120, 220, 320]})
    }
    ExcelHandler.write_multiple_sheets(data, input_path)

    # Leer todas las hojas
    all_sheets = ExcelHandler.read_all_sheets_pandas(input_path)
    logger.info(f"Hojas encontradas: {list(all_sheets.keys())}")

    # Extraer hoja específica
    handler = ExcelHandler(input_path)
    df_febrero = handler.extract_sheet_to_dataframe('Febrero')
    logger.info(f"Datos de Febrero:\n{df_febrero}")

    # Guardar hoja extraída en archivo separado
    output_path = Path('data/solo_febrero.xlsx')
    ExcelHandler.write_dataframe_to_excel(df_febrero, output_path, sheet_name='Febrero')

    logger.info(f"✓ Hoja extraída guardada: {output_path}")


def ejemplo_7_combinar_excels():
    """Ejemplo 7: Combinar múltiples archivos Excel."""
    logger.info("=== Ejemplo 7: Combinar archivos Excel ===")

    # Crear varios archivos de ejemplo
    files_to_merge = []
    for i, mes in enumerate(['Enero', 'Febrero', 'Marzo'], 1):
        df = pd.DataFrame({
            'Mes': [mes] * 5,
            'Dia': range(1, 6),
            'Ventas': np.random.randint(100, 500, 5)
        })
        file_path = Path(f'data/ventas_{mes.lower()}.xlsx')
        df.to_excel(file_path, index=False)
        files_to_merge.append(file_path)

    # Combinar todos los archivos
    output_path = Path('data/ventas_trimestre_combinado.xlsx')
    df_combined = merge_excel_files(files_to_merge, output_path)

    logger.info(f"✓ {len(files_to_merge)} archivos combinados en: {output_path}")
    logger.info(f"Total de filas: {len(df_combined)}")


def ejemplo_8_dividir_excel():
    """Ejemplo 8: Dividir un Excel en múltiples archivos."""
    logger.info("=== Ejemplo 8: Dividir Excel por categoría ===")

    # Crear archivo con datos de varias regiones
    df = pd.DataFrame({
        'Región': ['Norte', 'Sur', 'Norte', 'Este', 'Oeste', 'Sur', 'Este'],
        'Ciudad': ['Madrid', 'Sevilla', 'Barcelona', 'Valencia', 'Bilbao', 'Málaga', 'Alicante'],
        'Ventas': [10000, 8000, 12000, 9000, 7000, 8500, 9500]
    })

    input_path = Path('data/ventas_regiones.xlsx')
    df.to_excel(input_path, index=False)

    # Dividir por región
    output_dir = Path('data/por_region')
    split_excel_by_column(input_path, 'Región', output_dir)

    logger.info(f"✓ Excel dividido en archivos por región en: {output_dir}")


def ejemplo_9_extraer_rango():
    """Ejemplo 9: Extraer un rango específico de celdas."""
    logger.info("=== Ejemplo 9: Extraer rango específico ===")

    # Crear archivo de ejemplo
    df = pd.DataFrame({
        'A': range(1, 11),
        'B': range(11, 21),
        'C': range(21, 31),
        'D': range(31, 41)
    })
    input_path = Path('data/matriz_datos.xlsx')
    df.to_excel(input_path, index=False)

    # Extraer rango específico (filas 2-5, columnas 1-3)
    handler = ExcelHandler(input_path)
    handler.read_excel_openpyxl()

    # Extraer rango (nota: openpyxl usa índices 1-based)
    range_data = handler.extract_range('Sheet1', start_row=2, start_col=1, end_row=5, end_col=3)
    logger.info(f"Rango extraído (filas 2-5, cols 1-3):")
    for row in range_data:
        logger.info(f"  {row}")

    handler.close()


def ejemplo_10_procesamiento_avanzado():
    """Ejemplo 10: Procesamiento avanzado de datos."""
    logger.info("=== Ejemplo 10: Procesamiento avanzado ===")

    # Crear datos de ejemplo más complejos
    np.random.seed(42)
    df = pd.DataFrame({
        'Fecha': pd.date_range('2024-01-01', periods=100, freq='D'),
        'Producto': np.random.choice(['A', 'B', 'C'], 100),
        'Cantidad': np.random.randint(1, 50, 100),
        'Precio': np.random.uniform(10, 100, 100).round(2)
    })
    df['Total'] = (df['Cantidad'] * df['Precio']).round(2)

    # Análisis y agrupación
    resumen_producto = df.groupby('Producto').agg({
        'Cantidad': 'sum',
        'Total': 'sum',
        'Precio': 'mean'
    }).round(2)
    resumen_producto.columns = ['Cantidad_Total', 'Ventas_Total', 'Precio_Promedio']

    # Resumen por mes
    df['Mes'] = df['Fecha'].dt.to_period('M')
    resumen_mensual = df.groupby('Mes').agg({
        'Total': 'sum',
        'Cantidad': 'sum'
    }).round(2)

    # Guardar análisis en diferentes hojas
    output_path = Path('data/analisis_completo.xlsx')
    analisis = {
        'Datos_Originales': df.drop('Mes', axis=1),
        'Por_Producto': resumen_producto,
        'Por_Mes': resumen_mensual
    }
    ExcelHandler.write_multiple_sheets(analisis, output_path)

    logger.info(f"✓ Análisis completo guardado: {output_path}")
    logger.info(f"\nResumen por Producto:\n{resumen_producto}")


def ejecutar_todos_los_ejemplos():
    """Ejecuta todos los ejemplos."""
    logger.info("\n" + "="*60)
    logger.info("EJECUTANDO TODOS LOS EJEMPLOS")
    logger.info("="*60 + "\n")

    ejemplos = [
        ejemplo_1_crear_excel_basico,
        ejemplo_2_crear_excel_formateado,
        ejemplo_3_multiples_hojas,
        ejemplo_4_leer_y_procesar,
        ejemplo_5_manipular_hojas,
        ejemplo_6_extraer_hojas,
        ejemplo_7_combinar_excels,
        ejemplo_8_dividir_excel,
        ejemplo_9_extraer_rango,
        ejemplo_10_procesamiento_avanzado,
    ]

    for i, ejemplo in enumerate(ejemplos, 1):
        try:
            print(f"\n{'─'*60}")
            ejemplo()
            print(f"{'─'*60}\n")
        except Exception as e:
            logger.error(f"❌ Error en ejemplo {i}: {e}")

    logger.info("\n" + "="*60)
    logger.info("TODOS LOS EJEMPLOS COMPLETADOS")
    logger.info("="*60)


if __name__ == "__main__":
    # Ejecutar todos los ejemplos
    ejecutar_todos_los_ejemplos()

    # O ejecutar un ejemplo específico:
    # ejemplo_1_crear_excel_basico()
    # ejemplo_2_crear_excel_formateado()
    # etc...
