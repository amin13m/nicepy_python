Tired of writing hundreds of lines with pathlib's verbose syntax? 🤯

Meet NicePath.

A clean OOP path object with dozens of short, chainable methods and properties.

No try/except boilerplate.
Just .read(), .write(), .move_to() … and it works.

✨ Smart search
🌳 Tree visualization
📝 Automatic logging of hundreds of files with a single method

Less code. More clarity.

------------------------------------------------------------

🚀 NicePy

Advanced OOP File & Directory Management Library for Python
Built on top of pathlib with logging, search engine, tree view and smart utilities.

------------------------------------------------------------

✨ Why NicePy?

NicePath is a powerful wrapper around Python’s built-in pathlib, designed to make file management:

✔ Cleaner
✔ More readable
✔ More powerful
✔ Fully logged
✔ Searchable
✔ Tree-view ready

------------------------------------------------------------

📦 Installation

🔹 Local Development Mode

pip install -e .

🔹 Future PyPI Installation

pip install nicepy

------------------------------------------------------------

🚀 Quick Start

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

------------------------------------------------------------

🌳 Tree Visualization

root = NicePath("my_project")
print(root.tree(ignore_hidden=False))

Example Output:

my_project
├── main.py
├── nicepy
│   ├── core.py
└── README.md

------------------------------------------------------------

🔎 Advanced Search

root.search(
    name_contains="core",
    suffix=".py",
    recursive=True,
    ignore_hidden=True
)

Supported Filters:

- name_contains
- suffix
- stem
- regex
- only_files
- only_dirs
- recursive
- ignore_hidden

If nothing is found → returns [] (never raises error)

------------------------------------------------------------

🧾 logAll – Full Project Logger

Generate:
- Full tree structure
- Content of matched files
- Save everything into a file

project = NicePath("my_project")
output = NicePath("log.txt")

project.logAll(
    file_output=output,
    search_suffix=".py"
)

Useful for:
- Project snapshot
- Debug logging
- Code export
- Archiving structure

------------------------------------------------------------

📚 Available Methods

write(data)              → Write text to file
read()                   → Read file content
append(data)             → Append to file
delete()                 → Remove file or directory
copy_to(dest)            → Copy file/folder
move_to(dest)            → Move file/folder
search(...)              → Smart search engine
tree(...)                → Visual tree display
logAll(...)              → Full structured log export

Properties:
exists
is_file
is_dir
size
created_time
modified_time

------------------------------------------------------------

⚖ NicePy vs pathlib

Feature                        | pathlib | NicePy
------------------------------------------------------------
Basic read/write               | Yes     | Yes
Append built-in                | No      | Yes
Tree view                      | No      | Yes
Search engine                  | No      | Yes
Regex search                   | No      | Yes
Logging system                 | No      | Yes
Full project log export        | No      | Yes
Unified OOP interface          | Basic   | Advanced
Custom exceptions              | No      | Yes

------------------------------------------------------------

## ⚠️ Safety Limits in NicePath

NicePath library includes powerful methods like logAll, tree, and search that can traverse large directories or read/write many files.

To prevent accidental overloads, these methods have default safety limits:

- logAll: limits the maximum number of files and total size it processes.
  - Default max_files=500
  - Default max_total_size=10_000_000 bytes (10 MB)
- tree and search:
  - Can ignore virtual environments and library folders (ignore_venv=True by default)
  - Can limit recursion depth or number of entries if needed.

Behavior when limits are reached:

- The operation does not crash.
- Partial results are written to the output file.
- A warning message is logged with logger.warning stating that safety limits were reached.

Customizing Safety:

You can override safety defaults in method calls:

`python
dir = NicePath("D:/Projects")
output_file = dir / "log.txt"

dir.logAll(
    file_output=output_file,
    search_suffix=".py",
    max_files=1000,          # increase limit
    max_total_size=50_000_000, # 50 MB
    ignore_venv=False         # include virtual environments
)

🛠 Logging System

All critical operations are logged:

- Start
- Success
- Failure
- Error reason

Helps debugging and production stability.

------------------------------------------------------------

🧪 Testing

pytest -v

------------------------------------------------------------

🏗 Project Structure

nicepy_python
├── pycache
│   ├── init.pythonc
│   └── main.cpython-314.pyc
├── nicepy
│   ├── pycache
│   │   ├── init.pyc
│   │   └── logger.cpython-314.pyc
│   ├── nicepath
│   │   ├── pycache
│   │   │   ├── init.pyc
│   │   │   ├── core.cpython-314.pyc
│   │   │   └── exceptios.cpython-314.pyc
│   │   ├── init.py
│   │   ├── core.py
│   │   └── exceptios.py
│   ├── init.py
│   └── logger.py
├── nicepy.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   └── top_level.txt
├── tests
│   ├── pycache
│   │   ├── test_nicepath.cpython-314-pytest-9.0.2.pyc
│   │   └── test_nicepath.cpython-314.pyc
│   ├── newfolder
│   │   ├── ksc.txt
│   │   ├── tet.txt
│   │   └── text.txt
│   └── test_nicepath.py
├── init.py
├── main.py
├── pyproject.toml
└── README.md

------------------------------------------------------------

🔮 Roadmap

[ ] PyPI release
[ ] Async support
[ ] Caching search engine
[ ] Watchdog integration
[ ] Colored tree output
[ ] CLI interface

------------------------------------------------------------

👤 Author

Amin
GitHub: https://github.com/amin13m

------------------------------------------------------------

📜 License

MIT License

------------------------------------------------------------

💎 Philosophy

Clean code.
Predictable behavior.
Zero surprise file handling.