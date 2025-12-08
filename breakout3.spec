# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['breakout3.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sounds', 'sounds'),
        ('breakout3.icns', '.'),
        ('breakout3.png', '.'),
    ],
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
    [],
    exclude_binaries=True,
    name='BreakOut3',
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
    icon='breakout3.icns',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BreakOut3',
)

app = BUNDLE(
    coll,
    name='BreakOut3.app',
    icon='breakout3.icns',
    bundle_identifier='com.freqrider.breakout3',
    info_plist={
        'CFBundleName': 'BreakOut3',
        'CFBundleDisplayName': 'BreakOut3',
        'CFBundleIdentifier': 'com.freqrider.breakout3',
        'CFBundleVersion': '1.1.0',
        'CFBundleShortVersionString': '1.1.0',
        'CFBundlePackageType': 'APPL',
        'CFBundleSignature': '????',
        'CFBundleIconFile': 'breakout3.icns',
        'NSHighResolutionCapable': True,
        'LSEnvironment': {
            'PYGAME_HIDE_SUPPORT_PROMPT': '1'
        },
    },
)