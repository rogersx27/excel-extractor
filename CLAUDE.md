# CLAUDE.md

Guidance for Claude Code (claude.ai/code) working with this repository.

## Project Overview

**Purpose:** Advanced Excel manipulation (extraction, consolidation, batch processing)
**Tech:** Python 3.8+, pandas, openpyxl, xlsxwriter, xlrd, pyxlsb, python-calamine
**Features:** Multi-format (.xlsx/.xls/.xlsb) | Auto extraction/consolidation | Parallel processing | Pretty Logging | Structure detection | Context managers

## Key Commands

```bash
# Setup
python -m venv .venv && source .venv/bin/activate  # (.venv\Scripts\activate on Windows)
pip install -r requirements.txt

# Testing & Quality
pytest --cov=src --cov-report=html
black src/ tests/ && isort src/ tests/
flake8 src/ tests/ && pylint src/ && mypy src/

# Main Scripts (CLI)
python process_excel_directory.py "dir/" --output "out/" --parallel --workers 8
python consolidate_excel.py file.xlsx --output "consolidated/" --recursive
python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8 --dry-run

# Examples
python examples/{excel_examples,logging_example,pretty_logging_example,extract_excel_sheets,find_excel_example}.py
```

## Architecture

```toon
Modules[8]{path,purpose,key_items}:
 src/excel_handler/,Excel manipulation,"QuickExcel.read/write, ExcelHandler(ctx mgr), merge/split/compare utils, custom exceptions"
 src/excel_consolidator/,Consolidation,"ExcelConsolidator, BatchConsolidator, detect_structure, analyze_file_completely"
 src/excel_extractor/,Sheet extraction,"Extract individual sheets, integration with processor"
 src/find_excel_and_extract_sheets/,Directory scan,"find_and_extract_excel_sheets, scan_directory, parallel support"
 src/logger/,Logging system,"setup_logger, pretty.py (log_header/section/success/error/stats), colorlog integration"
 src/config.py,Configuration,"Load .env, BASE_DIR/DATA_DIR/LOGS_DIR, DEBUG/LOG_LEVEL/LOG_FORMAT"
 consolidate_excel.py,CLI consolidate,"Single file/dir consolidation, --recursive, --analyze-only"
 batch_consolidate_excel.py,CLI batch,"Parallel batch processing, --dry-run, --workers N"
 process_excel_directory.py,CLI extract,"Extract sheets from dir, --parallel, size filtering"

Docs[6]{file,content}:
 EXCEL_HANDLER.md,"Complete ExcelHandler/QuickExcel guide (27KB)"
 EXCEL_EXTRACTOR_GUIDE.md,"Sheet extraction workflows"
 FIND_EXCEL_GUIDE.md,"Directory scanning/batch extraction"
 LOGGING_GUIDE.md,"Logging configuration"
 LOGGING_CONFIGURATION.md,"Advanced logging setup"
 PRETTY_LOGGING_GUIDE.md,"Pretty Logging reference"

Examples[5]{file,demonstrates}:
 excel_examples.py,"ExcelHandler usage"
 logging_example.py,"Standard logging"
 pretty_logging_example.py,"Pretty Logging"
 extract_excel_sheets.py,"Sheet extraction"
 find_excel_example.py,"Directory scanning"
```

**Excel Libraries Selection:**
- Data analysis → pandas
- Format/styles → openpyxl
- Create formatted reports → xlsxwriter
- Large file reading → python-calamine
- Legacy .xls → xlrd/xlwt
- Binary .xlsb → pyxlsb

## Patterns

**Quick Excel Ops:**
```python
from excel_handler import QuickExcel
df = QuickExcel.read('file.xlsx')
QuickExcel.write(df, 'output.xlsx')
```

**Advanced (Multi-Sheet):**
```python
from excel_handler import ExcelHandler
with ExcelHandler('file.xlsx') as excel:
    excel.add_sheet('Ventas', df_ventas)
    excel.rename_sheet('Sheet1', 'Principal')
    excel.save()
```

**Consolidation:**
```python
from excel_consolidator import consolidate_excel_file, ExcelConsolidator
result = consolidate_excel_file('archivo.xlsx')  # Quick
with ExcelConsolidator(output_dir='out/') as cons:  # Advanced
    summary = cons.consolidate_directory('extraido/')
```

**Batch Processing:**
```python
from excel_consolidator import BatchConsolidator
batch = BatchConsolidator('data/extraido/', 'data/consolidados/', parallel=True, max_workers=8)
summary = batch.process_all()
```

**Pretty Logging:**
```python
from logger import setup_cli_logger, setup_logger
from logger.pretty import log_header, log_section, log_success, log_stats, indent, format_number

logger = setup_cli_logger(setup_logger, __name__)
log_header(logger, "App")
with indent():
    log_success(logger, f"Processed: {format_number(count)}")
log_stats(logger, {'Total': 100, 'Success': 95})
```

## Tool Selection

| Task | Tool | Usage |
|------|------|-------|
| Read Excel | `QuickExcel.read()` | `df = QuickExcel.read('data.xlsx')` |
| Write Excel | `QuickExcel.write()` | `QuickExcel.write(df, 'out.xlsx')` |
| Multi-sheet | `ExcelHandler` | `with ExcelHandler('f.xlsx') as e: ...` |
| Compare | `compare_excel_files()` | `diff = compare_excel_files('a.xlsx', 'b.xlsx')` |
| Merge | `merge_excel_files()` | `merge_excel_files(['a','b'], 'merged.xlsx')` |
| Extract sheets | `process_excel_directory.py` | CLI script |
| Consolidate file | `consolidate_excel.py` | CLI script |
| Batch consolidate | `batch_consolidate_excel.py` | CLI with --parallel |
| Programmatic consolidate | `ExcelConsolidator` | Class with context mgr |
| Detect structure | `detect_structure()` | Returns StructureType |
| Analyze file | `analyze_file_completely()` | Complete file analysis |
| CLI logging | Pretty Logging | `log_header/success/stats` |

## Workflows

**1. Extract + Consolidate:**
```bash
python process_excel_directory.py "COMPUTADOR 1/" --output "data/extraido/"
python batch_consolidate_excel.py "data/extraido/" --parallel --workers 8
```

**2. Analyze First:**
```bash
python consolidate_excel.py archivo.xlsx --analyze-only  # Check structure
python consolidate_excel.py archivo.xlsx --output resultados/  # Process if needed
```

**3. Programmatic:**
```python
from excel_handler import QuickExcel
from excel_consolidator import consolidate_excel_file
df = QuickExcel.read('data.xlsx')
df_filtered = df[df['valor'] > 100]
QuickExcel.write(df_filtered, 'temp.xlsx')
result = consolidate_excel_file('temp.xlsx', output_dir='resultados/')
```

**4. Batch with Error Handling:**
```python
from excel_consolidator import BatchConsolidator
from logger.pretty import log_header, log_success, log_error
batch = BatchConsolidator('data/extraido/', 'data/consolidados/', parallel=True, max_workers=4)
try:
    summary = batch.process_all()
    log_success(logger, f"Done: {summary['successful_files']}/{summary['total_files']}")
except Exception as e:
    log_error(logger, f"Error: {e}")
```

## Configuration

**pyproject.toml:** black (88), isort (black profile), pytest (--cov=src, html reports), mypy (ignore_missing_imports), pylint (88, no docstring warns), coverage (exclude tests/__init__)

**Environment (.env):**
```bash
DEBUG=False
LOG_LEVEL=INFO  # DEBUG|INFO|WARNING|ERROR|CRITICAL
LOG_FORMAT=simple  # simple|detailed|json
DATA_DIR=data/  # auto-created
LOGS_DIR=logs/  # auto-created
DEFAULT_WORKERS=4  # parallel processing
MAX_FILE_SIZE_MB=100  # skip larger files
```

## Dev Notes

1. Package structure with `__init__.py` exposing clean APIs
2. Prefer context managers (`with`) for ExcelHandler/ExcelConsolidator
3. Custom exceptions in `excel_handler.exceptions`
4. Auto-creates `data/` and `logs/` directories
5. Type hints used (mypy `disallow_untyped_defs=false`)
6. All deps in requirements.txt (includes colorlog)
7. Cross-platform via `pathlib.Path`
8. Batch scripts support `--parallel` with `--workers N`
9. Three main CLI scripts at root
10. Use Pretty Logging in CLI for UX
11. Examples are working code + documentation
12. Consolidator auto-detects simple/complex structures
13. Tests: `pytest --cov=src --cov-report=html` → `htmlcov/`
14. Docs in `docs/`, examples in `examples/`, scripts in `scripts/`
