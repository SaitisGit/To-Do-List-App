import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="TodoApp",
    version="1.0",
    description="To-Do List Application",
    options={"build_exe": {"packages": ["tkinter", "time", "random", "datetime"], "include_files": ["tasks.txt"]}},
    executables=[Executable("todo.py", base=base)]
)
