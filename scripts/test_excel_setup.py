"""Script para verificar que todas las librerías de Excel están instaladas correctamente."""
import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def check_library(name, import_statement):
    """Verifica si una librería está instalada correctamente."""
    try:
        exec(import_statement)
        print(f"✓ {name:20} - Instalado correctamente")
        return True
    except ImportError as e:
        print(f"✗ {name:20} - NO INSTALADO: {e}")
        return False
    except Exception as e:
        print(f"⚠ {name:20} - Error: {e}")
        return False


def main():
    """Verifica todas las dependencias de Excel."""
    print("\n" + "="*70)
    print("VERIFICACIÓN DE DEPENDENCIAS PARA TRABAJAR CON EXCEL")
    print("="*70 + "\n")

    libraries = [
        ("pandas", "import pandas as pd"),
        ("numpy", "import numpy as np"),
        ("openpyxl", "import openpyxl"),
        ("xlsxwriter", "import xlsxwriter"),
        ("xlrd", "import xlrd"),
        ("xlwt", "import xlwt"),
        ("pyxlsb", "import pyxlsb"),
        ("python-calamine", "from python_calamine import CalaminePandasReader"),
        ("python-dotenv", "from dotenv import load_dotenv"),
        ("python-dateutil", "from dateutil import parser"),
        ("validators", "import validators"),
        ("colorlog", "import colorlog"),
    ]

    results = []
    print("Librerías principales:")
    print("-" * 70)

    for name, import_stmt in libraries:
        results.append(check_library(name, import_stmt))

    # Resumen
    print("\n" + "="*70)
    installed = sum(results)
    total = len(results)
    percentage = (installed / total) * 100

    print(f"RESUMEN: {installed}/{total} librerías instaladas ({percentage:.1f}%)")

    if installed == total:
        print("✓ ¡Todas las dependencias están instaladas correctamente!")
        print("\nPuedes ejecutar los ejemplos con:")
        print("  python src/excel_examples.py")
    else:
        print("\n⚠ Algunas dependencias faltan. Instala con:")
        print("  pip install -r requirements.txt")

    print("="*70 + "\n")

    # Verificar versiones
    print("\nVersiones instaladas:")
    print("-" * 70)

    try:
        import pandas as pd
        print(f"pandas: {pd.__version__}")
    except:
        pass

    try:
        import numpy as np
        print(f"numpy: {np.__version__}")
    except:
        pass

    try:
        import openpyxl
        print(f"openpyxl: {openpyxl.__version__}")
    except:
        pass

    try:
        import xlsxwriter
        print(f"xlsxwriter: {xlsxwriter.__version__}")
    except:
        pass

    print("-" * 70)

    # Test rápido de funcionalidad
    if installed >= total * 0.8:  # Si al menos el 80% está instalado
        print("\n" + "="*70)
        print("TEST RÁPIDO DE FUNCIONALIDAD")
        print("="*70 + "\n")

        try:
            import pandas as pd
            import numpy as np

            # Crear DataFrame de prueba
            df = pd.DataFrame({
                'A': [1, 2, 3],
                'B': [4, 5, 6]
            })

            # Crear directorio de prueba
            test_dir = Path(__file__).parent.parent / 'data' / 'test'
            test_dir.mkdir(parents=True, exist_ok=True)

            # Guardar Excel
            test_file = test_dir / 'test_quick.xlsx'
            df.to_excel(test_file, index=False)
            print(f"✓ Archivo de prueba creado: {test_file}")

            # Leer Excel
            df_read = pd.read_excel(test_file)
            print(f"✓ Archivo de prueba leído correctamente")
            print(f"✓ Forma del DataFrame: {df_read.shape}")

            print("\n✓ ¡Test de funcionalidad completado con éxito!")

        except Exception as e:
            print(f"\n✗ Error en test de funcionalidad: {e}")

        print("="*70 + "\n")


if __name__ == "__main__":
    main()
