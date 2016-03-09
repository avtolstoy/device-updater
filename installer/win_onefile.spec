# -*- mode: python -*-

block_cipher = None
from kivy.deps import sdl2, glew

a = Analysis(['..\\src\\win.py'],
             pathex=['.\installer'],
             binaries=None,
             datas=[ ('..\\src\\gui.kv', '.'), ('..\\src\\assets', 'assets'), ('..\\src\\resources','resources')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
		*[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
          name='particle_updater',
          debug=False,
          strip=False,
          upx=False,
          console=True,
          icon='resources/particle.ico' )
