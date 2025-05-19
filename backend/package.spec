# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

backend_dir = os.path.dirname(os.path.abspath(__name__))
hooks_dir = os.path.join(backend_dir, 'hooks')

# Path adjustments
frontend_dist = os.path.join('..', 'frontend', 'dist')
data_files = [
    (os.path.join('..', 'frontend', 'dist'), 'static'),
    (os.path.join('data', 'songs_2m_parquet.parquet'), 'data'),
    *collect_data_files('models'),
    *collect_data_files('werkzeug')  # Add werkzeug data files
]

hidden_imports = [
    'flask',
    'flask_cors',
    'werkzeug',
    'werkzeug.middleware.dispatcher',
    'werkzeug.wsgi',
    'pandas',
    'numpy',
    'scipy',
    'pyarrow',
    'sqlite3',
    'models.recommender',
    'models.search',
    'models.song_manager'
]

a = Analysis(
    ['app.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=[
        ('../frontend/dist', 'static'),
        ('data/songs_2m_parquet.parquet', 'data'),
        *collect_data_files('models')
    ],
    hiddenimports=hidden_imports,
    hookspath=[hooks_dir], 
    runtime_hooks=['runtime-hooks.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
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