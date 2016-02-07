# -*- mode: python -*-

block_cipher = None
from kivy.tools.packaging.pyinstaller_hooks import get_deps_all, hookspath, runtime_hooks


a = Analysis(['../main.py'],
             pathex=['/Users/mat1/dev/spark/device-updater/installer'],
             binaries=None,
             datas=None,
             hookspath=hookspath(),
             runtime_hooks=runtime_hooks(),
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
		**get_deps_all())
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
	  a.binaries,
	  a.datas,
	  a.zipfiles,
          name='devupd',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('..'),
Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_image.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_ttf.framework'),Tree('/Applications/Kivy.app/Contents/Frameworks/SDL2_mixer.framework'),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='device_updater')
