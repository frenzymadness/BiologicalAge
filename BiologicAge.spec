# -*- mode: python -*-

block_cipher = None


a = Analysis(['BiologicAge.py'],
             binaries=[],
             datas=[('mainwindow.ui', '.'),
                    ('images', 'images'),
                    ('data', 'data')],
             hiddenimports=['scipy._lib.messagestream', 'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils', 'pandas._libs.tslibs.timedeltas'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

# For folder

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='BiologicAge',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='BiologicAge')

###################################################

# For file

# exe = EXE(pyz,
#           a.scripts,
#           a.binaries,
#           a.zipfiles,
#           a.datas,
#           name='BiologicAge',
#           debug=False,
#           strip=False,
#           upx=True,
#           runtime_tmpdir=None,
#           console=False )
