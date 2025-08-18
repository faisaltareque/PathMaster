# PathMaster 🪄

A simple utility to dynamically and cleanly add directories to Python's `sys.path`, especially useful for projects with nested notebooks or scripts.

---
## Installation

You can install `PathMaster` directly from GitHub using `pip`:

```bash
pip install git+https://github.com/faisaltareque/PathMaster.git
```

---

## Usage
`PathMaster` helps you avoid messy relative path manipulations like `sys.path.append('../..')`.

### Add a Specific Directory

Use `pathmaster.add_path()` to add any absolute path to your system path. This is perfect for adding a shared lib or src folder.

```python
import pathmaster

# Add a specific library folder to the path
pathmaster.add_path('/path/to/your/project/libs')
# ✅ Successfully added '/path/to/your/project/libs' to sys.path.
```

### Add a Parent Directory

Use `pathmaster.add_parent()` to add a parent or grandparent directory relative to your current working directory. This is ideal for when your scripts or notebooks are in a subfolder (e.g., `notebooks/`) and need to import modules from the project root.

```python
import pathmaster

# Your script is in 'my_project/notebooks/'
# This will add 'my_project/' to the path
pathmaster.add_parent(levels=1)
# ✅ Successfully added '/path/to/your/my_project' to sys.path.
```

If no levels argument is provided, it defaults to 1 (the immediate parent).

---

### List Files in a Directory

Use `pathmaster.list_files()` function to view the contents of a directory.

```python
import pathmaster

# List files in the current directory
files = pathmaster.list_files('/path/to/directory')
print(files)
# Output: ['main.py', 'helper.txt', 'data.csv']

# List files with their absolute paths
files_absolute = pathmaster.list_files('.', absolute_path=True)
print(files_absolute)
# Output: ['/full/path/to/project/main.py', '/full/path/to/project/helper.txt', '/full/path/to/project/data.csv']
```

---