# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['XGPT.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tiktoken_ext.openai_public', 'tiktoken_ext'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='X-GPT',
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
    icon=['GPT.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='X-GPT',
)
app = BUNDLE(
    coll,
    name='X-GPT.app',
    icon='GPT.icns',
    bundle_identifier=None,
)
