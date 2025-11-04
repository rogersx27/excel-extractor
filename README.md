# Proyecto Python

Proyecto base para desarrollo en Python con buenas prácticas y herramientas especializadas para trabajar con archivos Excel.

## Estructura del Proyecto

```
.
├── src/                  # Código fuente principal
├── tests/                # Tests unitarios y de integración
├── docs/                 # Documentación
├── scripts/              # Scripts auxiliares
├── data/                 # Datos del proyecto
├── logs/                 # Logs de la aplicación
├── requirements.txt      # Dependencias de producción
├── requirements-dev.txt  # Dependencias de desarrollo
├── pyproject.toml        # Configuración del proyecto
└── .gitignore           # Archivos ignorados por Git
```

## Configuración Inicial

### 1. Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate
```

### 2. Instalar dependencias

```bash
# Para desarrollo (incluye herramientas de testing y linting)
pip install -r requirements-dev.txt

# Solo para producción
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo y editarlo con tus valores
cp .env.example .env
```

## Uso

### Ejecutar tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src --cov-report=html

# Ver reporte de cobertura
# Abrir htmlcov/index.html en el navegador
```

### Formatear código

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

## Trabajar con Excel

Este proyecto incluye herramientas avanzadas para manipular archivos Excel.

### Verificar instalación de librerías Excel

```bash
python scripts/test_excel_setup.py
```

### Ejecutar ejemplos de Excel

```bash
# Ejecutar todos los ejemplos
python src/excel_examples.py

# O importar y usar el módulo
python
>>> from excel_handler import ExcelHandler
>>> df = ExcelHandler.read_excel_pandas('archivo.xlsx')
```

### Librerías incluidas para Excel

- **pandas** - Análisis y manipulación de datos
- **openpyxl** - Leer/escribir .xlsx con estilos y formato
- **xlsxwriter** - Crear archivos Excel con formato avanzado
- **xlrd/xlwt** - Soporte para archivos .xls antiguos
- **pyxlsb** - Leer archivos .xlsb (binarios)
- **python-calamine** - Lectura ultra-rápida de Excel

### Funcionalidades principales

- Leer y escribir archivos Excel (.xlsx, .xls, .xlsb)
- Crear hojas, eliminar hojas, renombrar hojas
- Extraer datos de hojas específicas
- Aplicar formato profesional (colores, fuentes, bordes)
- Combinar múltiples archivos Excel
- Dividir Excel por categorías
- Procesar grandes volúmenes de datos eficientemente

Consulta `docs/EXCEL_GUIDE.md` para documentación completa y ejemplos avanzados.

## Desarrollo

1. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`
2. Escribe código en `src/` y tests correspondientes en `tests/`
3. Ejecuta los tests y verificaciones de calidad
4. Haz commit de tus cambios
5. Envía un pull request

## Herramientas Incluidas

- **pytest**: Framework de testing
- **black**: Formateador de código
- **isort**: Ordenador de imports
- **flake8**: Linter de código
- **mypy**: Type checker
- **pylint**: Análisis estático de código
- **coverage**: Medición de cobertura de tests

## Licencia

[Especifica tu licencia aquí]
