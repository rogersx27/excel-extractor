# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive Python project specialized in Excel file manipulation, data extraction, consolidation, and batch processing. The project provides a complete suite of tools for reading, writing, formatting, extracting, and consolidating Excel files with both simple and complex structures.

**Primary Purpose:** Advanced Excel file handling with support for .xlsx, .xls, and .xlsb formats, including automated extraction, consolidation, and batch processing workflows

**Key Technology:** Python 3.8+ with pandas, openpyxl, xlsxwriter, and specialized Excel libraries

**Key Features:**
- Multi-format Excel support (.xlsx, .xls, .xlsb)
- Automated sheet extraction and consolidation
- Batch processing with parallel execution support
- Advanced logging system with visual formatting (Pretty Logging)
- Structure detection for simple and complex Excel files
- Context managers and clean API design

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt  # Production only
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html

# Run single test file
pytest tests/test_example.py

# Run specific test
pytest tests/test_example.py::test_function_name
```

### Code Quality
```bash
# Format code with black
black src/ tests/

# Sort imports with isort
isort src/ tests/

# Lint with flake8
flake8 src/ tests/

# Static analysis with pylint
pylint src/

# Type checking with mypy
mypy src/
```

### Excel Operations
```bash
# Run Excel handler examples
python examples/excel_examples.py

# Run logging examples
python examples/logging_example.py
python examples/pretty_logging_example.py

# Run extraction example
python examples/extract_excel_sheets.py

# Run find and extract example
python examples/find_excel_example.py
```

### Main Scripts (CLI)

The project includes three main CLI scripts for production use:

```bash
# 1. Extract all sheets from Excel files in a directory
python process_excel_directory.py "COMPUTADOR 1"
python process_excel_directory.py "datos/" --output "resultados/" --parallel --workers 8

# 2. Consolidate individual Excel files or directories
python consolidate_excel.py archivo.xlsx
python consolidate_excel.py directorio/ --recursive --output consolidados/

# 3. Batch consolidate entire directories (with parallel support)
python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8
python batch_consolidate_excel.py "data/extraido/" --dry-run
```

## Architecture and Code Structure

### Core Modules

**src/excel_handler/** - Advanced Excel manipulation module
- `ExcelHandler` class: Full-featured Excel manipulation with context manager support
  - Reading: `read_excel_pandas()`, `read_excel_openpyxl()`, `read_all_sheets_pandas()`
  - Writing: `write_dataframe_to_excel()`, `write_multiple_sheets()`, `create_formatted_excel()`
  - Sheet manipulation: `add_sheet()`, `delete_sheet()`, `rename_sheet()`
  - Data extraction: `extract_sheet_to_dataframe()`, `extract_range()`
- `QuickExcel` class: One-liner operations for simple read/write tasks
  - `QuickExcel.read(file)` - Fast pandas-based reading
  - `QuickExcel.write(df, file)` - Simple DataFrame export
- Custom exceptions: `ExcelHandlerError`, `SheetNotFoundError`, `InvalidFileFormatError`, etc.
- Utility functions: `merge_excel_files()`, `split_excel_by_column()`, `compare_excel_files()`

**src/excel_consolidator/** - Excel consolidation and structure analysis
- `ExcelConsolidator` class: Consolidates extracted Excel files (simple or complex structures)
- `BatchConsolidator` class: Batch processing with parallel execution support
- Structure detection: Automatically identifies simple vs. complex (multi-table) Excel files
- Data extraction: `extract_data()`, `extract_all_sheets()`, `preview_data()`
- Analysis tools: `analyze_file_completely()`, `detect_structure()`, `get_sheet_names()`
- Data cleaning: `clean_dataframe()`, `normalize_column_names()`, `is_likely_header()`

**src/excel_extractor/** - Sheet extraction utilities
- Tools for extracting individual sheets from Excel workbooks
- Integration with finder and processor modules

**src/find_excel_and_extract_sheets/** - Directory scanning and extraction
- `find_and_extract_excel_sheets()`: Main function for batch extraction
- `scan_directory()`: Directory analysis and file discovery
- Parallel and sequential processing modes
- Size filtering and pattern exclusion support

**src/logger/** - Centralized logging system
- `logging_config.py`: Main logger setup and configuration
- `pretty.py`: **Pretty Logging** system for enhanced visual output
  - Visual helpers: `log_header()`, `log_section()`, `log_success()`, `log_error()`, `log_warning()`
  - Data formatting: `log_item()`, `log_stats()`, `log_file_info()`, `log_sheet_info()`
  - Context management: `indent()` context manager for hierarchical logs
  - Formatters: `format_number()`, `format_duration()`, `format_size()`
- `config_helper.py`: Dynamic configuration from environment variables
- Integration with `colorlog` for colored console output

**src/config.py** - Configuration management
- Loads environment variables from .env file
- Defines base directories: BASE_DIR, DATA_DIR, LOGS_DIR
- Configuration: DEBUG, LOG_LEVEL, LOG_FORMAT

### Main Scripts (Root Level)

**consolidate_excel.py** - CLI tool for consolidating Excel files
- Consolidates single files or entire directories
- Supports recursive processing
- Analysis-only mode available (`--analyze-only`)

**batch_consolidate_excel.py** - Batch consolidation with parallel processing
- Process multiple files simultaneously (`--parallel`, `--workers`)
- Dry-run mode for testing (`--dry-run`)
- Progress tracking and detailed statistics

**process_excel_directory.py** - Extract sheets from Excel files in directories
- Scans directories for Excel files
- Extracts all sheets to individual files
- Parallel processing support
- Size filtering and pattern exclusion

### Directory Structure
```
src/
├── excel_handler/        # Excel manipulation (read, write, format)
│   ├── handler.py       # ExcelHandler class
│   ├── quick.py         # QuickExcel for simple ops
│   ├── utils.py         # Utility functions
│   └── exceptions.py    # Custom exceptions
├── excel_consolidator/  # Consolidation and structure detection
│   ├── consolidator.py  # ExcelConsolidator class
│   ├── batch.py         # BatchConsolidator class
│   ├── detector.py      # Structure detection
│   ├── extractor.py     # Data extraction
│   └── utils.py         # Helper functions
├── excel_extractor/     # Sheet extraction utilities
├── find_excel_and_extract_sheets/  # Directory scanning
│   └── core.py          # Main extraction functions
├── logger/              # Logging system
│   ├── logging_config.py  # Logger setup
│   ├── pretty.py        # Pretty Logging helpers
│   └── config_helper.py   # Dynamic config
└── config.py           # Global configuration

tests/                  # Unit and integration tests
data/                   # Data files (created at runtime)
logs/                   # Application logs (created at runtime)
docs/                   # Comprehensive documentation
├── EXCEL_HANDLER.md    # Complete ExcelHandler guide
├── EXCEL_EXTRACTOR_GUIDE.md  # Extraction workflows
├── FIND_EXCEL_GUIDE.md       # Directory scanning guide
├── LOGGING_GUIDE.md          # Logging configuration
├── LOGGING_CONFIGURATION.md  # Advanced logging setup
└── PRETTY_LOGGING_GUIDE.md   # Pretty Logging reference
examples/               # Working examples
scripts/                # Utility scripts
```

## Excel Library Strategy

This project includes multiple Excel libraries, each optimized for specific use cases:

1. **pandas** - Fast data analysis and basic read/write operations
2. **openpyxl** - Full-featured .xlsx manipulation with styles, formulas, and formatting
3. **xlsxwriter** - Creating professionally formatted Excel files from scratch
4. **xlrd/xlwt** - Legacy .xls format (Excel 97-2003) support
5. **pyxlsb** - Reading binary .xlsb files
6. **python-calamine** - Ultra-fast Excel reading for large files

**Selection Guide:**
- Data analysis → use pandas
- Format preservation/modification → use openpyxl
- Creating formatted reports → use xlsxwriter
- Large file reading → use python-calamine
- Legacy .xls files → use xlrd/xlwt

## Configuration

### pyproject.toml Settings
- **black:** line-length=88, Python 3.8-3.11
- **isort:** profile="black", compatible with black formatting
- **pytest:** verbose mode, auto-coverage (--cov=src), HTML reports, coverage reports in htmlcov/
- **mypy:** Python 3.8, ignore_missing_imports=true
- **pylint:** max-line-length=88, disables docstring and naming warnings
- **coverage:** source tracking, excludes tests and __init__.py

### Environment Variables
Create `.env` file in project root (see `.env.example`):
```bash
# Logging Configuration
DEBUG=False
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=simple           # simple, detailed, json

# Directories (optional, auto-created if needed)
DATA_DIR=data/
LOGS_DIR=logs/

# Processing Configuration
DEFAULT_WORKERS=4           # For parallel processing
MAX_FILE_SIZE_MB=100       # Skip files larger than this
```

## Important Patterns

### Excel Operations Pattern

#### Quick Operations (One-Liners)
```python
from excel_handler import QuickExcel

# Simple read/write operations
df = QuickExcel.read('file.xlsx')
QuickExcel.write(df, 'output.xlsx')
```

#### Advanced Operations (Multi-Sheet, Formatting)
```python
from excel_handler import ExcelHandler

# Using context manager (recommended)
with ExcelHandler('file.xlsx') as excel:
    excel.add_sheet('Ventas', df_ventas)
    excel.add_sheet('Resumen', df_resumen)
    excel.rename_sheet('Sheet1', 'Principal')
    excel.save()

# Manual management
handler = ExcelHandler('file.xlsx')
handler.read_excel_openpyxl()
handler.add_sheet('NewSheet', df)
handler.save()
handler.close()
```

### Consolidation Pattern
```python
from excel_consolidator import ExcelConsolidator, consolidate_excel_file

# Quick consolidation (helper function)
result = consolidate_excel_file('archivo.xlsx')
if result['success']:
    print(f"Consolidado: {result['output_file']}")

# Advanced consolidation with context manager
with ExcelConsolidator(output_dir='consolidados/') as consolidator:
    summary = consolidator.consolidate_directory('extraido/')
    print(f"Exitosos: {summary['successful']}/{summary['total_files']}")
```

### Batch Processing Pattern
```python
from excel_consolidator import BatchConsolidator

# Parallel batch processing
batch = BatchConsolidator(
    source_dir='data/extraido/',
    output_dir='data/consolidados/',
    parallel=True,
    max_workers=8
)
summary = batch.process_all()
print(f"Procesados: {summary['successful_files']}/{summary['total_files']}")
```

### Logging Pattern

#### Standard Logging
All modules use Python's standard logging with centralized configuration:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Error occurred", exc_info=True)
```

#### Pretty Logging (Visual Enhancement)
Use Pretty Logging for enhanced CLI output:
```python
from logger import setup_logger, setup_cli_logger
from logger.pretty import (
    log_header, log_section, log_success, log_error,
    log_item, log_stats, indent, format_number
)

logger = setup_cli_logger(setup_logger, __name__)

log_header(logger, "Mi Aplicación")
log_section(logger, "Procesando archivos")

with indent():
    log_item(logger, "archivo.xlsx", "Procesando...")
    # ... do work
    log_success(logger, f"Procesados: {format_number(count)} archivos")

log_stats(logger, {
    'Total': 100,
    'Exitosos': 95,
    'Fallidos': 5
})
```

### Path Handling
Use pathlib.Path for all file operations:
```python
from pathlib import Path

file_path = Path('data/file.xlsx')
file_path.parent.mkdir(parents=True, exist_ok=True)

# Check file existence
if file_path.exists():
    print(f"Found: {file_path.name}")
```

## Module Selection Guide

**Decision table for choosing the right tool/module:**

| Task | Use This | Example |
|------|----------|---------|
| Read single Excel file quickly | `QuickExcel.read()` | `df = QuickExcel.read('data.xlsx')` |
| Write DataFrame to Excel | `QuickExcel.write()` | `QuickExcel.write(df, 'output.xlsx')` |
| Multi-sheet manipulation | `ExcelHandler` (context manager) | `with ExcelHandler('file.xlsx') as excel: ...` |
| Compare two Excel files | `compare_excel_files()` | `diff = compare_excel_files('a.xlsx', 'b.xlsx')` |
| Merge multiple Excel files | `merge_excel_files()` | `merge_excel_files(['a.xlsx', 'b.xlsx'], 'merged.xlsx')` |
| Extract all sheets from workbook | `process_excel_directory.py` script | `python process_excel_directory.py "dir/"` |
| Consolidate extracted Excel file | `consolidate_excel.py` script | `python consolidate_excel.py archivo.xlsx` |
| Batch consolidate directory | `batch_consolidate_excel.py` script | `python batch_consolidate_excel.py "dir/" --parallel` |
| Consolidate programmatically | `ExcelConsolidator` class | `consolidator.consolidate_file('file.xlsx')` |
| Detect Excel structure | `detect_structure()` | `structure = detect_structure('file.xlsx')` |
| Analyze Excel file | `analyze_file_completely()` | `info = analyze_file_completely('file.xlsx')` |
| Enhanced CLI logging | Pretty Logging helpers | `log_header()`, `log_success()`, `with indent():` |

## Common Workflows

### Workflow 1: Extract and Consolidate
Complete workflow for processing complex Excel files:

```bash
# Step 1: Extract all sheets from Excel workbooks
python process_excel_directory.py "COMPUTADOR 1/" --output "data/extraido/"

# Step 2: Consolidate extracted files (parallel mode)
python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8

# Result: Clean, consolidated Excel files in data/consolidados/
```

### Workflow 2: Analyze Before Processing
Understand file structure before consolidation:

```bash
# Analyze structure without processing
python consolidate_excel.py archivo.xlsx --analyze-only

# If structure is complex, proceed with consolidation
python consolidate_excel.py archivo.xlsx --output resultados/
```

### Workflow 3: Programmatic Processing
Process Excel files from Python code:

```python
from excel_handler import QuickExcel
from excel_consolidator import consolidate_excel_file

# Read original file
df_original = QuickExcel.read('data.xlsx')

# Do some processing
df_processed = df_original[df_original['valor'] > 100]

# Save and consolidate
QuickExcel.write(df_processed, 'temp.xlsx')
result = consolidate_excel_file('temp.xlsx', output_dir='resultados/')
```

### Workflow 4: Batch Operations with Error Handling
Process multiple files with proper error handling:

```python
from pathlib import Path
from excel_consolidator import BatchConsolidator
from logger import setup_logger
from logger.pretty import log_header, log_success, log_error

logger = setup_logger(__name__)
log_header(logger, "Consolidación Batch")

batch = BatchConsolidator(
    source_dir='data/extraido/',
    output_dir='data/consolidados/',
    parallel=True,
    max_workers=4
)

try:
    summary = batch.process_all()
    log_success(logger, f"Completado: {summary['successful_files']}/{summary['total_files']}")
except Exception as e:
    log_error(logger, f"Error en batch: {e}")
```

## Testing Approach

- Tests located in `tests/` directory
- Use pytest framework with coverage reporting
- Test files follow `test_*.py` naming convention
- Coverage reports generated in `htmlcov/` directory
- Run tests: `pytest` or `pytest --cov=src --cov-report=html`

## Documentation

Comprehensive documentation available in `docs/`:

- **EXCEL_HANDLER.md** - Complete guide to ExcelHandler and QuickExcel (27KB, very detailed)
- **EXCEL_EXTRACTOR_GUIDE.md** - Sheet extraction workflows and examples
- **FIND_EXCEL_GUIDE.md** - Directory scanning and batch extraction
- **LOGGING_GUIDE.md** - Logging system configuration
- **LOGGING_CONFIGURATION.md** - Advanced logging setup
- **PRETTY_LOGGING_GUIDE.md** - Pretty Logging reference with all visual helpers

**Examples** available in `examples/`:
- `excel_examples.py` - ExcelHandler usage examples
- `logging_example.py` - Standard logging examples
- `pretty_logging_example.py` - Pretty Logging demonstrations
- `extract_excel_sheets.py` - Sheet extraction examples
- `find_excel_example.py` - Directory scanning examples

## Notes for Development

1. **Module Structure:** Project uses package-based structure with `__init__.py` files exposing clean APIs
2. **Context Managers:** Prefer context managers (`with`) for `ExcelHandler` and `ExcelConsolidator`
3. **Error Handling:** Custom exceptions in `excel_handler.exceptions` for domain-specific errors
4. **File Creation:** Excel operations automatically create `data/` and `logs/` directories if needed
5. **Type Hints:** Codebase uses type hints; mypy's `disallow_untyped_defs` is disabled for flexibility
6. **Dependencies:** All dependencies in `requirements.txt`; includes `colorlog` for colored logging
7. **Windows Compatibility:** Uses `pathlib.Path` for cross-platform compatibility
8. **Parallel Processing:** Batch scripts support `--parallel` flag with configurable worker count
9. **CLI Scripts:** Three main CLI scripts at root level for production workflows
10. **Pretty Logging:** Use Pretty Logging functions in CLI scripts for enhanced user experience
11. **Examples as Documentation:** All `examples/*.py` files are working code and serve as documentation
12. **Structure Detection:** Consolidator automatically detects simple vs. complex Excel structures
