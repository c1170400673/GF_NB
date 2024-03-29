# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main_V5.py'],
    pathex=[],
    binaries=[],
    datas=[('script/13_4.yaml','script'),
    ('script/8_1N.yaml','script'),
    ('script/config.yaml','script'),
	('script/target.yaml','script'),
#	('target/1080p_dpi280/*.png','target/1080p_dpi280'),
    ('target/720p_dpi240/*.png','target/720p_dpi240'),
	('README.md','.'),
	('logger.conf','.')],
    hiddenimports=[],
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
    name='GF_CAR',
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
    icon='app_icon.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GF_CAR',
)
