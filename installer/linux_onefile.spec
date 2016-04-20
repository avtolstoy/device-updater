# -*- mode: python -*-

block_cipher = None

from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks




a = Analysis(['../src/gui.py'],
             pathex=['./installer'],
              binaries=None,
             datas=[ ('../src/gui.kv', '.')],
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
		**get_deps_all())
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
	  Tree('../src'),
          a.scripts,
	  a.binaries,
	  a.datas,
	  a.zipfiles,
          name='particle_system_firmware',
          debug=False,
          strip=False,
          upx=False,
          console=False )
coll = COLLECT(exe, Tree('../src'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='particle_system_firmware_dir')
