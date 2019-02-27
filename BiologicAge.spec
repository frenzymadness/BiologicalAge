# -*- mode: python -*-

block_cipher = None


a = Analysis(['BiologicAge.py'],
             pathex=['C:\\Users\\Lumir\\BiologicAge'],
             binaries=[],
             datas=[("mainwindow.ui", "."), ("images", "images"), ("data", "data")],
             hiddenimports=["scipy._lib.messagestream", "sklearn.tree._utils", "sklearn.neighbors.typedefs", "sklearn.neighbors.quad_tree", "pandas._libs.tslibs.timedeltas"],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='BiologicAge',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
