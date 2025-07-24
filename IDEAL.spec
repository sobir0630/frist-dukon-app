# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['dukon.py'],
    pathex=[],
    binaries=[],
    datas=[('app_config.json', '.'), ('deleted_phones.json', '.'), ('internal_codes.json', '.'), ('passwords.json', '.'), ('selected_phone.json', '.'), ('sold_phones.json', '.'), ('sotish_file.json', '.'), ('telefon_data.json', '.'), ('theme_settings.json', '.')],
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
    name='IDEAL',
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
    icon=['images\\ideal.ico'],
)
