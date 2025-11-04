# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project specialized in Excel file manipulation and data processing. The project includes comprehensive tools and utilities for reading, writing, formatting, and processing Excel files using various Python libraries.

**Primary Purpose:** Advanced Excel file handling with support for .xlsx, .xls, and .xlsb formats

**Key Technology:** Python 3.8+ with pandas, openpyxl, xlsxwriter, and other Excel libraries

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
# Verify Excel libraries installation
python scripts/test_excel_setup.py

# Run all Excel examples (creates sample files in data/)
python src/excel_examples.py

# Run main application
python src/main.py
```

## Architecture and Code Structure

### Core Modules

**src/excel_handler.py** - Central module for Excel operations
- `ExcelHandler` class: Main interface for Excel manipulation
  - Reading: `read_excel_pandas()`, `read_excel_openpyxl()`, `read_all_sheets_pandas()`
  - Writing: `write_dataframe_to_excel()`, `write_multiple_sheets()`, `create_formatted_excel()`
  - Sheet manipulation: `add_sheet()`, `delete_sheet()`, `rename_sheet()`
  - Data extraction: `extract_sheet_to_dataframe()`, `extract_range()`
- Utility functions: `merge_excel_files()`, `split_excel_by_column()`

**src/excel_examples.py** - 10 comprehensive examples demonstrating all Excel functionality

**src/config.py** - Configuration management
- Loads environment variables from .env file
- Defines base directories: BASE_DIR, DATA_DIR, LOGS_DIR
- Configuration: DEBUG, LOG_LEVEL

**src/main.py** - Application entry point with logging setup

### Directory Structure
```
src/          # Main source code
tests/        # Unit and integration tests
data/         # Data files (created at runtime)
logs/         # Application logs (created at runtime)
docs/         # Documentation including EXCEL_GUIDE.md
scripts/      # Utility scripts
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
- **pytest:** verbose mode, auto-coverage (--cov=src), HTML reports
- **mypy:** Python 3.8, ignore_missing_imports=true
- **pylint:** max-line-length=88, disables docstring and naming warnings

### Environment Variables
Create `.env` file in project root:
```
DEBUG=False
LOG_LEVEL=INFO
```

## Important Patterns

### Excel Operations Pattern
```python
# For pandas-based operations (data analysis)
df = ExcelHandler.read_excel_pandas('file.xlsx')
# ... process df
ExcelHandler.write_dataframe_to_excel(df, 'output.xlsx')

# For openpyxl-based operations (formatting, sheet manipulation)
handler = ExcelHandler('file.xlsx')
handler.read_excel_openpyxl()
handler.add_sheet('NewSheet', df)
handler.save()
handler.close()
```

### Logging Pattern
All modules use Python's standard logging with centralized configuration from config.py:
```python
import logging
logger = logging.getLogger(__name__)
logger.info("Message")
```

### Path Handling
Use pathlib.Path for all file operations:
```python
from pathlib import Path
file_path = Path('data/file.xlsx')
file_path.parent.mkdir(parents=True, exist_ok=True)
```

## Testing Approach

- Tests located in `tests/` directory
- Use pytest framework with coverage reporting
- Test files follow `test_*.py` naming convention
- Coverage reports generated in `htmlcov/` directory

## Notes for Development

1. **File Creation:** Excel operations automatically create the `data/` directory if it doesn't exist
2. **Type Hints:** The codebase uses type hints but mypy's `disallow_untyped_defs` is disabled for flexibility
3. **Dependencies:** No dev requirements file exists; all dependencies are in requirements.txt
4. **Windows Compatibility:** Project structure supports Windows paths (uses pathlib for cross-platform compatibility)
5. **Examples as Documentation:** The `excel_examples.py` file serves as both documentation and functional examples
