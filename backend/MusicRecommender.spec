# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None
frontend_dist = os.path.join('..', 'frontend', 'dist')
data_files = [
    (os.path.join('..', 'frontend', 'dist', 'assets'), 'static/assets'),
    (os.path.join('..', 'frontend', 'dist', 'index.html'), 'static'),
    (os.path.join('data', 'songs_2m_parquet.parquet'), 'data'),
    (os.path.join('data', 'tracksdb.db'), 'data'),
    *collect_data_files('models'),
    *collect_data_files('werkzeug')  # Add werkzeug data files
]

a = Analysis(
    ['app.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        (os.path.join('..', 'frontend', 'dist', 'assets'), 'static/assets'),
        (os.path.join('..', 'frontend', 'dist', 'index.html'), 'static'),
        (os.path.join('data', 'songs_2m_parquet.parquet'), 'data'),
        (os.path.join('data', 'tracksdb.db'), 'data'),
        *collect_data_files('models')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    optimize=0,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MusicRecommender',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    onefile=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('..', 'frontend', 'public', 'favicon.ico') if os.path.exists(os.path.join('..', 'frontend', 'public', 'favicon.ico')) else None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MusicRecommender'
)