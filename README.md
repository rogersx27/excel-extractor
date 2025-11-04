# Proyecto Python

Proyecto base para desarrollo en Python con buenas prácticas.

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
