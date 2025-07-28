import sys
import pathlib

def add_path(custom_path: str):
    """
    Adds a specific, absolute path to the system path if it exists and is not already there.

    Args:
        custom_path (str): The absolute path to the directory to add.
    """
    path_to_add = pathlib.Path(custom_path).resolve()
    
    if not path_to_add.exists() or not path_to_add.is_dir():
        print(f"⚠️ Warning: Path '{path_to_add}' does not exist or is not a directory.")
        return

    if str(path_to_add) not in sys.path:
        sys.path.insert(0, str(path_to_add))
        print(f"✅ Successfully added '{path_to_add}' to sys.path.")
    else:
        print(f"ℹ️ Path '{path_to_add}' is already in sys.path.")


def add_parent(levels: int = 1):
    """
    Adds a parent directory of the current working directory to the system path.

    Args:
        levels (int): The number of parent levels to go up. 
                      1 for the immediate parent, 2 for the grandparent, etc.
    """
    current_dir = pathlib.Path.cwd()
    
    parent_path = current_dir
    try:
        for _ in range(levels):
            parent_path = parent_path.parent
    except IndexError:
        print(f"⚠️ Warning: Cannot go up {levels} levels from '{current_dir}'.")
        return
    add_path(str(parent_path))