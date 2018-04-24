import sys
import os.path
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'
    
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

options = {
    'build_exe': {
        'include_files':[
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tk86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, 'DLLs', 'tcl86t.dll'),
            os.path.join(PYTHON_INSTALL_DIR, '', 'vcruntime140.dll'),
         ],
        'includes': ['numpy.core._methods',
                     'numpy.lib.format',
                     'matplotlib.backends.backend_tkagg',
                     'tkinter',
                     'tkinter.filedialog']
    }
}

executables = [
    Executable('surfacefit_for_shading.py', base=base)
]

setup(name='shading',
      version='0.1',
      description='shading fit',
      options=options,
      executables=executables
      )
