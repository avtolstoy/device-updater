# -*- mode: python -*-
import os
appname=os.environ['appname']
fqname=os.environ['fqname']
version=os.environ['VERSION']

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
          name=fqname,
          debug=False,
          strip=False,
          upx=False,
          console=False )
coll = COLLECT(exe, Tree('../src'),
        Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_image.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_ttf.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_mixer.framework'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name=appname)
app = BUNDLE(exe,
             name=fqname+'.app',
             icon='resources/particle.icns',
             bundle_identifier=None)
