# run_app.spec
import os
import streamlit

block_cipher = None

# Path to Streamlit version metadata (required to avoid importlib.metadata error)
streamlit_dist_info = os.path.join(
    os.path.dirname(streamlit.__file__),
    "../streamlit-1.45.1.dist-info"
)

a = Analysis(
    ['run_app.py'],
    pathex=['.'],
    binaries=[],
datas=[
    ('FileTree_App.py', '.'),
    ('Graphviz_DirGraph.py', '.'),
    ('DF_from_Dir.py', '.'),
    ('ElasticGraph_fromDir.py', '.'), ('C:/Users/email/Desktop/Repos/Data_Science_IT_Support_repos/250601_FileTreeVisualization/.venv/Scripts/streamlit.exe', '.'),
],
    hiddenimports=[
        'streamlit',
        'streamlit.web.cli',
        'pywebview',
        'importlib.metadata',  # for streamlit.__version__
    ],
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
    name='FileTreeViewer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for final user build
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FileTreeViewer',
)
