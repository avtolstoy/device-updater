# -*- mode: python -*-

block_cipher = None
from kivy.deps import sdl2, glew


a = Analysis(['..\\src\\gui.py'],
             pathex=['.\\installer'],
             binaries=None,
             datas=[('..\\src\\gui.kv','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='win_dir',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
                Tree('..\\src\\resources', prefix='resources'),
                Tree('..\\src\\assets', prefix='assets'),
		*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],        
               strip=False,
               upx=True,
               name='win_dir')
