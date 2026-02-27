# StintFlow AI Agent Instructions

StintFlow is a PyQt6 desktop application for tracking racing stints, tire management, and race strategies with LMU (Le Mans Ultimate) shared memory integration.

## Project Overview & Status

**Technology Stack**:
- Framework: PyQt6 | Language: Python 3.14 | Database: MongoDB | Integration: LMU Shared Memory (via `pyLMUSharedMemory` submodule)
- Build: PyInstaller (`StintFlow.spec`) | Execution: `python3 .\main.py`

## Architecture Overview

**Layered Architecture**: Strict separation between UI, shared infrastructure, and domain-specific processes.
- **`core/`**: Shared infrastructure (errors, logging, database operations)
  - `errors/`: Centralized error handling & logging system
  - `database/`: MongoDB operations (shared by all processes)
- **`ui/`**: PyQt6 components, models, styles, and UI orchestration
  - `components/`: Reusable PyQt6 widgets
  - `models/`: Table models, custom roles, view state management
  - `styles/`: QSS stylesheets
- **`processors/`**: Independent domain-specific processes
  - `stint_tracker/`: Core stint tracking process (runs standalone, called from UI)
    - `core/`: Stint-tracker-specific business logic (tire management, strategy calculations)
    - `strategies/`: Strategy-related functions
  - Future processors follow the same pattern
- **`pyLMUSharedMemory/`**: LMU game data integration (external submodule—leave as-is)

**Critical Pattern: One Function Per File**
- Each function in its own file for maintainability
- Barrel files (`__init__.py`) export functions from modules
- Example: `processors/stint_tracker/__init__.py` exports `get_stints()`, `validate_compound()`, etc.
- **Enforce this pattern rigorously** when adding functionality

**Independent Processes (Separate OS Processes)**
- Each processor is a **standalone Python script** that runs in its own OS process via `QProcess`
- Started by UI with command-line arguments; runs independently from the main PyQt6 application
- Communicates back to UI via stdout/stderr using the `__event__:category:action` format
- Example: `stint_tracker` runs as separate process: `python3 processors/stint_tracker/run.py --session-id <id> --drivers <names>`
- UI listens to stdout/stderr to receive status updates and trigger signals (e.g., `stint_created` event)

**Data Flow Pattern**:
UI signal → Launch process via QProcess → Process runs independently → Process outputs events to stdout → UI parses events → Model updates → UI display
(Example: User clicks "Start tracking" → QProcess launches `stint_tracker/run.py` → process calculates stints → outputs `__event__:stint_tracker:stint_created` → UI receives signal → TableModel updates)

## Key Conventions

### Code Organization & Style
- **PEP 8 compliance**, descriptive naming, comments explaining "why" not "what"
- **Private functions and methods**: Prefix with underscore (`_function_name`) to indicate they're only used internally
- **Docstrings**: Include for all functions, classes, modules (module-level comments explaining file purpose)
- **Inline comments**: Only for complex logic; explain reasoning and non-obvious behavior
- **Readability over brevity**: Explicit, clear code preferred over clever one-liners
- **Maintenance First**: Highest priority is easy understanding and modification
- **Type Hints**: Use type hints for clarity, but **DO NOT use `Optional`**—use default values instead (e.g., `def foo(models: ModelContainer = None)` not `def foo(models: Optional[ModelContainer] = None)`)

**Logging Convention**: Use the `log()` and `log_exception()` functions from `core.errors` instead of `print()` statements
- For regular logging: `log(level, message, category='component', action='specific_action')`
  - Levels: `'DEBUG'`, `'INFO'`, `'WARNING'`, `'ERROR'`, `'CRITICAL'`
  - Example: `log('DEBUG', 'Font loaded successfully', category='ui', action='setup_font')`
- For exceptions: `log_exception(exception, 'Error description', category='component', action='specific_action')`
  - Automatically includes full stack trace
  - Example: `log_exception(e, 'Failed to load stylesheet', category='main', action='load_stylesheet')`
- Structured logging ensures messages are written to both console and log file with proper timestamps and levels

### PyQt6 Patterns
- **Signals/Slots**: Use PyQt6 signals for cross-component communication, NOT direct function calls
- **Model Container Pattern**: Pass models to UI components using `ModelContainer` dataclass
  - Defined in `ui/models/model_container.py`
  - Example: `OverviewMainWindow(ModelContainer(selection_model=..., table_model=...))`
  - Provides type safety, IDE autocomplete, and clear dependencies
  - Component constructors accept `models: ModelContainer` parameter
- **Table Models**: Extend `QAbstractTableModel` with custom roles (`TableRoles.py`)
  - Store display data (`_data`) and metadata (`_tires`, `_meta`) separately
  - Use `beginResetModel()`/`endResetModel()` for bulk updates
  - Core methods: `rowCount()`, `columnCount()`, `data()`, `setData()`, `flags()`
- **UI Composition**: Prefer small, composable widgets over monolithic components (improvement goal)
- **Styling**: QSS files in `styles/` directory; avoid inline styles unless necessary

### Database & Business Logic
- All MongoDB operations through `core/database/`—**no direct DB calls in UI**
- Domain-specific logic lives in `processors/<domain>/`
- Keep functions stateless; pass minimal context
- Processor-specific helpers stay in `processors/<name>/core/` or relevant submodule

### Resource Loading
- **Always use `resource_path()`** helper for icons, fonts, stylesheets
- Validate paths exist before loading—log warnings if missing, **continue gracefully** (no crashes)
- Fonts: `get_fonts()` from UI utilities | Styles: QSS files in `ui/styles/`

## Error Handling & Logging

**Graceful Degradation**: App continues operation on error—no flat-out crashes
- Resources missing? Log warning, continue with defaults
- DB operation fails? Degrade gracefully, allow user to retry

## Code Quality & Improvement Guidance

**Priorities**:
1. **Clarity & Maintainability** (highest)—code should be easy to understand and modify
2. **Performance**—only prioritize if clear, measurable benefit; favor clarity otherwise
3. **Brevity**—never sacrifice readability for fewer lines

**When Suggesting Improvements**:
- Comment clarity, naming, spacing, function size, single responsibility
- Efficiency improvements that maintain or improve readability
- Python/PyQt6 best practices and common patterns
- File organization and the "one function per file" principle
- **Avoid shortcuts** that reduce lines at the cost of maintainability
- **NEVER remove TODO comments**—they document future work and incomplete features; if implementing the TODO, update or replace it with the completion

**Testing**: 
- Write code to be testable (dependency injection, separation of concerns)
- Tests not the current focus but code should enable testing later

## File Organization Examples

When adding new functionality:
```
Shared DB operation     → core/database/<operation_name>.py
Domain-specific logic   → processors/<domain>/core/<function_name>.py
Domain strategies       → processors/<domain>/strategies/<function_name>.py
UI component            → ui/components/<component_name>.py
UI model                → ui/models/<model_name>.py
Export function         → Add to relevant __init__.py
```

## Critical Integration Points

- **LMU Shared Memory**: Access via `pyLMUSharedMemory` submodule (typically from `processors/stint_tracker/`)
- **MongoDB**: All operations through `core/database/` layer
- **Error System**: Register handlers in `core/errors/handle_error.py`
- **Asset Loading**: Use `resource_path()` helper only
- **UI-to-Process Communication**: UI components launch processors; processes report back via stdout events

**Key Principles**:
- Processors are entirely separate OS processes—they don't share Python state with UI
- Each processor can be run standalone or integrated; design accordingly
- Use exit codes to signal success/failure to the UI
- Processors handle their own error logging; UI logs what it receives from stdout/stderr

## Processor Design Guidelines

**Scope**: Do not create a new processor, unless the user explicitly requests it. Instead, add functionality to existing processors (e.g., `stint_tracker`) or create new functions within the existing processor structure.

**Working Directory**: When launching via `QProcess`, paths are relative to the main app's working directory. Use `os.path.abspath()` or `pathlib.Path` for relative imports and resource access.

**Error Handling**: Processors should fail gracefully:
- Catch exceptions and print structured error messages to stderr
- Use appropriate exit codes (0 = success, non-zero = failure)
- Let the UI handle recovery based on exit code and stderr messages

**Exit Codes**: 
- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- Custom codes for specific failure modes (optional but recommended)
