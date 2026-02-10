# -*- mode: python ; coding: utf-8 -*-



import os

def winpath(path):
    return path.replace('/', os.sep)

a = Analysis(
    [winpath('main.py')],
    pathex=[],
    binaries=[],
    datas=[(winpath('resources'), winpath('resources'))],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

    
a_stint = Analysis(
    [winpath('processors/stint_tracker/run.py')],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz_stint = PYZ(a_stint.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='StintFlow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[winpath('resources/favicons/favico.ico')],
)
exe_stint = EXE(
    pyz_stint,
    a_stint.scripts,
    [],
    exclude_binaries=True,
    name='StintTracker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    exe_stint,
    a.binaries,
    a.datas,
    a_stint.binaries,
    a_stint.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='StintFlow',
)
