# script.spec
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['script.py'],  # Main Python script
    pathex=['.'],  # Current directory where your script is located
    binaries=[],
    datas=[
        ('pasteicon.png', '.'),  # Include the paste icon in the root of the app
    ],
    hiddenimports=[
        'PIL',  # Pillow library for image handling
        'customtkinter',  # CustomTkinter library for GUI
    ],  # Add any hidden imports if necessary
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Sortlify',  # Name of the executable
    debug=False,
    strip=False,
    upx=True,
    console=False,  # Set to False to avoid showing a terminal window
    icon='icon.icns'  # Path to your .icns icon file (optional)
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Sortlify'
)

app = BUNDLE(
    coll,
    name='Sortlify.app',  # Name of the .app bundle
    icon='icon.icns',  # Path to your .icns icon file (optional)
    bundle_identifier='chamiru.made.this.Sortlify'  # Unique bundle identifier
)