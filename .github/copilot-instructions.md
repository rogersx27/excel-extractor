# Copilot Instructions for ascrudos

## Project Overview
Python project specialized in **Excel file manipulation and data processing**. Built for robust handling of .xlsx, .xls, and .xlsb formats with comprehensive logging and modular architecture.

**Core Purpose:** Advanced Excel operations with production-ready utilities for data extraction, formatting, and file management.

## Architecture Patterns

### Module Structure
- **`src/excel_handler.py`** - Central `ExcelHandler` class with dual API: pandas (fast analysis) + openpyxl (formatting/styles)
- **`src/excel_extractor/`** - Specialized module for splitting multi-sheet Excel files into individual files
- **`src/find_excel_and_extract_sheets.py`** - Advanced utility for batch processing: find Excel files in directories and extract sheets with parallel/sequential/batch strategies
- **`src/logger/`** - Custom logging system with date-based file rotation and colored console output
- **`src/config.py`** - Path management using `pathlib.Path` with auto-directory creation

### Key Design Principles
1. **Dual Excel APIs**: Use pandas for data operations, openpyxl for formatting/styling
2. **Path-based Configuration**: All paths defined in `config.py` using `Path` objects
3. **Modular Logging**: Each module gets its own logger via `setup_logger(__name__)`
4. **Auto-directory Creation**: `DATA_DIR` and `LOGS_DIR` created automatically

## Essential Workflows

### Environment Setup (Windows-first)
```powershell
python -m venv .venv
.venv\Scripts\activate  # Windows PowerShell pattern
pip install -r requirements.txt
```

### Excel Operations Entry Points
```python
# Central pattern - import ExcelHandler class
from excel_handler import ExcelHandler

# Reading: pandas for data, openpyxl for formatting
df = ExcelHandler.read_excel_pandas(file_path, sheet_name=0)
wb = ExcelHandler.read_excel_openpyxl(file_path)

# Writing with formatting
ExcelHandler.create_formatted_excel(df, output_path, sheet_name='Data')

# Batch processing with find_excel_and_extract_sheets
from find_excel_and_extract_sheets import find_and_extract_excel_sheets, ProcessingStrategy

result = find_and_extract_excel_sheets(
    search_directory="COMPUTADOR 1",
    strategy=ProcessingStrategy.PARALLEL,
    max_workers=4
)
```

### Testing and Quality
```bash
# Standard development workflow
pytest --cov=src --cov-report=html  # Coverage reports to htmlcov/
black src/ tests/                   # Code formatting
isort src/ tests/                   # Import sorting
python scripts/test_excel_setup.py  # Verify Excel libraries
```

## Project-Specific Conventions

### Logging Pattern
```python
from logger import setup_logger
logger = setup_logger(__name__)  # Module-specific logger
```
- Creates date-based log files: `logs/YYYY-MM-DD.log`
- Colored console output using `colorlog`
- Different log levels per module configuration

### Excel File Organization
- Input files: `COMPUTADOR 1/` (real Excel files from users)
- Generated files: `data/` (programmatic outputs)
- Examples create sample files demonstrating all functionality

### Error Handling Pattern
Excel operations use defensive programming:
```python
try:
    result = ExcelHandler.read_excel_pandas(file_path)
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
except Exception as e:
    logger.error(f"Excel operation failed: {e}")
```

## Integration Points

### External Dependencies
- **pandas**: Primary data manipulation (2.2.0+)
- **openpyxl**: Excel formatting and styles (3.1.2+)
- **xlsxwriter**: Advanced Excel writing with charts
- **pyxlsb**: Binary Excel file support
- **python-dotenv**: Environment configuration

### Cross-Module Communication
- `config.py` provides shared paths and settings
- `logger/` system used across all modules
- `excel_extractor/` imports from main `excel_handler.py`
- Examples in `examples/` demonstrate integration patterns

## Development Notes

When working with Excel files:
1. **Always** use `Path` objects from `config.py` for file paths
2. **Choose API** based on need: pandas (data) vs openpyxl (formatting)
3. **Log operations** using module-specific loggers
4. **Test with** `scripts/test_excel_setup.py` after dependency changes
5. **Follow examples** in `examples/excel_examples.py` for implementation patterns

Key files to reference: `src/excel_handler.py` (main API), `examples/excel_examples.py` (usage patterns), `src/config.py` (paths/settings), `src/find_excel_and_extract_sheets.py` (batch processing), `examples/find_excel_example.py` (batch processing examples).
