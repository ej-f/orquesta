#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import sys
from orquesta import __version__

sys.argv.append('build')
base = 'ConsoleKeepPath'
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
        Executable("orquesta.py", base = base)
]
includefiles = [] # 'externals/kitty.exe']
target_dir = "../../orquesta_build"
setup(name="Orquesta",
      version = __version__,
      author = "Edgar Fuentes",
      description = "Orquesta - an open source automation tool for remote terminal operations",
      options = {"build_exe": { "build_exe" : target_dir,
                                "optimize" : 2,
                                "create_shared_zip" : True,
                                "append_script_to_exe" : True,
                                "include_in_shared_zip" : False,
                                "include_files" : includefiles
                                },
                 },
      executables = executables,
      )
