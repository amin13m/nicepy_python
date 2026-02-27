<p align="center">  
  <img src="docs/logo.jpg" alt="NicePy Logo" width="150"/>  
</p>  

# NicePy

Tired of writing hundreds of lines with pathlib's verbose syntax? 🤯  

Meet NicePath, a clean OOP path object with dozens of short, chainable methods and properties.  

No try/except boilerplate. Just .read(), .write(), .move_to() … and it works.  

Smart search | Tree visualization | Automatic logging  

Less code. More clarity.  

------------------------------------------------------------

## What is NicePy?

Advanced OOP File & Directory Management Library for Python  
Built on top of pathlib with logging, search engine, tree view, and smart utilities.

### Why NicePy?

NicePath is a powerful wrapper around Python’s built-in pathlib, designed to make file management:

- Cleaner
- More readable
- More powerful
- Fully logged
- Searchable
- Tree-view ready

------------------------------------------------------------

## Installation

**Local Development Mode:**
```
pip install -e .
```

**PyPI Installation (Future):**
```
pip install nicepython
```

------------------------------------------------------------

## Quick Start

```python
from nicepy import NicePath

# Create path
p = NicePath("example.txt")

# Write data
p.write("Hello NicePy!")

# Read data
print(p.read())

# Append
p.append("\nNew Line")

# Show tree
root = NicePath(".")
print(root.tree())

# Search files
for f in root.search(suffix=".py"):
    print(f.path)
```

------------------------------------------------------------

## Tree Visualization

```python
root = NicePath("my_project")
print(root.tree(ignore_hidden=False))
```

**Example Output:**
```text
my_project
├── main.py
├── nicepy
│   ├── core.py
└── README.md
```

------------------------------------------------------------

## Advanced Search

```python
root.search(
    name_contains="core",
    suffix=".py",
    recursive=True,
    ignore_hidden=True
)
```

**Supported Filters:**

- name_contains
- suffix
- stem
- regex
- only_files
- only_dirs
- recursive
- ignore_hidden

Returns empty list if nothing is found. Never raises error.

------------------------------------------------------------

## logAll – Full Project Logger

```python
project = NicePath("my_project")
output = NicePath("log.txt")

project.logAll(
    file_output=output,
    search_suffix=".py"
)
```

Generates:

- Full tree structure
- Content of matched files
- Saves everything into a file

Use for project snapshot, debug logging, code export, or archiving structure.

------------------------------------------------------------

## Available Methods

| Method        | Description                        |
|---------------|------------------------------------|
| write(data)   | Write text to file                 |
| read()        | Read file content                  |
| append(data)  | Append to file                     |
| delete()      | Remove file or directory           |
| copy_to(dest) | Copy file/folder                   |
| move_to(dest) | Move file/folder                   |
| search(...)   | Smart search engine                |
| tree(...)     | Visual tree display                |
| logAll(...)   | Full structured log export         |

**Properties:**

- exists
- is_file
- is_dir
- size
- created_time
- modified_time

------------------------------------------------------------

## NicePy vs pathlib

| Feature                  | pathlib | NicePy |
|---------------------------|---------|--------|
| Basic read/write          | Yes     | Yes    |
| Append built-in           | No      | Yes    |
| Tree view                 | No      | Yes    |
| Search engine             | No      | Yes    |
| Regex search              | No      | Yes    |
| Logging system            | No      | Yes    |
| Full project log export   | No      | Yes    |
| Unified OOP interface     | Basic   | Advanced |
| Custom exceptions         | No      | Yes    |

------------------------------------------------------------

## Safety Limits

Methods like logAll, tree, and search have default limits to prevent overload:

- logAll: max_files=500, max_total_size=10_000_000 bytes (10 MB)
- tree & search: ignore_venv=True, can limit recursion/depth

**Behavior on limit reach:**

- Operation does not crash
- Partial results written
- Warning logged via logger.warning

**Override safety:**
```python
dir = NicePath("D:/Projects")
output_file = dir / "log.txt"

dir.logAll(
    file_output=output_file,
    search_suffix=".py",
    max_files=1000,
    max_total_size=50_000_000,
    ignore_venv=False
)
```

------------------------------------------------------------

## Logging System

All critical operations are logged:

- Start
- Success
- Failure
- Error reason

Ensures debugging & production stability.

------------------------------------------------------------

## Testing

```
pytest -v
```

------------------------------------------------------------

## Project Structure

```text
nicepy_python/
├── nicepy/
│   ├── nicepath/
│   │   ├── core.py
│   │   └── exceptios.py
│   └── logger.py
├── tests/
├── main.py
├── README.md
├── pyproject.toml
└── docs/
    └── index.html
```

------------------------------------------------------------

## Roadmap

- [ ] PyPI release
- [ ] Async support
- [ ] Caching search engine
- [ ] Watchdog integration
- [ ] Colored tree output
- [ ] CLI interface

------------------------------------------------------------

## Documentation

Live SPA Documentation: https://amin13m.github.io/nicepy_python/

------------------------------------------------------------

## Author

Amin  
GitHub: https://github.com/amin13m

------------------------------------------------------------

## License

MIT License

------------------------------------------------------------

## Philosophy

Clean code. Predictable behavior. Zero surprise file handling.