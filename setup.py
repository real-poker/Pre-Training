"""
# Setup script to create .exe file using cx_Freeze 
"""
import sys
import os.path
from cx_Freeze import setup, Executable


PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

build_exe_options = {"packages": ["os"], "include_files":[os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'), os.path.join(PYTHON_INSTALL_DIR, 'DLLS', 'tcl86t.dll')]}

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

setup(
        name = "Pre-Training",
        version = "0.1",
        description = "NLHE Preflop Range Trainer",
        options = {"build_exe": build_exe_options},
        executables = [Executable("Pre-Training.py", base=base, icon='icon.ico')]
        )
