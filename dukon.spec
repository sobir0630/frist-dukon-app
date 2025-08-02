# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dukon.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images'), ('deleted_phones.json', '.'), ('telefon_data.json', '.'), ('sotish_file.json', '.'), ('sotish_file.json', '.'), ('sold_phones.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='dukon',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
