# -*- mode: python ; coding: utf-8 -*-
"""Congela Gamma Lab con PyInstaller (R39): una carpeta con GammaLab.exe.

Los plugins se cargan por ruta (`core/plugins/loader.py`), así que PyInstaller no ve lo que
importan. Este archivo lee con `ast` los imports de todo `plugins/` y los declara como
`hiddenimports`: un plugin nuevo no obliga a editarlo.
"""
import ast
import importlib.util
import os
from pathlib import Path

raiz = Path(SPECPATH).parent
PROPIOS = ("core", "plugins", "app", "test", "resources_rc")   # (los de core y app se agregan aparte, enteros)


def es_modulo(nombre):
    try:
        return importlib.util.find_spec(nombre) is not None
    except (ImportError, ValueError, AttributeError):
        return False


def importaciones_de_plugins():
    nombres = set()
    for archivo in (raiz / "plugins").rglob("*.py"):
        try:
            arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError):
            continue
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                nombres.update(a.name for a in nodo.names)
            elif isinstance(nodo, ast.ImportFrom) and nodo.level == 0 and nodo.module:
                nombres.add(nodo.module)
                nombres.update(f"{nodo.module}.{a.name}" for a in nodo.names
                               if a.name != "*" and es_modulo(f"{nodo.module}.{a.name}"))
    return sorted(n for n in nombres if n.split(".")[0] not in PROPIOS)


def modulos_propios():
    """Todo `core/` y `app/`: los plugins importan módulos que `main.py` no importa."""
    nombres = []
    for carpeta in ("core", "app"):
        for archivo in (raiz / carpeta).rglob("*.py"):
            if "__pycache__" in archivo.parts:
                continue
            partes = list(archivo.relative_to(raiz).with_suffix("").parts)
            if partes[-1] == "__init__":
                partes.pop()
            nombres.append(".".join(partes))
    return sorted(nombres)


def datos(carpeta):
    """(origen, destino) de cada archivo de `carpeta`, sin cachés."""
    return [(str(p), str(Path(carpeta) / p.parent.relative_to(raiz / carpeta)))
            for p in (raiz / carpeta).rglob("*")
            if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]


a = Analysis(
    [str(raiz / "main.py")],
    pathex=[str(raiz)],
    datas=datos("plugins") + datos("assets"),
    hiddenimports=importaciones_de_plugins() + modulos_propios() + ["yaml", "vtkmodules.all"],
    excludes=["tkinter", "pytest", "test", "torch", "torchvision"],   # SciPy sondea torch si está instalado: 378 MB que no se usan
)
# PyQt5 trae msvcp140*.dll 14.26 (2020) y NumPy, SciPy y VTK necesitan una más nueva: se usan
# las del sistema en todo el programa, que además no exige tener instalado el runtime de Visual C++.
sistema = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32"
nuevas = [(n, str(sistema / n), "BINARY") for n in ("msvcp140.dll", "msvcp140_1.dll", "msvcp140_2.dll")
          if (sistema / n).exists()]
NOMBRES_MSVCP = {"msvcp140.dll", "msvcp140_1.dll", "msvcp140_2.dll"}   # (NumPy y VTK traen copias con sufijo hash: se dejan)
a.binaries = [b for b in a.binaries if Path(b[0]).name.lower() not in NOMBRES_MSVCP] + nuevas
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, [],
    exclude_binaries=True,
    name="GammaLab",
    console=False,
    icon=str(raiz / "assets" / "logos" / "app-logo.ico"),
)
coll = COLLECT(exe, a.binaries, a.datas, name="GammaLab")
