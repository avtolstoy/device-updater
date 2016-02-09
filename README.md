
## Features

- available as CLI and GUI
- cross platform - Windows, OSX, Linux, (potentially Android, iOS also)
- automatically detects devices when they are connected
- ymodem client implementation
- ymodem server implementation
- handles flashing multiple files and the ensuing device resets
- progress notification spans multiple flashes


## Roadmap

- DONE: multi file flash
- DONE: composite progress notification
- DONE: PoC console app to flash to a real device
- DONE: threading for app/UI separation
- DONE: gui app to flash to the device
- DONE: hide button when it's not needed - move widgets offscreen that aren't needed
- DONE: reveal progress bar when it's needed
- DONE: center device image
- DONE: white background
- DONE: particle logo
- DONE: fade in/out device on connection change
- DONE: text displaying device type / port
- DONE: derived properties for updating and other state
- DONE: different button colors for different states
- DONE: on last flash, don't go to complete until the device has rebooted
- DONE: Capture exceptions on the app thread and propagate to UI thread

- Install Serial driver on Windows if needed using either windows standard command line tools or libdwi
- Device text / image pulled from Device config
- Intro page? - tell the user what the tool does. next button swipes to flash page
- Complete page? - page when update is complete. Helps the user have closure - process is done.
  Back button to flash more devices. Close button to close the app.
- signing executable file on windows, signing for other platforms? dmg on OSX?


## Test plan

- device initially listening
- device initially connecting to the cloud
- ...

## Todo before Release
- propagate exceptions on actor thread via callback
- ymodem from listening mode
- Add exception handler for app that displays a popup then exits.


## Rough setup notes

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

