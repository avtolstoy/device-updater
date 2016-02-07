


- DONT:: install kivy - https://kivy.org/docs/installation/installation-osx.html#using-the-kivy-app
- test by typing `kivy`, then `import kivy` in the REPL
- eh, cannot use Kivy.app because the dlls include @import_path/SDL2_ttf etc.. which fails to work when packaged as an installer.

test the app - `kivy main.py`

Python 3.4

Instead, have to manually install
virtualenv -p /usr/bin/python3.4 venv
source venv/bin/activate

On windows, requires OpenGL 2.0 (found out that this isn't supported on VirtualBox with Windows 8 Guest. Upgraded to Windows 10.)

brew tap Homebrew/python
brew update



brew install sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install -I Cython==0.23
CC=cc CXX=c++ USE_OSX_FRAMEWORKS=0 pip install kivy

brew install pygame

pip install PyInstaller


https://twistedpairdevelopment.wordpress.com/2012/03/19/installing-kivy-on-os-x-from-pip-and-homebrew/


https://groups.google.com/forum/#!msg/kivy-users/MmhoPHBzLhk/oDnxOprSZ5UJ

